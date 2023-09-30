#!/usr/bin/env python
"""
This project queries the KEGG database base on
align_predicted.txt file from assignment nine and
append orthology information such as KEGG pathways
back to the BLAST file
"""

import argparse
import requests


def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Enter input filename, e-value threshold, and output filename from the\
        command line arguments",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Create a sequential argument (eg. it has to come in the order defined)
    # Create a flagged argument (eg. input comes after a short "-i" or long "--input" form flag)
    parser.add_argument('-e', '--evalue',
                        metavar='FLOAT',
                        help='evalue threshold',
                        type=float,
                        default=10**-5,  # default option if no input is given by the user
                        )
    parser.add_argument('-i', '--infile',
                        metavar='STRING',
                        help='Input File Name for querying KEGG data',
                        type=str,
                        default='./data/alignPredicted.txt'
                        )
    parser.add_argument('-o', '--outfile',
                        metavar='STRING',
                        help='Output File Name for adding the KEGG pathways data',
                        type=str,
                        default='./data/alignPredicted_new.txt'
                        )
    return parser.parse_args()


def get_uniprot_id(blast_line, threshold):
    """Return UniProt ID from the BLAST line if the evalue is below the threshold.

    Returns False if evalue is above threshold.
    """
    cleaned_line = blast_line.strip()
    blast_fields = cleaned_line.split("\t")
    if float(blast_fields[7]) < float(threshold):
        return blast_fields[1]
    return False


def get_kegg_genes(uniprot_id):
    """Return a list of KEGG organism:gene pairs for a provided uniprot_id."""
    result = requests.get(
        f'https://rest.kegg.jp/conv/genes/uniprot:{uniprot_id}', timeout=5)
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)
        fields = str_entry.split("\t")
        # To avoid a complex 2D array, get the UniProt id by the list index
        if len(fields) > 1:
            return fields[1]
        return ""


def get_kegg_orth(kegg_gene):
    """Return a list of KEGG orthology ko:KEGGiD pairs for the provided KEGG organism:gene pairs."""
    result = requests.get(
        f'https://rest.kegg.jp/link/ko/{kegg_gene}', timeout=5)
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)
        fields = str_entry.split("\t")
        # To avoid a complex 2D array, get the UniProt id by the list index
        if len(fields) > 1:
            return fields[1]
        return ""


def get_path_id(kegg_orth):
    """Return a list of KEGG :KEGGiD pairs for the provided KEGG orthology ko:KEGGiD pairs."""
    path_ids = []
    result = requests.get(
        f'https://rest.kegg.jp/link/pathway/{kegg_orth}', timeout=5)
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)
        fields = str_entry.split("\t")
        path_ids.append(fields[1])
    return path_ids[1::2]


def load_kegg_pathways():
    """Return all the KEGG pathways in a dictionary for user querying."""
    kegg_pathways = {}
    result = requests.get(
        'https://rest.kegg.jp/list/pathway/ko', timeout=5)
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)
        fields = str_entry.split("\t")
        kegg_pathways[fields[0]] = fields[1]
    return kegg_pathways


def get_path_dicts(uniprot_ids, kegg_orth, kegg_path_ids):
    """Return three dictionaries Uniprot: Path, Path: KO,and Path: Description."""
    pathways = load_kegg_pathways()
    desc_dict = {}
    id_desc = {}
    for i in range(len(kegg_path_ids)):
        for j in range(len(kegg_path_ids[i])):
            desc_dict[kegg_path_ids[i][j]] = pathways[kegg_path_ids[i][j]]
            id_desc[kegg_path_ids[i][j]] = kegg_orth[i]
    uniprot_ko = {uniprot_ids[i]: kegg_path_ids[i]
                  for i in range(len(uniprot_ids))}
    return (uniprot_ko, id_desc, desc_dict)


def add_kegg_pathways():
    """Main logic of business."""
    args = get_args()
    in_file = open(args.infile, "r", encoding='utf-8')
    # Use list comprehensions to store KEGG data
    uniprot_ids = [get_uniprot_id(blastline, args.evalue)
                   for blastline in in_file]
    kegg_gene = [get_kegg_genes(id)
                 for id in uniprot_ids]
    kegg_orth = [get_kegg_orth(gene)for gene in kegg_gene]
    kegg_path_ids = [get_path_id(orth) for orth in kegg_orth]

    # I noticed there were no path returns cases, so I need to check if there is
    # any path in return first in my program. Therefore, I made three dictionaries
    # KO: Path (1 to many), Path: Description (1:1), and Uniprot: Path (1 to many).
    # If a path is in there, then we access the rest of the values to file
    uniprot_ko, id_desc, desc_dict = get_path_dicts(
        uniprot_ids, kegg_orth, kegg_path_ids)
    in_file.seek(0)
    out_file = open(args.outfile, "a", encoding='utf-8')

    # Use Uniprot: Path (1 to many) as a boolean to check any path-associated value.
    # The other dictionaries are for querying values and append to file.
    for line in in_file:
        data = line.split("\t")
        if uniprot_ko[data[1]]:
            for path in uniprot_ko[data[1]]:
                new_lines = f"\t{id_desc[path]}\t{path}\t{desc_dict[path]}\n"
                out_file.write(line.rstrip()+new_lines)
        else:
            out_file.write(line)

    out_file.close()
    in_file.close()


if __name__ == "__main__":
    add_kegg_pathways()


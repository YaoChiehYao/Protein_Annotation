import pytest

from add_kegg_pathways import (get_uniprot_id, get_kegg_genes,
                               get_kegg_orth, get_path_id, load_kegg_pathways, get_path_dicts)

BLAST_LINE = "TRINITY_DN10002_c0_g1_i1.p1	Q5ZL74	125	220	124	46	37.097	5.34e-25	RecName: Full=Vesicle-associated membrane protein 7; AltName: Full=Synaptobrevin-like protein 1"
EVALUE = (10**-5)
UNIPROT_ID = ['Q5ZL74']
KEGG_ORTH = ['ko:K08515']
KEGG_PATH_ID = [['path:ko04130']]


def test_get_uniprot_id():
    """Get SwissProt from BLAST line"""
    assert get_uniprot_id(BLAST_LINE, EVALUE) == "Q5ZL74"


def test_get_kegg_genes():
    """Query gene data from KEGG gene"""
    assert get_kegg_genes("Q5ZL74") == "gga:422297"


def test_get_kegg_orth():
    """Query kegg orthology from KEGG ko"""
    assert get_kegg_orth("gga:422297") == "ko:K08515"


def test_get_path_id():
    """Query path id from KEGG pathways"""
    assert get_path_id("ko:K08515") == ["path:ko04130"]


def test_load_kegg_pathways():
    """Query pathway description from KEGG pathways"""
    assert load_kegg_pathways(
    )["path:ko04130"] == "SNARE interactions in vesicular transport"


def test_get_path_dicts():
    """Query pathway description from KEGG pathways"""
    assert get_path_dicts(UNIPROT_ID, KEGG_ORTH, KEGG_PATH_ID) == ({'Q5ZL74': ['path:ko04130']}, {
        'path:ko04130': 'ko:K08515'}, {'path:ko04130': 'SNARE interactions in vesicular transport'})


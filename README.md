
BINF 6308 Assignment 10

# Project name: KEGG Restful API application 


## Description

Assignment 10 demonstrates data acquisition by querying the KEGG
(Kyoto Encyclopedia of Genes and Genomes) database, and append back
to the original BLAST result as an annotation.


## Getting Started

* Hi, this is the documentation for assignment 10 of the bio-computational
  method course.
* That's start querying data from the KEGG database by understanding its 
  structure and sending simple requests to test via URL.
  https://www.kegg.jp/kegg/
* The working environment recommends the python IDE cooperate with the web
  browser (observe query result before coding) for requests and get data from
  the KEGG server.


### Dependencies

python 3.8


### Installing
 
Install the python3 request module by the following command:
pip3 install requests (MacOS) or 
pip install request (Windows)


### Executing program

* Use the python IDE to prepare function units in following steps:

* getUniProtFromBlast():
  This function uses SwissProt (6 characters) from the "alignPredicted.txt."
  file to query UniProt: Id from KEGG if the E-value is below the threshold.
  (1e-5) If not, this should instead return False and ignore that data.

* getKeggGenes():
  This function uses provided uniprot_id from the previous process and returns
  the querying result in a list of KEGG organism: gene pairs.

* getKeggOrthology():
  Same as the previous one, this function takes organism: gene pairs for 
  database querying and return a list of KEGG orthology ko: KEGGiD pairs.

* getKeggPathIDs():
  Again, we use the former result KEGG orthology ko: KEGGiD pairs for database
  query and return pathway_id pairs.

* loadKeggPathways():
  The functions collect all the KEGG pathway categories and its description as
  a dictionary and return them in dictionary format for the user to use key-value
  pairs querying.

* addKEGGPathways():
  Combine all the functions above and runs as the main script.


* In the end, make all functions into one python script.


  Here is the link of file: 
```
https://github.com/NU-Bioinformatics/module-10-YaoChiehYao.git
```

## Method

* KEGG ORTHOLOGY
 This project uses the KEGG database which provides multiple entry
 points for users to query data via Restful API architecture. 

 Here are the entry points used in this program:
   1.  KEGG PATHWAY      KEGG pathway maps
       https://rest.kegg.jp/link/pathway/

   2.  KEGG ORTHOLOGY    KO functional orthologs
       https://rest.kegg.jp/link/ko/

   3.  KEGG GENES        Genes and proteins
       https://rest.kegg.jp/conv/genes/
 
For more information, please refer to the official website of KEGG in the citations.


## Citations

  KEGG ORTHOLOGY
  1. Kanehisa Laboratories. 2022 "KEGG" KEGG official website
     https://www.kegg.jp/kegg/

  Python Request Module
  1. Kenneth Reitz.2022. "Requests: HTTP for Humans" requests website
     https://requests.readthedocs.io/en/

  2. Jason Van Schooneveld. 2022. "Python and REST APIs: Interacting With Web Services" Real Python
     https://realpython.com/api-integration-in-python/


## Help

Any other issue contact with yao.yao-@northeastern.edu


## Authors

Yao Chieh Yao
Northeastern University Bioinformatics


## Version History

* 1.0
    * Assignment01 Finish 
* 0.1
    * Assignment01 Release 


## License

This project is an assignment work and only license to TA and professors of Northeastern University Bioinformatics 


## Acknowledgments

Thanks to the Kanehisa Laboratories for their work on the KEGG database, this open-source database, tools, and
documentation are beneficial for bioinformaticians and interested users, and the python Request module developers
and maintainers team for the excellent means to access Restful API-based public data sources.

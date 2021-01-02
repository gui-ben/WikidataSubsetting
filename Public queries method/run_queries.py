#pip install sparqlwrapper
import argparse
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib, urllib
from rdflib import URIRef
import os
from run_1_query import run_query



def run_all_queries(format='nquads'):
    for root, dirs, files in os.walk("."):
        for file_name in files:
            if file_name.endswith(".sparql"):

                run_query(input_query_file_path=root, input_query_file_name=file_name,
                          output_file_path=os.path.join('Results', os.path.basename(root)),
                          output_file_name=file_name.split(".")[0],
                          output_format=format)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--format", help="Output format. Use 'ntriples' or 'nquads'. Default output value is n quads.", default='nquads')

    args = vars(parser.parse_args())
    run_all_queries(format=args['format'])

#pip install sparqlwrapper
import argparse
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib, urllib
from rdflib import URIRef
import os
from datetime import datetime

def run_query(endpointUrl='https://query.wikidata.org/sparql',
              named_graph_id='https://www.wikidata.org',
              output_format='nquads',
              input_query_file_path='.',
              input_query_file_name='query.sparql',
              output_file_path='.',
              output_file_name='query_results'):

    input_file = os.path.join(input_query_file_path, input_query_file_name)

    with open(input_file,'r') as file:
        query_string = file.read()

        print('Processing query: ' + os.path.join(input_query_file_path, input_query_file_name))
        itemGraph = rdflib.ConjunctiveGraph(store="IOMemory")
        start_time = datetime.now()
        url = endpointUrl + '?query=' + urllib.parse.quote(query_string)
        # rdflib retrieves the results, parses the triples, and adds them to the graph
        itemGraph.parse(source=url, publicID=named_graph_id)

        print('The query took: ' + str(datetime.now() - start_time))
        results = itemGraph.serialize(format=output_format).decode('utf-8')

        output_file_extention = 'nq' if output_format == 'nquads' else 'nt'
        output_file = os.path.join(output_file_path, output_file_name + "." + output_file_extention)
        os.makedirs(output_file_path, exist_ok=True)
        print('Saving query results in: ' + output_file)

        with open(output_file, 'w+') as output:
            output.write(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="Query file name. Default file name is 'query.sparql' located on this folder", default='query.sparql')
    parser.add_argument("-f", "--format", help="Output format. Use 'ntriples' or 'nquads'. Default output value is n quads.", default='nquads')
    parser.add_argument("-o", "--output", help="Output file name. Default value is query_results.nq", default='query_results')

    args = vars(parser.parse_args())

    input_path, input_filename = os.path.split(args['query'])

    run_query(input_query_file_path = input_path, input_query_file_name=input_filename,
              output_format=args['format'], output_file_name=args['output']) # Use output_format='nt' for ntriples

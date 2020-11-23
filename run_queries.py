#pip install sparqlwrapper

from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib, urllib
from rdflib import URIRef
import os


endpointUrl = 'https://query.wikidata.org/sparql'


for root, dirs, files in os.walk("."):
    for file_name in files:
        if file_name.endswith(".sparql"):
             with open(os.path.join(root, file_name),'r') as file:

                 print(os.path.join(root, file_name))
                 query_string = file.read()

                 print('processing query: ' + file_name)
                 itemGraph=rdflib.Graph()

                 url = endpointUrl + '?query=' + urllib.parse.quote(query_string)

                # rdflib retrieves the results, parses the triples, and adds them to the graph
                 result = itemGraph.parse(url)

                #my_ntriples = result.serialize(format='nt')
                 my_ntriples = result.serialize(format='nt').decode('utf-8')

                 print('saving file into: query results/' + file_name)

                 os.makedirs(os.path.join(root, 'query results', file_name), exist_ok=True)

                 with open(os.path.join(root, 'query results', file_name), 'w+') as output_file:
                    output_file.write(my_ntriples)

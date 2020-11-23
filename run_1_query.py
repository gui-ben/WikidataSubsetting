#pip install sparqlwrapper

from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib, urllib
from rdflib import URIRef
import os


endpointUrl = 'https://query.wikidata.org/sparql'


with open('query.sparql','r') as file:
    query_string = file.read()

    print('processing query')
    itemGraph=rdflib.Graph()

    url = endpointUrl + '?query=' + urllib.parse.quote(query_string)

    # rdflib retrieves the results, parses the triples, and adds them to the graph
    result = itemGraph.parse(url)

    #my_ntriples = result.serialize(format='nt')
    my_ntriples = result.serialize(format='nt').decode('utf-8')

    print('saving file into: query results')


    with open('output.nt', 'w+') as output_file:
        output_file.write(my_ntriples)

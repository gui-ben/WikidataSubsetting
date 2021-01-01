#pip install sparqlwrapper

from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib, urllib
from rdflib import URIRef
import os
from datetime import datetime



endpointUrl = 'https://query.wikidata.org/sparql'
named_graph_id = 'https://www.wikidata.org'

with open('query.sparql','r') as file:
    query_string = file.read()

    print('processing query')
    itemGraph=rdflib.ConjunctiveGraph(store="IOMemory")

    start_time = datetime.now()

    url = endpointUrl + '?query=' + urllib.parse.quote(query_string)

    # rdflib retrieves the results, parses the triples, and adds them to the graph
    itemGraph.parse(source=url, publicID=named_graph_id)

    print('the query took: ' + str(datetime.now() - start_time))


    #my_ntriples = result.serialize(format='nt')
    my_ntriples = itemGraph.serialize(format='nquads').decode('utf-8')

    print('saving file into: query results')


    with open('output.nq', 'w+') as output_file:
        output_file.write(my_ntriples)

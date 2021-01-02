#pip install sparqlwrapper

from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib, urllib
from rdflib import URIRef
import os
import re
import sys


# try:
#     entity_id = sys.argv[1]
# except IndexError:
#     print('You have to specify an entity id as argument for the script! For example: python3 get_subtypes.py Q12136')
#     sys.exit()

sparql = SPARQLWrapper('https://query.wikidata.org/sparql')


types_list = ['Q8054', 'Q423026', 'Q4936952', 'Q616005', 'Q4915012', 'Q2996394', 'Q5058355', 'Q11173', 'Q37748', 'Q12136', 'Q7187', 'Q3271540', 'Q12140', 'Q14860489', 'Q28885102', 'Q50377224', 'Q898273', 'Q417841', 'Q215980', 'Q15304597', 'Q3273544', 'Q7644128', 'Q169872', 'Q16521', 'Q50379781']
#reduced_types_list = ['Q8054', 'Q423026', 'Q4936952', 'Q616005', 'Q4915012', 'Q5058355', 'Q37748', 'Q12136', 'Q3271540', 'Q12140', 'Q14860489', 'Q28885102', 'Q50377224', 'Q898273', 'Q417841', 'Q215980', 'Q15304597', 'Q3273544', 'Q7644128', 'Q169872', 'Q50379781']


results_set = set()


for entity_id in reduced_types_list:
    print('Processing type: ' + entity_id)

    query_string = '''SELECT DISTINCT ?instance_of
    WHERE {{
      ?item wdt:P31/wdt:P279* wd:{type_id}.
      minus {{?item wdt:P31|wdt:P279 wd:{type_id}}}
      ?item wdt:P31 ?instance_of.
      SERVICE wikibase:label {{bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".}}
    }}
    '''.format(type_id=entity_id)

    query_string_2 = '''SELECT DISTINCT ?instance_of
    WHERE {{
      ?item wdt:P31* wd:{type_id}.
      minus {{?item wdt:P31|wdt:P279 wd:{type_id}}}
      ?item wdt:P31 ?instance_of.
      SERVICE wikibase:label {{bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".}}
    }}
    '''.format(type_id=entity_id)

    queries_list = [query_string, query_string_2]

    for query in queries_list:
        try:
            sparql.setQuery(query_string)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            break
        except:
            print('Query failed. Trying next query')

    print('Query finished!')

    for result in results['results']['bindings']:
        result_wikidata_id = re.sub('.*\/', '', result['instance_of']['value'])
        results_set.add(result_wikidata_id)


with open('types_ids.txt', 'w') as output_file:
    for type in results_set:
        output_file.write(type + '\n')

print('Size: ' + str(len(results_set)))

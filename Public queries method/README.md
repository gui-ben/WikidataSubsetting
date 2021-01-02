# Using CONSTRUCT queries to create a Wikidata subset

Here you can see how you can create a Wikidata subset by running [CONSTRUCT](https://www.w3.org/TR/rdf-sparql-query/#construct) queries on the [public Wikidata endpoint](https://query.wikidata.org/).

With CONSTRUCT queries, we created a life sciences Wikidata subset using as a guide [this graph](https://upload.wikimedia.org/wikipedia/commons/b/b9/Biomedical_Knowledge_Graph_in_Wikidata.svg) from [this paper](https://elifesciences.org/articles/52614).

## Contents

On this folder you will find:
* [A Python script to run one query on the Wikidata public endpoint](https://github.com/ingmrb/WikidataSubsetting/blob/main/run_1_query.py)
* [A Python script to run all queries on the repo](https://github.com/ingmrb/WikidataSubsetting/blob/main/run_queries.py)
* Two folders containing two set of queries. One folder with queries creating a subset using Wikidata types and one folder with queries that create a new graph using [Bioschemas](https://bioschemas.org/) types and properties whenever possible.


## Results
You can download a zip containing the Bioschemas subset as [nquads](https://www.en.wikipedia.org/wiki/Named_graph) on [this link](https://www.storage.googleapis.com/subsets_bucket/Wikidata_n_quads.zip) (queries ran on December 2020).


## Why are the queries the way they are?

The queries have the following structure:
```sparql
PREFIX schema: <https://schema.org/>
PREFIX wikibase: <http://wikiba.se/ontology#>

CONSTRUCT {
?disease a schema:MedicalCondition.
?disease schema:signOrSymptom ?symptoms.  
?disease wdt:P828 ?taxon.
?disease wdt:P2293 ?associated_gene.
?disease schema:associatedAnatomy ?anatomical_location.
?disease schema:drug ?drug_used_for_treatment.
}

WHERE {
{?disease wdt:P31/wdt:P279* wd:Q12136.} # Instance of or subclass of Disease.
UNION {?disease wdt:P31/wdt:P279* wd:Q12136. ?disease wdt:P780 ?symptoms.}
UNION {?disease wdt:P31/wdt:P279* wd:Q12136. ?disease wdt:P828 ?taxon.}
UNION {?disease wdt:P31/wdt:P279* wd:Q12136. ?disease wdt:P2293 ?associated_gene.}
UNION {?disease wdt:P31/wdt:P279* wd:Q12136. ?disease wdt:P927 ?anatomical_location.}
UNION {?disease wdt:P31/wdt:P279* wd:Q12136. ?disease wdt:P2176 ?drug_used_for_treatment.}
SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
}
```
The CONSTRUCT part corresponds to the new graph we are generating. In the Wikidata queries where we create a pure Wikidata subset, each statetment will be equal to it's correponding statement one on the WHERE clause. In the queries where we enriched the data with Schema.org properties, we tried to use Schemas whenever possible, but, as there isn't a 1:1 mapping between Wikidata and Schema.org properties, in some cases the subset resulting from that query will be a hybrid with both Schemas and Wikidata properties, as you can see on this example.

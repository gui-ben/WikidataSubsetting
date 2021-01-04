# How to create a Wikidata subset

## What is Wikidata and why would I want a subset of it?

[Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) is a collaboratively edited knowledge graph hosted by the Wikimedia Fundation.

There are several reason why you might want to create a subset, as documented on [this report from the 12th SWAT4HCLS conference](https://www.wikidata.org/wiki/Wikidata:WikiProject_Schemas/Subsetting#Rationales).

We could enumerate two main reasons:
1. Wikidata is getting bigger each year. This means that the same query gets more computationally expensive as time goes by and more data is added to the graph. Maybe a query that runs fine on the [public Wikidata endpoint](https://query.wikidata.org/) today, will timeout in the future and, as a consequence, will not get you any results (unless you modify it someway or put a [LIMIT](https://www.w3.org/TR/rdf-sparql-query/#modResultLimit) to at least get some partial results). In the same way, if you are running your own copy of Wikidata, locally or in a Cloud, each year you will need more space (i.e., money) to host it than the year before.


2. Data normalization. If you have your subset, you can normalize the data to other representations or [schemas](https://schema.org/), in order to make it easier to integrate with external data that doesn't use the same representation as Wikidata.


## (Some) methods to create a subset

There are countless possible ways to create a Wikidata subset. We will look into just three particular ways:

### 1. Running CONSTRUCT queries on the public Wikidata endpoint

A [CONSTRUCT](https://www.w3.org/TR/rdf-sparql-query/#construct) query will allow us to create a new RDF graph from Wikidata. We can run these type of queries in the public endpoint. This method may be the first idea that comes to your mind, and probably the first one you should try.


### Pros
* Cheap (most likely free).
You don't need more extra space than the disk space that the resulting subset will take.

* Fast.
Each query either runs in a few minutes or don't.

### Cons
* It's very likely that you will run into queries that timeout. Depending on your usecase, you could then modify the queries to fetch less results. In that case, the resulting graph will be a **partial subset** of Wikidata. If you need a complete subset, you'll have to use some other method.


### 2. Get a Wikidata dump and load it into a triplestore

For this method you can follow [@addshore](https://www.github.com/addshore)'s tutorial called [Your own Wikidata Query Service, with no limits](https://addshore.com/2019/10/your-own-wikidata-query-service-with-no-limits/). After you have your own copy of Wikidata loaded into a triplestore, you can run the same CONSTRUCT queries that you tried on the public endpoint before.

### Pros
* The resulting subset will be a complete Wikidata subset.

### Cons
* Expensive.
As of December 2020, a compressed version of all entities in Wikidata is ~90 GB. Uncompressed is ~1 TB.

* Slow.
The data will take about 1TB of disk space, but then you will have to load all of it into a triplestore of your choice, like [Blazegraph](https://www.blazegraph.com/). This process, on a standard Google Cloud VM configuration like the one used on [@addshore](https://www.github.com/addshore)'s tutorial, at the time of writing, takes around 10 days.


### 3. Get a Wikidata dump, filter it with Wdumper, and load it into a triplestore

You can think of method as the same as the previous one, but with an extra step: [Wdumper](https://www.github.com/bennofs/wdumper). Wdumper is a tool that allow us to filter Wikidata dumps. This program takes as input a [JSON spec](https://github.com/bennofs/wdumper/blob/master/examples/humans.json) where you have to specify the characteristics of the items you want to fetch. Then, the tool does one pass over the Wikidata dump, iterating item by item, and checks if the current element should be included in the resulting dump, based on the given JSON spec.


### Pros
* Cheaper than loading a whole Wikidata dump into a triplestore
You will not be loading into your triplestore a whole Wikidata dump, but the filtered dump from Wdumper, which will very likely take only a fraction of a whole Wikidata dump.

* Faster than loading a whole Wikidata dump into a triplestore
At the time of writing, on a laptop with a 4th generation Intel Core i7 processor, Wdumper takes around 9 hours to iterate over a current Wikidata dump. It can take a bit longer if you use as input a large JSON spec. Then you have to add the time the Wdumper subset will take to load into a triple store, which varies according to the size of the Wdumper dump.

### Cons

* You could end up with a partial subset.
Wdumper works by iterating item by item, in one pass. For each item, it checks if it conforms the input JSON spec or not. For example, let's say that we want to create a subset with all intances of [diseases](https://www.wikidata.org/wiki/Q12136) present in Wikidata. We would then, in the JSON spec, express that we want to fetch all items that appear as an instance of disease. The problem we could run into is that some diseases might appear as an instance of [rare disease](https://www.wikidata.org/wiki/Q929833) or [lung disease](https://www.wikidata.org/wiki/Q3392853), but not as instance of disease, as you can see on this [Wikidata query](https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fitem%20%3FitemLabel%0A%20%20%20%20WHERE%20%7B%0A%20%20%20%20%20%20%3Fitem%20wdt%3AP31%2a%20wd%3AQ12136.%0A%20%20%20%20%20%20minus%20%7B%3Fitem%20wdt%3AP31%7Cwdt%3AP279%20wd%3AQ12136%7D%0A%20%20%20%20%20%20%3Fitem%20wdt%3AP31%20%3Finstance_of.%0A%20%20%20%20%20%20SERVICE%20wikibase%3Alabel%20%7Bbd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%7D%0A%20%20%20%20%7D).
To solve this, we can run a query on the public endpoint for each type we want to filter, such that we can get a list of all the 'subtypes' corresponding to the type we are interested in. In our case, we could in the end express in the input JSON that we want not only all items that appear as an instance of disease, but also as an instance of rare disease, pulmonary disease, etc.
We can end up with a partial subset because to get all the possible 'subtypes' we need to run a query on the public endpoint, and therefore, it could timeout. It's a bit of an edge case, but it's a possible scenario.

* I could be slow or expensive
On Wdumper you can not fetch only certain properties of items you are interested in. If a Wikidata item should be added to the output dump, according to the JSON spec, then the item will be added as a whole. This means that your Wdumper dump could contain too much extra information. So, loading it into a triplestore can still be quite time consuming or expensive.


## Examples

You can find examples of how to create Wikidata subsets with methods 1 and 3 on the corresponding folders of this repo.


## Conclusion

We only explored some possible ways of creating Wikidata subsets. There's no "one size fits all" solution to this problem, at least at the time of writing. There are different approaches that work for different use cases.

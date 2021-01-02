# Using Wdumper to create a Wikidata subset

Here you can see how you can create a Wikidata subset with [Wdumper](https://github.com/bennofs/wdumper) from your terminal.

Our goal was to created a life sciences Wikidata subset, based on [this graph](https://upload.wikimedia.org/wikipedia/commons/b/b9/Biomedical_Knowledge_Graph_in_Wikidata.svg) from [this paper](https://elifesciences.org/articles/52614).

## Contents
* Bash script to run Wdumper via Docker.
* Python script to run queries to get a list of subtypes for a given Wikidata type.
* Python script to create input a Wdumper JSON file for a given list of Wikidata types.

You might also find handy [this 2014 Wikidata dump (3.5GB)](https://drive.google.com/file/d/1JeowPytImF08kch7RJ71g7sHhbPn93MQ/view?usp=sharing), since it's considerably lighter than a current dump. You can use it to test your input JSON file without having to run Wdumper on a current dump, which would take much longer.


The easiest way to run Wdumper is via Docker. Running Wdumper that way will place the output dump on the root folder of the Docker container [(link to the Github issue)](https://github.com/bennofs/wdumper/issues/27) and you will have to extract it from there manually. To get around this, you can use the bash script located on this folder. Place the script inside the Wdumper folder and run: `./run_wdumper.sh your_wikidata_dump.json.gz your_input_spec.json`
This script will run Wdumper from docker and place the Wdumper dump on the same folder where you are located.

## Results

[Life sciences subset (extracted from December 2020 Wikidata dump)](https://drive.google.com/file/d/1lrplgEYOlHZI7cSLd9FUgvll9Q-XwoKz/view?usp=sharing)

# Example: ./run_wdumper.sh minidump.json.gz gene.json
docker run -v ~/wdumper:/my_data/ --name wdumper wdumper_test:0.1  /my_data/$1 /my_data/$2
docker cp wdumper:/wdump-1.nt.gz .
docker rm wdumper
#rm wdump-1.nt
#gunzip wdump-1.nt.gz

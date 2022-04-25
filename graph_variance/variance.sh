#!/bin/bash

C=0.05

ID=star

GRAPH_FILE=graphs/$ID.txt

if [[ ! -f $GRAPH_FILE ]]; then
	echo -e "graph file not found"
	exit;
fi

OUTPUT_FILE=star_uni_s005/${1}.txt

NUM_RUNS=10000

DIST="uniform"

FIT_ADV=0.5

for i in {0..99}
do
	param=$(echo "scale=4;$C*$i" |bc)
	FIT_VAR=$param
	
	BASE_FIT=5

	./sim.out $GRAPH_FILE $OUTPUT_FILE $NUM_RUNS $DIST $BASE_FIT $FIT_ADV $FIT_VAR 
done


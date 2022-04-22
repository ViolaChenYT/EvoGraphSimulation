#!/bin/bash

C=0.05

ID=star

GRAPH_FILE=graphs/$ID.txt

if [[ ! -f $GRAPH_FILE ]]; then
	echo -e "graph file not found"
	exit;
fi

OUTPUT_FILE=results/${FIT_VAR}.txt

NUM_RUNS=100000

DIST="poisson"

FIT_ADV=0.05


for i in {0..99}
do
	param=$(echo "scale=4;$C*$i" |bc)
	FIT_VAR=$param
	
	BASE_FIT=$param

	./sim.out $GRAPH_FILE $OUTPUT_FILE $NUM_RUNS $DIST $BASE_FIT $FIT_ADV $FIT_VAR >> poisson_variance_star.txt 
done


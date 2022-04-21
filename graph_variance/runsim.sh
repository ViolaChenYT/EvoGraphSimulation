#!/bin/bash

#echo -e "input format: graph_file | num_runs | fitness(float) | var in fitness ...\n"
g++ -o sim.out -w Evograph.cpp

ID=$1
GRAPH_FILE=graphs/$ID.txt
if [[ ! -f $GRAPH_FILE ]]; then
	echo -e "graph file not found"
	exit;
fi
FIT_VAR=${5:-1}
OUTPUT_FILE=results/${FIT_VAR}.txt
NUM_RUNS=${2:-1000}
BASE_FIT=${3:-10}
FIT_ADV=${4:-0}


./sim.out $GRAPH_FILE $OUTPUT_FILE $NUM_RUNS $BASE_FIT $FIT_ADV $FIT_VAR
# eg. ./runsim.sh wellmixed 10000 5
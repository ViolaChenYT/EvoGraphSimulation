#!/bin/bash

#echo -e "input format: graph_file | num_runs | fitness(float) | var in fitness ...\n"
g++ -std=c++11 -o sim.out -w Evograph.cpp

ID=$1
GRAPH_FILE=graphs/$ID.txt
if [[ ! -f $GRAPH_FILE ]]; then
	echo -e "graph file not found"
	exit;
fi
FIT_VAR=${6:-1}
NUM_RUNS=${2:-1000}
DIST=${3:-"uniform"}
BASE_FIT=${4:-10}
FIT_ADV=${5:-0}
OUTPUT_FILE=${ID}_${DIST}_${FIT_ADV}.txt


./sim.out $GRAPH_FILE $OUTPUT_FILE $NUM_RUNS $DIST $BASE_FIT $FIT_ADV $FIT_VAR
# eg. ./runsim.sh wellmixed 10000 5

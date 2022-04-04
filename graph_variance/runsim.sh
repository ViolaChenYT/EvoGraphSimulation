#!/bin/bash

echo -e "input format: num_runs | fitness(float) | alternative fitness ...\n"

g++ -o sim.out -w Evograph.cpp

ID=0
GRAPH_FILE=graphs/$ID.txt
OUTPUT_FILE=results/$ID.txt
NUM_RUNS=${1:-1}
FIT_ADV=${2:-0.1}

./sim.out $GRAPH_FILE $OUTPUT_FILE $NUM_RUNS $FIT_ADV

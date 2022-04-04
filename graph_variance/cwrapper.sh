#!/bin/bash

i=$1
i=$((i+1))
x=$(sed "${i}q;d" parameters.in | awk '{print $1}')
y=$(sed "${i}q;d" parameters.in | awk '{print $2}')

# original: 20000 runs
./main $x $y 1000 0.01 0.05 0.1


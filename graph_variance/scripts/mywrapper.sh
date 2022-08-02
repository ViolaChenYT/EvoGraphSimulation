#!/bin/bash

i=$1
i=$((i+1))
x=$(sed "${i}q;d" param.in | awk '{print $1}')
y=$(sed "${i}q;d" param.in | awk '{print $2}')

# original: 20000 runs
./sim.out $x $y 20000 0.1


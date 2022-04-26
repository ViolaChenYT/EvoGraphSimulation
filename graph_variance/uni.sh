#!/bin/bash

i=$1
i=$((i+1))
x=$(sed "${i}q;d" param.in | awk '{print $1}')
# y=$(sed "${i}q;d" param.in | awk '{print $2}')

model=star
dist=uniform
s=0.05

# original: 20000 runs
./sim.out "graphs/${model}.txt" $x 5000 $dist 5 $s 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9 3.0 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8 3.9 4.0 4.1 4.2 4.3 4.4 4.5 4.6 4.7 4.8 4.9 5.0


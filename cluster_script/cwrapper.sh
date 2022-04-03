#!/bin/bash

i=$1
i=$((i+1))
x=$(sed "${i}q;d" parameters.in | awk '{print $1}')
y=$(sed "${i}q;d" parameters.in | awk '{print $2}')

./main $x $y 200000 0.01 0.05 0.1


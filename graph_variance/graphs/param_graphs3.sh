#!/bin/bash
i=$1
i=$((i+1))
x=$(sed "${i}q;d" param_graphs3.param.in | awk '{print $1}')
y=$(sed "${i}q;d" param_graphs3.param.in | awk '{print $2}')
dist=binom
./gph $x $y 100000 $dist 0.25 0.0 0.01 0.02 0.03 0.05 0.07 0.08 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9

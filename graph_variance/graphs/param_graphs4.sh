#!/bin/bash
i=$1
i=$((i+1))
x=$(sed "${i}q;d" param_graphs4.param.in | awk '{print $1}')
y=$(sed "${i}q;d" param_graphs4.param.in | awk '{print $2}')
dist=binom
./gph $x $y 200000 $dist 0.1 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9

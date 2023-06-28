#!/bin/bash
i=$1
i=$((i+1))
x=$(sed "${i}q;d" param_graphs4.param.in | awk '{print $1}')
y=$(sed "${i}q;d" param_graphs4.param.in | awk '{print $2}')
dist=binom
./gph $x $y 250000 $dist 0.001 0.0 0.316 0.447 0.548 0.632 0.707 0.775 0.837 0.894 0.949

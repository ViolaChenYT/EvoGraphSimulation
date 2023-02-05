#!/bin/bash
i=$1
i=$((i+1))
x=$(sed "${i}q;d" param_graph_neg5.param.in | awk '{print $1}')
y=$(sed "${i}q;d" param_graph_neg5.param.in | awk '{print $2}')
dist=binom
./gph1 $x $y 100000 $dist 0.1 0.0 0.9

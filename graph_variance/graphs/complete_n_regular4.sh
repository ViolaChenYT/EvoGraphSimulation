#!/bin/bash
i=$1
i=$((i+1))
x=$(sed "${i}q;d" complete_n_regular4.param.in | awk '{print $1}')
y=$(sed "${i}q;d" complete_n_regular4.param.in | awk '{print $2}')
dist=binom
./gph.out $x $y 100000 $dist 0.1 0.0 0.9

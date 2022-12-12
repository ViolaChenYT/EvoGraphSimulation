#!/bin/bash
i=$1
i=$((i+1))
x=$(sed "${i}q;d" pop_size_10_reg1.param.in | awk '{print $1}')
y=$(sed "${i}q;d" pop_size_10_reg1.param.in | awk '{print $2}')
dist=binom
./gph $x $y 1000000 $dist 0.1 0.0 0.9

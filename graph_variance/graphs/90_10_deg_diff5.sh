#!/bin/bash
i=$1
i=$((i+1))
x=$(sed "${i}q;d" 90_10_deg_diff5.param.in | awk '{print $1}')
y=$(sed "${i}q;d" 90_10_deg_diff5.param.in | awk '{print $2}')
dist=binom
./gph.out $x $y 200000 $dist 0.1 0.0 0.9

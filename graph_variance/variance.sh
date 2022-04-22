#!/bin/bash

C=0.05

for i in {0..99}
do
	param=$(echo "scale=4;$C*$i" |bc)
	./runsim.sh star 80000 "binom" 5 0.05 $param >> ./results/binom_variance_star.txt
done


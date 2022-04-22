#!/bin/bash

C=0.05

for i in {1..100}
do
	param=$(echo "scale=4;$C*$i" |bc)
	./runsim.sh star 10000 "binom" 5 0 $param >> ./results/star_binom_var.txt
done

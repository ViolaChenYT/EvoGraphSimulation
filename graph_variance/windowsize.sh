#!/bin/bash

C=0.05

for i in {1..100}
do
	param=$(echo "scale=4;$C*$i" |bc)
	./runsim.sh wellmixed 80000 "uniform" $param 0.05 $param >> ./results/cmp_poisson.txt
done

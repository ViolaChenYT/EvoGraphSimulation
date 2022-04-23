#!/bin/bash

C=0.05

for i in {0..99}
do
	param=$(echo "scale=4;$C*$i" |bc)
	for j in {1..100}
	do
		./runsim.sh wellmixed 10000 "uniform" 5 0.1 $param >> ./wellmixed_uni_s01/${j}.txt
	done
done

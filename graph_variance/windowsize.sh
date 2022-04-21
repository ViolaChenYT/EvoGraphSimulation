#!/bin/bash

C=0.05

for i in {1..100}
do
	param=$(echo "scale=4;$C*$i" |bc)
	./runsim.sh wellmixed 50000 1 $param 0.05 >> ./results/wellmixed_diffs_var0.05.txt
done

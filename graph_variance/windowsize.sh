#!/bin/bash

C=0.05

for i in {0..99}
do
	param=$(echo "scale=4;$C*$i" |bc)
	./runsim.sh wellmixed 50000 1 $param 0.1 >> ./results/wellmixed_diffs_var.1.txt
done

#!/bin/bash

for i in {1..50}
do
	./runsim.sh star 50000 $i >> ./results/star_window.txt
done

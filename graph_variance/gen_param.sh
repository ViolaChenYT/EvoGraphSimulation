#!/bin/bash
dirname=$1
for i in {1..500}
do
	echo "${dirname}/${i}.txt" >> param.in
done

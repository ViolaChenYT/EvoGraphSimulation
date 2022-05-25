#!/bin/bash
model=$1
dirname=$2
echo "" > ${model}param.in
for i in {1..500}
do
	echo "mean1/${dirname}/${i}.txt" >> params/${model}param.in
done

#!/bin/bash
model=$1
dirname=$2
echo "" > ${model}_param.in
for i in {1..500}
do
	echo "mean1/${dirname}/${i}.txt" >> ${model}_param.in
done

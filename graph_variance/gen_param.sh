#!/bin/bash
model=$1
echo "" > ${model}_param.in
for i in {1..5000}
do
	echo "${model}/${i}.txt" >> ${model}_param.in
done

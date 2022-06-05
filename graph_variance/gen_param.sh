#!/bin/bash
model=$1
echo "" > ${model}_param.in
for i in {1..8000}
do
	res=$(((i-1)%800))
	echo "param_graphs/$res.txt   ${model}_result1/${i}.txt" >> ${model}_param.in
	# echo "${model}/${i}.txt" >> ${model}_param.in
done

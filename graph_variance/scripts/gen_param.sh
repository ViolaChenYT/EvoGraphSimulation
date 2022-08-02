#!/bin/bash
model=$1
echo "" > ${model}_param.in
if [[ "$1" == "graph_all" ]]; then
for i in {1..7350}
do
	res=$((i-1))
	pa=150
	regx4=950
	if [ $res -lt $pa ]; then
		id=$((res+250))
		echo "graphs/pa_graphs/$id.txt   graphall_result/pa/${i}.txt" >> ${model}_param.in
	elif [ $res -lt $regx4 ]; then
		id=$((res-150))
		echo "graphs/regx4_graphs/$id.txt   graphall_result/regx4/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 1750 ]; then
		id=$((res-950))
		echo "graphs/fam_graphs/$id.txt   graphall_result/fam/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 2150 ]; then
		id=$((res-1750))
		echo "graphs/assorted_graphs/$id.txt   graphall_result/assort/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 2550 ]; then
		id=$((res-2150))
		echo "graphs/20_3_graphs/$id.txt   graphall_result/20_3/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 3350 ]; then
		id=$((res-2550))
		echo "graphs/mv_graphs/$id.txt   graphall_result/mv/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 4150 ]; then
		id=$((res-3350))
		echo "graphs/complex_graphs/$id.txt   graphall_result/complex/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 4950 ]; then
		id=$((res-4150))
		echo "graphs/isl0_graphs/$id.txt   graphall_result/isl0/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 5750 ]; then
		id=$((res-4950))
		echo "graphs/isl1_graphs/$id.txt   graphall_result/isl1/${id}.txt" >> ${model}_param.in
	elif [ $res -lt 6550 ]; then
		id=$((res-5750))
		echo "graphs/isl2_graphs/$id.txt   graphall_result/isl2/${id}.txt" >> ${model}_param.in
	else
		id=$((res-6550))
		echo "graphs/isl3_graphs/$id.txt   graphall_result/isl3/${id}.txt" >> ${model}_param.in
	fi
done
fi
if [[ "$model" == "wheel" ]]; then
	for i in {1..100}
	do
		echo "wheel.txt   wheel_result/$((i-1))" >> ${model}_param.in
	done
fi
if [[ "$model" == "skew" ]]; then
	for i in {1..100}
	do 
		echo "graphs/wellmixed.txt   skew_result/$((i-1)).txt" >> ${model}_param.in
	done 
	for i in {101..200}
	do 
		echo "graphs/3reg.txt   skew_result/$((i-1)).txt" >> ${model}_param.in
	done
	for i in {201..300}
	do 
		echo "wheel.txt   skew_result/$((i-1)).txt" >> ${model}_param.in
	done
fi
# echo "${model}/${i}.txt" >> ${model}_param.in

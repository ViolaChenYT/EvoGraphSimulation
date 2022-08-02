#!/bin/bash

# for i in {1..100}
# do
#	f=./star_uni_s0/${i}.txt
#	line=`head -1 $f`
#	thing=`cut -f3 line`
#	echo $thing
# done
id=$1
mv star_uni_s0/${1}.txt star_uni_s005/${1}.txt

#!/bin/bash

i=$1
i=$((i+1))
x=$(sed "${i}q;d" parameters.in | awk '{print $1}')
y=$(sed "${i}q;d" parameters.in | awk '{print $2}')

# original: 20000 runs
<<<<<<< HEAD
./sim.out $x $y 20000 0.1
=======
./sim.out $x $y 1000 0.1
>>>>>>> 88c6e0500ad9e1fffbbcfc39fbdb0001783e0932


#!/bin/sh

for a in returns steps policy; do
    echo $a...
    ./graph.py $a $*;
done


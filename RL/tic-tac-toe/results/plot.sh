#!/bin/bash
#
# Bootstrap script for plot.gnuplot
#
# Usage: plot.sh <datafile> [title]
#

if [ -z "$1" ]; then
    echo "Usage: $0 <datafile> [title]" 1>&2
    exit 1
fi

datafile=$1
shift

title=$*

if [ -z "$title" ]; then
    title=${datafile%.*}
fi

echo -e "datafile='$datafile'\ntitle='$title'" | gnuplot -persist - plot.gnuplot

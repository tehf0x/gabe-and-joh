#
# gnuplot script for creating the graphs!
# 
# Run like this: gnuplot -persist plot.gnuplot
#

# Input data file
datafile = "first_free_2009-08-21_17:40:23.dat"

# Uncomment these two lines to output to PNG
# set terminal png
# set output "first_free_2009-08-20_17:45:10.png"

# Title of the plot
set title "First Free Environment" font "Arial Bold,18"

# Labels for x and y axis
set xlabel "Plays"
set ylabel "Average reward (%)"

# Set ranges
set yrange [0:1]

# Don't show key
set key off

# Draw only the left and bottom borders:
set border 11

set xtics nomirror
set grid ytics

# Plot!
plot datafile every 10 lt rgb "#008800" lw 3 pt 6 with linespoints

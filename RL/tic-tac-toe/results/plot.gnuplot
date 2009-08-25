#
# gnuplot script for creating the graphs!
# 
# NB: Do not run this file directly! Use plot.sh instead.
#
# plot.sh sets the variables datafile and title
#

# Uncomment these two lines to output to SVG
#set terminal svg enhanced
#set output "first_free_2009-08-24_16:53:12.svg"

# Title of the plot
set title title font "Arial Bold,18"

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


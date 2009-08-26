#
# gnuplot script for creating the graphs!
# 
# NB: Do not run this file directly! Use plot.sh instead.
#
# plot.sh sets the variables datafile and title
#
title = 'Simple Training'
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
set key inside right center 

# Draw only the left and bottom borders:
set border 11

set xtics nomirror
set grid ytics

# Plot!
plot 'first_free_2009-08-25_17:41:17.dat' every 10 lt rgb "#880000" lw 3 pt 6 with linespoints title 'First Free', 'random_2009-08-25_17:49:34.dat' every 10 lt rgb "#008800" lw 3 pt 6 with linespoints title 'Random', 'minimax_2009-08-25_22:38:14.dat' every 10 lt rgb "#000088" lw 3 pt 6 with linespoints title 'MiniMax'


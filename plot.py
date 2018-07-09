#!/usr/bin/python3
import json
import sys
import os
import time

from numpy import *
import Gnuplot, Gnuplot.funcutils

# g = Gnuplot.Gnuplot(debug=1)
g = Gnuplot.Gnuplot()

class gnuplot():
    
    def __init__(self):
        
        g.title('A simple example') # (optional)
        # g('set style data linespoints') # give gnuplot an arbitrary command
        # g('set xdata time')
        # g('set timefmt "%H:%M:%S" ')
        g('set autoscale y')
        # g('set xrange ["16:25":"17:00"]')
        g('set grid')


    def plot(self):
        g.plot("'test.txt' using 1 with line, 'points.txt' using 1:2, 'sell_points.txt' using 1:2,")

    
def main():
    plot = gnuplot()
    while 1:
        plot.plot()

    #     print(ram.get_ram_price(simulate))

        time.sleep(1)

if __name__ == "__main__":
    main()
        

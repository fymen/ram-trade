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

    # def set_point(self, x, y)
    #     g("'set object circle at first " + str(x) + "," + str(y) + "radius char 0.5 fillstyle empty border lc rgb \'#aa1100\' lw 2'")
        
    def plot(self, plot):
        g.plot(plot)

    
def main():
    plot = gnuplot()
    while 1:
        plot.plot()

    #     print(ram.get_ram_price(simulate))

        time.sleep(1)

if __name__ == "__main__":
    main()
        

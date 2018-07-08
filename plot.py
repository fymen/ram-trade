#!/usr/bin/python3
import json
import sys
import os
import math
import time

from ram_op import *

from numpy import *
import Gnuplot, Gnuplot.funcutils


class plot():

    def __init__(self):
        g = Gnuplot.Gnuplot(debug=1)
        g.title('A simple example') # (optional)
        g('set style data linespoints') # give gnuplot an arbitrary command
        g('set xdata time')
        g('set timefmt "%H:%M:%S" ')
        g('set autoscale y')
        g('set xrange ["16:25":"17:00"]')
        g('set grid')


    def plot(self):
        g.plot("'test.txt' using 1:2")


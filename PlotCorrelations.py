#!/usr/bin/env python
# encoding: utf-8

from pylab import *
import sys


data = loadtxt(sys.argv[1])

ncols = data.shape[1]

for i in xrange(ncols):
    for j in xrange(ncols):
        if i > j:
            subplot(ncols, ncols, (i * ncols) + j + 1)

            data1 = data[:, i]
            data2 = data[:, j]

            plot(data1, data2, 'k,')

            gca().xaxis.set_major_formatter(NullFormatter())
            gca().yaxis.set_major_formatter(NullFormatter())



subplots_adjust(wspace=0, hspace=0)


show()

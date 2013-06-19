import pylab
import numpy as np
import sys

pylab.rcParams.update({'path.simplify' : False})
fig = pylab.figure()
ax = fig.add_subplot(111)

fn = sys.argv[1]

data = pylab.loadtxt(fn)

# data format:
# x-axis = time
# y-axis = individuals' fitness values
n_ind = data[:, 0].size
n_gen = data[0, :].size
min_fit, max_fit = data.min(), data.max()

print 'debug', n_ind, n_gen

for gen in xrange(n_gen):
#    print 'data[:, gen].size', data[:, gen].size
    ax.scatter(gen * np.ones(n_ind), data[:, gen])

ax.set_ylim((min_fit, max_fit))
pylab.legend()
pylab.show()

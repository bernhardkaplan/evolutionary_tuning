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

global_best_ind, global_best_fitness, global_best_gen = 0, -1000, 0
global_lowest_ind, global_lowest_fitness, global_lowest_gen = 0, 10**9, 0

for gen in xrange(n_gen):
#    print 'data[:, gen].size', data[:, gen].size
    ax.scatter(gen * np.ones(n_ind), data[:, gen])
    best_fitness = data[:, gen].max()
    best_ind = data[:, gen].argmax()
    lowest_fitness = data[:, gen].min()
    lowest_ind = data[:, gen].argmin()

    if best_fitness > global_best_fitness:
        global_best_ind, global_best_fitness, global_best_gen = best_ind, best_fitness, gen
    if lowest_fitness < global_lowest_fitness:
        global_lowest_ind, global_lowest_fitness, global_lowest_gen = lowest_ind, lowest_fitness, gen
#    print 'Fittest individual in gen %d is ind %d' % (gen, best_ind), 'Results/fx_%d_%d.dat' % (gen, best_ind)

print 'Fittest individual of all gen is ind %d with fitness %.3e in gen %d' % (global_best_ind, global_best_fitness, global_best_gen), 'Results/fx_%d_%d.dat' % (global_best_gen, global_best_ind)
print 'Individual of all gen with lowest fitness is ind %d with fitness %.3e in gen %d' % (global_lowest_ind, global_lowest_fitness, global_lowest_gen), 'Results/fx_%d_%d.dat' % (global_lowest_gen, global_lowest_ind)


ax.set_ylim((min_fit, max_fit))
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')

pylab.legend()
pylab.show()

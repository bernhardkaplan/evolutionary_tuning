"""
Plot the function as defined in example.py my_fitness
with the parameters given in a file (after having run example.py)
"""
import pylab
import numpy as np
import json
import sys
from example import my_fitness


#fn = 'Results/params_gen99.prm'
fn = sys.argv[1]
print 'fn', fn
f = file(fn, 'r')
individuals = json.load(f)
#print 'debug', individuals 
#exit(1)

n_individuals = len(individuals)
n_plot = 5
print 'Individuals:', individuals[0]
plot_individuals = individuals[:5]

x_start = 0
x_stop = 20.
n_x = 1000.
dx = (x_stop - x_start) / n_x
x = np.arange(x_start, x_stop, dx)

MF = my_fitness({})
MF.set_fitness_function(x, save_target_function=False)

fig = pylab.figure()
ax = fig.add_subplot(111)

fitness_values = np.zeros(n_individuals)
for i_, p in enumerate(individuals):
    a = p['a']
    b = p['b']
    c = p['c']
    d = p['d']
    e = p['e']
    f = p['f']
    f_x = x * np.exp(np.sin(a * x + b)) * np.cos(c * x + d) * e + f
    fitness_values[i_] = MF.get_fitness(f_x)

sorted_idx = np.argsort(fitness_values)
print 'best fitness:', fitness_values[sorted_idx[-n_plot:]]
best_individuals = sorted_idx[-n_plot:]
print 'best_individuals:', best_individuals
#print individuals[np.array([1, 2, 3])]
#print 'debug', individuals[best_individuals]

for idx in best_individuals:
    print 'idx', idx
    p = individuals[idx]
    a = p['a']
    b = p['b']
    c = p['c']
    d = p['d']
    e = p['e']
    f = p['f']
    f_x = x * np.exp(np.sin(a * x + b)) * np.cos(c * x + d) * e + f
    print 'my_fitness:', MF.get_fitness(f_x)
    ax.plot(x, f_x)

a = 1
b = -1
c = 5.
d = 2
e = 3
f = -4
f_x = x * np.exp(np.sin(a * x + b)) * np.cos(c * x + d) * e + f
ax.plot(x, f_x, lw=4, c='k')

pylab.show()

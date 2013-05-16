import parameters
import simulation
import run_evolution
import fitness
import numpy as np

class my_sim(simulation.Simulation):

    def __init__(self, params):
        """Constructor
        Initializes the x-axis of the function to fit to
        """
        super(my_sim, self).__init__(params)

    def run_sim(self, params, my_number):
        """Implement an example 'simulation'

        Keyword arguments:
        params -- parameter dictionary
        """
        a = params['a']# = 1
        b = params['b']# = -1
        c = params['c']# = 5.
        d = params['d']# = 2
        e = params['e']# = 3
        f = params['f']# = -4
        x = self.params['x']
        f_x = x * np.exp(np.sin(a * x + b)) * np.cos(c * x + d) * e + f
        output_fn = self.params['output_fn_base'] + '%d.dat' % (my_number)
        np.savetxt(output_fn, np.array((x, f_x)))


    def get_results_for_individual(self, individual):

        output_fn = params['output_fn_base'] + '%d.dat'  % (individual)
        d = np.loadtxt(output_fn)
        return d


class my_fitness(fitness.Fitness):

    def __init__(self, params):

        super(my_fitness, self).__init__(params)


    def set_fitness_function(self, input_data):
        """Set the target function.

        Keyword arguments:
        input_data -- array of floats as input for the target or fitness function
        """
        a = 1
        b = -1
        c = 5.
        d = 2
        e = 3
        f = -4
        x = input_data
        f_x = x * np.exp(np.sin(a * x + b)) * np.cos(c * x + d) * e + f
        self.target_function = f_x


    def get_fitness(self, result):
        """Evaluate the results from one iteration

        Keyword arguments: 
        result -- must have the same format as self.input_data
        """
        diff = result - self.target_function
        abs_diff = np.abs(diff).sum()
        fitness = 1. / (abs_diff + 1e-12) 
        return fitness


class my_parameters(parameters.Parameters):

    def __init__(self):

        super(my_parameters, self).__init__()

        # set the input data on which the simulation class and the fitness should compute
        x_start = 0
        x_stop = 20.
        n_x = 1000.
        dx = (x_stop - x_start) / n_x
        x = np.arange(x_start, x_stop, dx)
        self.params['x'] = x
        self.params['output_fn_base'] = 'Results/fx_'


# the parameter storage class
my_params = my_parameters()
params = my_params.params
print 'params[\'x\']', params['x']

# the simulation you want to have tuned
sim = my_sim(params)
print 'my_sim.params', sim.params

fitness = my_fitness(params)

#sim.params['x'] = x
fitness.set_fitness_function(params['x'])


# create the main class that acts as framework
Evo = run_evolution.Evolution(sim, params, fitness, n_generations=100) 

parameter_ranges = { 'a' : (-10, 10.), \
                     'b' : (-10, 10.), \
                     'c' : (-10, 10.), \
                     'd' : (-10, 10.), \
                     'e' : (-10, 10.), \
                     'f' : (-10, 10.), \
                     }
"""
parameter_ranges should contain all parameters that are to tune.
Parameters that should not be modified by the algorithm must not be contained here, but in the parameter class.
"""
Evo.set_parameter_ranges(parameter_ranges)
Evo.run_evolution()

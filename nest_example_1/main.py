import parameters
import simulation
import run_evolution
import fitness
import numpy as np
import os

class my_sim(simulation.Simulation):


    def __init__(self, params):
        """Constructor
        Initializes the x-axis of the function to fit to
        """
        super(my_sim, self).__init__(params)


    def run_sim(self, params, ind_nr, save_to_disk=False):
        """Implement an example 'simulation'

        Keyword arguments:
        params -- parameter dictionary
        ind_nr -- (int) individual number
        gen_nr -- (int) generation number
        """
        
        self.params['folder_name'] = 'SimResults_%d/' % (ind_nr)
        os.system('python run_sim.py %s' % (self.params['folder_name']))


    def get_results_for_individual(self, ind_nr, gen_nr):
        """Return the data produced by a certain individuum in a certain generation.

        The output_fn that is loaded must be the same as in run_sim.

        Keyword arguments:
        ind_nr -- (int) individual number
        gen_nr -- (int) generation number

        Return value must be compatible with the fitness.get_fitness(r) array
        --> From run_evolution:
            result = self.sim.get_results_for_individual(j, gen_cnt)
            fitness_values[gen_cnt, j] = self.fitness.get_fitness(result)

        """
        # call the script that produces the analysis result
        os.system('python run_analysis.py %s' % (self.params['folder_name']))

        # pass the filename storing the result to the fitness class
        return self.params['analysis_result_fn']



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
        output_fn = self.params['folder_name'] +  'target_function.dat'
        print 'Saving target function to:', output_fn
        np.savetxt(output_fn, np.array((x, f_x)))


    def get_fitness(self, result_fn):
        """Evaluate the results from one iteration

        Keyword arguments: 
        result -- must have the same format as self.input_data
        """
        result = np.loadtxt(result_fn)

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
        self.params['folder_name'] = 'Results/'
        self.params['folder_names'] = [self.params['folder_name']]
        self.params['output_fn_base'] = '%sfx_' % self.params['folder_name']
        self.params['fitness_vs_time_fn'] = '%sfitness_vs_generation.dat' % (self.params['folder_name'])
        self.params['fitness_for_generation_fn_base'] = '%sfitness_gen_' % (self.params['folder_name'])
        self.params['parameters_for_individuals_fn_base'] = '%sparams_gen' % (self.params['folder_name'])
        self.create_folders()




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
Evo = run_evolution.Evolution(sim, params, fitness, n_generations=4, n_individuals=3, survivors=0.6, mutation_factor=0.05) 
#def __init__(self, sim, params, fitness, n_generations=10, n_individuals=10, survivors=0.6, rnd_seed=0):

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

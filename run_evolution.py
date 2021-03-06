import simulation
import parameters
import fitness
import numpy as np
import random
import json

class Evolution(object):

    def __init__(self, sim, params, fitness, n_generations=10, n_individuals=10, survivors=0.6, mutation_factor=0.05, rnd_seed=0):
        """Initialize the evolutionary_tuning framework

        Keyword arguments:
        sim -- instance of a simulation to be tuned
        params -- instance of a parameter class that stores all simulation parameters
        fitness -- the fitness function to be optimized
        n_generation -- Number of generations (full iterations) to be run (default 10)
        n_individuals -- Total number of individuals simulated in one generation (default 10)
        survivors -- Fraction of individuals that survive in each generation 
                    (default 0.6 meaning that the 40% of the individuals with the lowest fitness will be re-created in each generation)
        mutation_factor -- max percentage of change for each parameter for surviving individuals
        """

        self.sim = sim
        self.params = params
        self.fitness = fitness
        self.n_generations = n_generations
        self.n_individuals = n_individuals
        self.generation_cnt = 0 # count the generations 
        self.rnd_seed = rnd_seed # seed to initialize parameter values
        self.n_survivors = int(round(survivors * self.n_individuals))
        np.random.seed(self.rnd_seed)
        random.seed(self.rnd_seed + 1234)
        self.mutation_factor = mutation_factor 
#        assert (self.mutation_factor > .0 and self.mutation_factor < 1.0), 'ERROR: mutation_factor out of range: %f (must be > 0 and < 1.)' % (self.mutation_factor)
        self.param_ranges_set = False # before starting the Evolutionary algorithm, set_parameter_ranges must be called
        self.check_mandatory_params()

    def check_mandatory_params(self):
        list_of_mandatory_params = ['fitness_vs_time_fn', 'parameters_for_individuals_fn_base']
#        list_of_mandatory_params = ['fitness_vs_time_fn', 'fitness_for_generation_fn_base']

        list_of_missing_params = []
        for p in list_of_mandatory_params:
            try:
                a = self.params[p]
            except:
                list_of_missing_params.append(p)

        if len(list_of_missing_params) > 0:
            print 'ERROR! The following parameters have not been set in the parameters class'
            print list_of_missing_params
            print '\nPlease give them a value in your parameter class derived from class my_parameters(parameters.Parameters):'
            exit(1)

    def run_evolution(self):
        """
        Run the evolutionary optimization for sim_model 
        by tuning the parameters given in the dictionary params_to_tune
        and by evaluating the results by the fitness class.

        type(params_to_tune) = list
        """
        assert (self.param_ranges_set), 'ERROR: Call set_parameter_ranges(some_dictionary) before calling run_evolution in order to set the parameters to tune and their ranges!'
        self.initialize_individuals()
        self.run_all_generations()



    def initialize_individuals(self, init_params_for_individuals=None):
        """
        initializes the params_to_tune, e.g.

        for j, p in enumerate(len(self.params_to_tune)):
        """

        if init_params_for_individuals == None:
            self.params_for_individuals = [ {} for i in xrange(self.n_individuals)] # each individual has its own parameter dictionary
            for i in xrange(self.n_individuals):
                for j, p in enumerate(self.parameter_ranges.keys()):
                    self.params_for_individuals[i][p] = np.random.uniform(self.parameter_ranges[p][0], self.parameter_ranges[p][1])
                print 'Individual %d has init params' % i, self.params_for_individuals[i]
        else:
            self.params_for_individuals = init_params_for_individuals

                

    def set_parameter_ranges(self, dict_of_parameter_ranges):
        """
        Arg: dict_of_parameter_ranges is a dict with the parameter name as key,
        and a tuple storing (min, max) for the respective parameter as value.
        e.g.
        dict_of_parameter_ranges = {'a' : (a_min, a_max), ...}
        """
        self.parameter_ranges = dict_of_parameter_ranges
        self.params_to_tune = dict_of_parameter_ranges.keys()
        self.param_ranges_set = True


    def run_all_generations(self):
        """
        run the simulation --> Simulation
        evaluate results --> Fitness 

        """



        fitness_values = np.zeros((self.n_generations, self.n_individuals))
        for gen_cnt in xrange(self.n_generations):


            for ind in xrange(self.n_individuals):
                self.sim.run_sim(self.params_for_individuals[ind], ind, gen_cnt)

            # Get the results and fitness values for all individuals in the generation
            print 'Evolution.gen_cnt:', gen_cnt
            for j in xrange(self.n_individuals):
                result = self.sim.get_results_for_individual(j, gen_cnt)
                fitness_values[gen_cnt, j] = self.fitness.get_fitness(result)
#                print '%d %.6e' % (j, fitness_values[gen_cnt, j])
            sorted_idx = np.argsort(fitness_values[gen_cnt, :])
            n_new = self.n_individuals - self.n_survivors
            to_be_reinitiated = sorted_idx[:n_new]
            survivor_idx = sorted_idx[n_new:]

            # for interemediate control, save the fitness values for this generation

#            output_fn = self.params['fitness_for_generation_fn_base'] + '%d.dat' % (gen_cnt)
#            np.savetxt(output_fn, fitness_values[gen_cnt, :])

#            print '\nDEBUG'
#            print 'To be reinitiated:', to_be_reinitiated, fitness_values[gen_cnt, to_be_reinitiated]
#            print 'Survivors:', survivor_idx, fitness_values[gen_cnt, survivor_idx]

            # Re-initiate the ones that 'did not survive'
            for i_, new_ind_ in enumerate(to_be_reinitiated):
                # Determine the parents for this one individual
                parent_0 = random.choice(survivor_idx)
                parent_1 = random.choice(survivor_idx)
                while (parent_0 == parent_1):
                    parent_1 = random.choice(survivor_idx)
#                    print 'while', parent_0, parent_1, random.choice(survivor_idx)
#                print 'New individual %d gets parents:' % new_ind_, parent_0, parent_1
#                print 'parents params 0', parent_0, self.params_for_individuals[parent_0]
#                print 'parents params 1', parent_1, self.params_for_individuals[parent_1]
#                new_params = self.combine_parents_params(parent_0, parent_1, method='random')
                new_params = self.combine_parents_params(parent_0, parent_1, method='mean')
                self.params_for_individuals[new_ind_] = new_params
#                print 'After combination:', self.params_for_individuals[new_ind_]

            # Mutate those that survived
#            for survivor in sorted_idx[self.n_survivors:]:
            for survivor in survivor_idx:
                self.mutate(survivor)
#                print 'survivor, params', survivor, self.params_for_individuals[survivor]

            # Logging of parameters
            log_fn = self.params['parameters_for_individuals_fn_base'] + '%d.prm' % gen_cnt
            log_file = file(log_fn, 'w')
            print 'Writing parameters for generation %d to %s' % (gen_cnt, log_fn)
            json.dump(self.params_for_individuals, log_file)
            log_file.flush()


        output_fn = self.params['fitness_vs_time_fn']
        print 'Saving fitness values to:', output_fn
        np.savetxt(output_fn, fitness_values.transpose())

        print 'Saving parameters for individuals to:', output_fn
#                parents = np.random.randint #... 



    def combine_parents_params(self, parent_0, parent_1, method='random'):
        """Generate a new parameter set from the two existing ones

        Keyword arguments:
        parent_0, parent_1 -- integer values indicating the parent indices
        method -- if 'random' for each individual parameter a random value between parent_0 and parent_1 is chosen
                  if 'mean' the mean value between the parent_0's and parent_1's value is chosen.
        """

        p0 = self.params_for_individuals[parent_0]
        p1 = self.params_for_individuals[parent_1]
        new_params = {}
        for key in p0.keys():
            min_val = min(p0[key], p1[key])
            max_val = max(p0[key], p1[key])
            if method == 'mean':
                new_value = .5 * (max_val - min_val) + min_val
            else:# method == 'random':
                new_value = (max_val - min_val) * np.random.rand() + min_val
            new_params[key] = new_value
        return new_params

                    
    def mutate(self, individual): 
        """Modify the parameters of a 'surviving individual'. 
        
        Keyword arguments:
        individual -- integer giving the index of in the parameter list
        """
        old_params = self.params_for_individuals[individual]
        for key in old_params.keys():
            change = 2 * self.mutation_factor * np.random.rand() + (1. - self.mutation_factor)
            new_value = change * old_params[key] 
            global_min_val = self.parameter_ranges[key][0]
            global_max_val = self.parameter_ranges[key][1]
            # map into the 'allowed' range
            new_value = max(global_min_val, min(global_max_val, new_value))
            self.params_for_individuals[individual][key] = new_value


if __name__ == '__main__':

    # the parameter storage class
    params = parameters.Parameters()

    # the simulation you want to have tuned
    sim = simulation.Simulation(params)

    # params need to 
    fitness = fitness.Fitness(params)

    # create the main class that acts as framework
    Evo = Evolution(sim, params, fitness, n_generations=1) 

    parameter_ranges = { 'a' : (0, 1.), \
                         'b' : (0, 10.), \
                         'c' : (-1., 1) 
                         }
    """
    parameter_ranges should contain all parameters that are to tune.
    Parameters that should not be modified by the algorithm must not be contained here, but in the parameter class.
    """
    Evo.set_parameter_ranges(parameter_ranges)
    Evo.run_evolution()

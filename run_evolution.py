import simulation
import parameters
import fitness
import numpy as np

class Evolution(object):

    def __init__(self, sim, params, fitness, n_generations=10, n_individuals=10, survivors=0.6, rnd_seed=0):
        """Initialize the evolutionary_tuning framework

        Keyword arguments:
        sim -- instance of a simulation to be tuned
        params -- instance of a parameter class that stores all simulation parameters
        fitness -- the fitness function to be optimized
        n_generation -- Number of generations (full iterations) to be run (default 10)
        n_individuals -- Total number of individuals simulated in one generation (default 10)
        survivors -- Fraction of individuals that survive in each generation 
                    (default 0.6 meaning that the 40% of the individuals with the lowest fitness will be re-created in each generation)
        """

        self.sim = sim
        self.params = params
        self.fitness = fitness
        self.n_generations = n_generations
        self.n_individuals = n_individuals
        self.generation_cnt = 0 # count the generations 
        self.rnd_seed = rnd_seed # seed to initialize parameter values
        self.n_survivors = int(round(survivors * self.n_individuals))


    def run_evolution(self):
        """
        Run the evolutionary optimization for sim_model 
        by tuning the parameters given in the dictionary params_to_tune
        and by evaluating the results by the fitness class.

        type(params_to_tune) = list
        """
        self.initialize_individuals()
        self.run_generation()



    def initialize_individuals(self, init_params_for_individuals=None):
        """
        initializes the params_to_tune, e.g.

        for j, p in enumerate(len(self.params_to_tune)):
        """

        if init_params_for_individuals == None:
            np.random.seed(self.rnd_seed)
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



    def run_generation(self):
        """
        run the simulation --> Simulation
        evaluate results --> Fitness 

        """

        for gen_cnt in xrange(self.n_generations):

            self.sim.run_sim(self.params_for_individuals)

            # Get the results for all individuals in the generation
            generation_results = np.zeros(self.n_individuals)
            print 'Results for generation', gen_cnt
            for j in xrange(self.n_individuals):
                result = self.sim.get_results_for_individual(j)
                generation_results[j] = self.fitness.get_fitness(result)
                print '%d %.6e' % (j, generation_results[j])
            sorted_idx = np.argsort(generation_results)
            to_be_reinitiated = sorted_idx[:self.n_survivors]
            print generation_results[sorted_idx]
            print 'The following parameter sets survive this:'

            # Mutate those that survived
            for survivor in sorted_idx[self.n_survivors:]:
                print survivor, self.params_for_individuals[survivor]
                self.mutate(survivor)

            n_new = to_be_reinitiated.size
            # Re-initiate the ones that 'did not survive'
            for new_ind_ in xrange(n_new)
                # Determine the parents for this one individual
#                parents = np.random.randint #... 



                    
      def mutate(self, individual): 
          pass


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

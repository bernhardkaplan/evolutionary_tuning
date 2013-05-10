import simulation
import parameters
import fitness

class Evolution(object):

    def __init__(self, sim, params, fitness, n_generations=10, n_individuals=10):
        self.sim = sim
        self.params = params
        self.fitness = fitness
        self.n_generations = n_generations
        self.n_individuals = n_individuals
        self.generation_cnt = 0 # count the generations 

    def run_evolution(self, params_to_tune):
        """
        Run the evolutionary optimization for sim_model 
        by tuning the parameters given in the dictionary params_to_tune
        and by evaluating the results by the fitness class.

        type(params_to_tune) = list
        """
        self.params_to_tune = params_to_tune
        self.initialize_individuals()
        self.run_generation()


    def initialize_individuals(self):
        """
        initializes the params_to_tune
        """

        for i in xrange(self.n_individuals):
#            for j in xrange(len(self.params_to_tune)):
                self.params.initialize(self.params_to_tune)
#                pass


    def run_generation(self):
        """
        run the simulation --> Simulation
        evaluate results --> Fitness 

        """
        for i in xrange(self.n_generations):
            self.sim.run_sim()


if __name__ == '__main__':

    # the parameter storage class
    params = parameters.Parameters()

    # the simulation you want to have tuned
    sim = simulation.Simulation(params)

    # params need to 
    fitness = fitness.Fitness(params)

    # create the main class that acts as framework
    Evo = Evolution(sim, params, fitness) 

    params_to_tune = ['a']
    Evo.run_evolution(params_to_tune)

import numpy as np

class Fitness(object):

    def __init__(self, params):
        self.params = params
        pass


    def set_fitness_function(self, input_data):
        """Define the fitness function

        Keyword arguments:
        fitness_function -- The input data for the fitness function. Must have the same format as passed to get_fitness
        """
#        self.fitness_function = input_data
        pass 


    def get_fitness(self, result):
        """Evaluate the results from one iteration

        Keyword arguments: 
        result -- must have the same format as self.fitness_function
        """
        return np.random.rand()
#        pass

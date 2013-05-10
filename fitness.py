import numpy as np

class Fitness(object):

    def __init__(self, params):
        self.params = params
        pass


    def set_fitness_function(self, input_data):
        """Define the fitness function

        Keyword arguments:
        input_data -- The input data for the fitness function. Must have the same format as passed to get_fitness
        """
        self.input_data = input_data

    def get_fitness(self, result):
        """Evaluate the results from one iteration

        Keyword arguments: 
        result -- must have the same format as self.input_data
        """
        return np.random.rand()
#        pass

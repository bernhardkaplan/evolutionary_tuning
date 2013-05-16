
class Parameters(object):

    def __init__(self):
        self.params = {}

    def get(self):
        """Returns the stored parameters"""
        return self.params

    def set(self, p):
        """Update parameters

        Keyword arguments:
        p -- dictionary storing parameter keys and values to be updated.
        """
        if type(p) != type({'a':0}):
            print 'WARNING Parameters.set got wrong argument type! No parameters were set'
            return
        for key in p.keys():
            self.params[key] = p[key]

    def initialize(self, list_of_params_to_init):
        """
        Each parameter in the list_of_params_to_init should have a range(min, max):
        for p in list_of_params_to_init:
        """
        pass

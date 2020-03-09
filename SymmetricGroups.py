import logging
import itertools

S4_logger = logging.getLogger('S4_logger')
logging.basicConfig(level=logging.WARNING)
S4_logger.info('S4 logger created')

class SymGroup(n):

    def __init__(self):
        # Define it using an element list
        self.element_list = set(g for g in itertools.permutations(range(n)))
    # Combining two elements using the group operation is a very important function to define.

class SymGroupElem(n):

    def __mul__(self, second):
        logging.debug('1st element is %s, 2nd element is %s' %(self.element_list, second.element_list))
        return (lambda x: tuple(x[0][j] for j in x[1]))

My_S4 = S4Group()
print(My_S4.element_list)

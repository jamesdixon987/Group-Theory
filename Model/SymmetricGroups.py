import logging
import itertools
import Model.FinGroups

Sym_logger = logging.getLogger('Sym_logger')
logging.basicConfig(level=logging.WARNING)
Sym_logger.info('Sym logger created')

class SymGroup(Model.FinGroups.FinGroup):
    Sym_logger.info('Initiating SymGroup class')

    def __init__(self, size):
        assert(isinstance(size,int) and size > 1)
        Sym_logger.debug('size is %d' % size)
        self.element_list = set(g for g in itertools.permutations(range(1, size + 1)))
        self.size = size
        self.id = tuple(range(1, size + 1))
        Sym_logger.info('Symmetric group of size %d created' % size)

    Sym_logger.info('SymGroup class defined')


class SymGroupElem():
    Sym_logger.info('Initiating SymGroupElem class')

    def __init__(self, Sn_tuple):
        assert(isinstance(Sn_tuple,tuple))
        size = len(Sn_tuple)
        for k in Sn_tuple:
            assert k in range(1, size + 1)
        self.size = size
        self.display = Sn_tuple
        Sym_logger.info('Symmetric group element of size %d defined' % size)

    def __mul__(self, second):
        logging.debug('1st element is %s, 2nd element is %s' %(self, second))
        result = tuple(second.display[j - 1] for j in self.display)
        return result

    def __call__(self, value):
        assert(value in range(1,5))
        return self.display[value - 1]

    def get_cycle_representation(self):
        raise NotImplementedError()

    Sym_logger.info('SymGroup class defined')

My_S4 = SymGroup(4)

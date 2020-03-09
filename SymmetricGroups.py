import logging
import itertools

Sym_logger = logging.getLogger('Sym_logger')
logging.basicConfig(level=logging.WARNING)
Sym_logger.info('Sym logger created')

class SymGroup():
    Sym_logger.info('Initiating SymGroup class')

    def __init__(self, size):
        assert(isinstance(size,int) and size > 1)
        Sym_logger.debug('size is %d' % size)
        self.element_list = set(g for g in itertools.permutations(range(1, size + 1)))
        self.size = size
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

    Sym_logger.info('SymGroup class defined')

My_S4 = SymGroup(4)
print(My_S4.element_list)
FourTuple = SymGroupElem((4,1,2,3))
ThreeTuple = SymGroupElem((1,4,2,3))

print(FourTuple * ThreeTuple)

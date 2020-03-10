import logging
import itertools
from Model.FinGroups import FinGroup
from Model.FinGroups import FinGroupElement

sym_logger = logging.getLogger('sym_logger')
logging.basicConfig(level=logging.WARNING)
sym_logger.info('Sym logger created')

class SymGroup(FinGroup):
    sym_logger.info('Initiating SymGroup class')

    def __init__(self, order):
        assert(isinstance(order,int) and order > 1)
        """
        Attributes:
         * .order - an integer denoting the order of the symmetric group
         * .elements - a set of the objects that are the elements
         * .identity - a member of .elements that represents the group identity
        """
        self.order = order
        sym_logger.debug('order is %d' % order)
        element_list = tuple(itertools.permutations(range(1, order + 1)))
        self.elements = tuple(SymGroupElem(g) for g in element_list)
        sym_logger.debug('self.elements created')
        self.identity = FinGroup.get_identity(self.elements)
        sym_logger.info('Symmetric group of order %d created' % order)

    sym_logger.info('SymGroup class defined')


class SymGroupElem():
    sym_logger.info('Initiating SymGroupElem class')

    def __init__(self, Sn_tuple):
        assert(isinstance(Sn_tuple,tuple))
        group_order = len(Sn_tuple)
        test_unique_list = []
        for k in Sn_tuple:
            assert k in range(1, group_order + 1)
            assert k not in test_unique_list
            test_unique_list.append(k)
            sym_logger.debug('test list is %s' % test_unique_list)
        self.group_order = group_order
        self.display = Sn_tuple
        self.group_identity = tuple(range(1, group_order + 1))
        self.inverse = NotImplementedError()
        sym_logger.info('Symmetric group element {} defined'.format(self.display))

    def __mul__(self, second):
        sym_logger.debug('1st element is %s, 2nd element is %s' %(self, second))
        assert(self.group_order == second.group_order)
        sym_logger.debug('Elements are from symmetric group of group_order %d' % self.group_order)
        result = tuple(second.display[j - 1] for j in self.display)
        return result

    def __eq__(self, other):
        return self.display == other

    def __call__(self, value):
        assert(value in self.group_identity)
        return self.display[value - 1]

    def get_cycle_representation(self):
        raise NotImplementedError()

    sym_logger.info('SymGroup class defined')

# My_S4 = SymGroup(4)
# sym_logger.info('I reached here')
# Bad_element = SymGroupElem((1,4,2,3))
# print(FinGroup.get_inverse(Bad_element, My_S4).display)

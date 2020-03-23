import logging
import itertools
from Model.FinGroups import FinGroup
from Model.FinGroups import FinGroupElem

sym_logger = logging.getLogger('sym_logger')
logging.basicConfig(level=logging.INFO)
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

        FinGroup.__init__(self, self.elements)
    sym_logger.info('SymGroup class defined')


class SymGroupElem(FinGroupElem):
    sym_logger.info('Initiating SymGroupElem class')

    def __init__(self, Sn_tuple):
        assert(isinstance(Sn_tuple,tuple))
        FinGroupElem.__init__(self)

        """
        Attributes:
         * .group_order - an integer denoting the order of the symmetric group
         * .display - a display of the tuple representing the element
         * .order
         
         Operations:
         * mul - group operation
         * pow - power group operation
         * eq & ne - compares tuples
         * call - shows where a number (1 to n) moves to under the element
         
         Class methods:
         * get_cycle_representation - fairly self-explanatory
         * group_identity - returns a SymGroupElem object, group identity
         """

        group_order = len(Sn_tuple)
        self.group_order = group_order
        test_unique_list = []
        for k in Sn_tuple:
            assert k in range(1, group_order + 1)
            assert k not in test_unique_list
            test_unique_list.append(k)
            sym_logger.debug('test list is %s' % test_unique_list)
        self.display = Sn_tuple

        sym_logger.debug('Symmetric group element {} defined'.format(self.display))

    def __mul__(self, second):
        sym_logger.debug('1st element is %s, 2nd element is %s' %(str(self.display), str(second.display)))
        assert(isinstance(second, SymGroupElem))
        assert(self.group_order == second.group_order)
        sym_logger.debug('Elements are from symmetric group of group_order %d' % self.group_order)
        result = tuple(second.display[j - 1] for j in self.display)
        sym_logger.debug('result is %s' %(str(result)))
        return SymGroupElem(result)

    def __pow__(self, power):
        assert(isinstance(power, int))
        if power == 0:
            return group_identity(self)
        elif power == 1:
            return self
        elif power > 1:
            return self * pow(self, power - 1)
        else:
            return self.inverse[pow(self, -power)]

    def __call__(self, value):
        assert(value in self.display)
        return self.display[value - 1]

    def group_identity(self):
        return SymGroupElem(tuple(range(1,self.group_order + 1)))

    def get_cycle_representation(self):
        sym_logger.info('Initialising get_cycle_representation method')
        num_list = tuple(range(1,self.group_order + 1))
        done = []
        cycles = []
        for num in num_list:
            sym_logger.debug('next num is %d' %num)
            if num in done:
                sym_logger.debug('%d in done' %num)
                pass
            elif self.display[num - 1] == num:
                sym_logger.debug('%d not in a cycle' %num)
                done.append(num)
            else:
                current_num = self.display[num - 1]
                sym_logger.debug('current_num is %d' %current_num)
                cycle = [num]
                while current_num != num:
                    done.append(current_num)
                    cycle.append(current_num)
                    current_num = self.display[current_num - 1]
                done.append(num)
                sym_logger.debug('cycle is %s' %str(cycle))
                cycles.append(tuple(cycle))
        if len(cycles) == 1:
            sym_logger.info('element has one cycle: %s' %str(cycle))
            return cycles[0]
        elif len(cycles) == 0:
            sym_logger.info('element is identity')
            return ()
        else:
            sym_logger.info('element cycle representation is %s' %str(cycles))
            return tuple(cycles)

    sym_logger.info('SymGroup class defined')


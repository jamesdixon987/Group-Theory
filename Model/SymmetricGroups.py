import logging
import itertools
from Model.FinGroups import FinGroup
from Model.FinGroups import FinGroupElem

sym_logger = logging.getLogger('sym_logger')
sym_logger.info('sym_logger created')


class SymGroup(FinGroup):
    sym_logger.info('Initiating SymGroup class')

    def __init__(self, order):
        assert(isinstance(order, int) and order > 1)

        """
        Attributes:
         * .order - an integer denoting the order of the symmetric group
         * .elements - a set of the objects that are the elements
        """

        self.order = order
        sym_logger.debug('order is %d' % order)

        element_list = tuple(itertools.permutations(range(1, order + 1)))
        self.elements = tuple(SymGroupElem(g, self) for g in element_list)
        sym_logger.debug('self.elements created')

        sym_logger.info('Symmetric group of order %d created' % order)

        super().__init__(self, self.elements, type = 'Symmetric', group_description = f'Symmetric order {order}',
                          associated_group = self)

        generator1 = list(range(2, order + 1))
        generator1.append(1)
        generator1 = SymGroupElem(tuple(generator1), associated_group = self)
        generator2 = [2, 1]
        for x in range(3, order + 1):
            generator2.append(x)
        generator2 = SymGroupElem(tuple(generator2), associated_group = self)
        self.generating_set = (generator1, generator2)

    sym_logger.info('SymGroup class defined')


class SymGroupElem(FinGroupElem):
    sym_logger.info('Initiating SymGroupElem class')

    def __init__(self, Sn_tuple, associated_group = None):
        assert(isinstance(Sn_tuple, tuple))

        """
        Attributes:
         * .group_type - 'Symmetric'
         * .group_order - an integer denoting the order of the symmetric group
         * .display - a display of the tuple representing the element
         * .order

         Operations:
         * mul - group operation
         * call - shows where a number (1 to n) moves to under the element

         Methods:
         * get_cycle_representation - fairly self-explanatory

         Inherited Attributes:
         * _inverse_holder - placeholder for inverse, so it doesn't have to be recalculated every time

         Inherited Operations:
         * pow - power in group operation
         * eq & ne - compare elements
         * str - string representation of element.dsiplay

         Inherited Methods:
         * inverse - must have a group associated
         * order - order of element; must have a group associated
         * group_identity - must have a group associated
         """

        assert(isinstance(associated_group, FinGroup) or associated_group is None)
        FinGroupElem.__init__(self, associated_group = associated_group)

        self.group_type = 'Symmetric'

        if self.associated_group is None:
            self.group_order = len(Sn_tuple)
        else: self.group_order = self.associated_group.order

        test_unique_list = []
        for k in Sn_tuple:
            assert k in range(1, self.group_order + 1)
            assert k not in test_unique_list
            test_unique_list.append(k)
            sym_logger.debug('test list is %s' % test_unique_list)

        self._element_holder = Sn_tuple

        self.display = SymGroupElem.get_cycle_representation(self)
        sym_logger.debug('element cycle representation is %s' % str(self.display))

        sym_logger.debug('Symmetric group element {} defined'.format(self.display))

    def __mul__(self, second):
        sym_logger.debug('1st element is %s, 2nd element is %s' % (str(self.display), str(second.display)))
        assert(isinstance(second, SymGroupElem))
        assert(self.group_order == second.group_order)
        sym_logger.debug('Elements are from symmetric group of group_order %d' % self.group_order)
        result = tuple(second._element_holder[j - 1] for j in self._element_holder)
        sym_logger.debug('result is %s' % (str(result)))
        if self.associated_group is None:
            return SymGroupElem(result)
        else:
            return self.associated_group(result)

    def __call__(self, value):
        assert(value in self._element_holder)
        return self._element_holder[value - 1]

    def cycle_type(self):
        result = []
        for g in self.display:
            result.append(len(g))
        sym_logger.debug('element cycle type is %s' % str(result))
        return tuple(result)

    @classmethod
    def get_cycle_representation(cls, self):
        sym_logger.debug('Initialising get_cycle_representation method')
        num_list = tuple(range(1, self.group_order + 1))
        sym_logger.debug('num_list is %s' % str(num_list))
        sym_logger.debug('tuple is %s' % str(self._element_holder))
        done = []
        cycles = []
        for num in num_list:
            sym_logger.debug('next num is %d' % num)
            if num in done:
                sym_logger.debug('%d in done' % num)
                pass
            else:
                current_num = self._element_holder[num - 1]
                sym_logger.debug('current_num is %d' % current_num)
                cycle = [num]
                while current_num != num:
                    done.append(current_num)
                    cycle.append(current_num)
                    current_num = self._element_holder[current_num - 1]
                done.append(num)
                sym_logger.debug('cycle is %s' % str(cycle))
                cycles.append(tuple(cycle))
        if len(cycles) == 0:
            sym_logger.debug('element is identity')
            return ()
        else:
            sym_logger.debug('element cycle representation is %s' % str(cycles))
            return tuple(cycles)

    sym_logger.info('SymGroup class defined')


dih_logger = logging.getLogger('dih_logger')
dih_logger.info('dih_logger created')


class DiGroup(FinGroup):
    dih_logger.info('Initiating DiGroup class')

    def __init__(self, order):
        dih_logger.info('Initiating DiGroup object')
        dih_logger.warning('Digroup(n) represents the symmetries of an n-sided polygon')
        assert(isinstance(order, int) and order > 1)

        """
        Attributes:
         * .order - an integer denoting the order of the dihedral group
         * .elements - a set of the objects that are the elements
         * .identity - a member of .elements that represents the group identity
        """

        self.order = order
        dih_logger.debug('order is %d' % order)

        if order == 2:
            self.elements = FinGroupElem.generate(SymGroupElem((2, 1))).elements
        else:
            generator1 = list(range(2, order+1))
            generator1.append(1)
            generator1 = tuple(generator1)

            generator2 = [1]
            for x in range(order, 1,-1):
                generator2.append(x)
            generator2 = tuple(generator2)

            self.elements = FinGroupElem.generate(SymGroupElem(generator1),
                                                  SymGroupElem(generator2)).elements


        for element in self.elements:
            element.associated_group = self
            element.group_type = 'Dihedral'

        FinGroup.__init__(self, self.elements, type = 'Dihedral', group_description = 'Dihedral order %d' % order,
                  associated_group = self)

        dih_logger.debug('self.elements created')

        dih_logger.info('Dihedral group of order %d created' % order)

    dih_logger.info('Dihedral class defined')

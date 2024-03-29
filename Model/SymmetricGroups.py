import logging
import itertools
from Model.FinGroups import *

sym_logger = logging.getLogger('sym_logger')
sym_logger.info('sym_logger created')


class SymGroup(FinGroup):
    sym_logger.info('Initiating SymGroup class')

    def __init__(self, order):
        #Errors
        if not isinstance(order, int):
            raise TypeError('order must be an integer')
        if not order > 1:
            raise ValueError('order must be greater than 1')

        self.order = order
        sym_logger.debug('SymGroup order is %d' % order)

        self.tuple_list = tuple(itertools.permutations(range(1, order + 1)))
        self.elements = tuple(SymGroupElem(g, self) for g in self.tuple_list)
        sym_logger.debug('self.elements created')

        super().__init__(self.elements, type = 'Symmetric', group_description = f'Symmetric order {order}')

        generator1 = list(range(2, order + 1))
        generator1.append(1)
        generator1 = SymGroupElem(tuple(generator1), associated_group = self)
        generator2 = [2, 1]
        for x in range(3, order + 1):
            generator2.append(x)
        generator2 = SymGroupElem(tuple(generator2), associated_group = self)
        self.generating_set = (generator1, generator2)

        sym_logger.info('Symmetric group of order %d created' % order)

    sym_logger.info('SymGroup class defined')


class SymGroupElem(FinGroupElem):
    sym_logger.info('Initiating SymGroupElem class')

    def __init__(self, Sn_tuple, associated_group = None):
        # Errors
        if not isinstance(Sn_tuple, tuple):
            raise TypeError('Sn_tuple must be an tuple')
        if not len(Sn_tuple) > 1:
            raise ValueError('length must be greater than 1')

        test_unique_list = []
        for k in Sn_tuple:
            if not isinstance(k, int):
                raise ValueError('values must be integers')
            if not k in range(1, len(Sn_tuple) + 1):
                raise ValueError('values must range from 1 to length of tuple')
            if k in test_unique_list:
                raise ValueError('values must not be repeated')
            test_unique_list.append(k)

        assert(isinstance(associated_group, FinGroup) or associated_group is None)

        super().__init__(associated_group = associated_group)

        self.group_type = 'Symmetric'

        if self.associated_group is None:
            self.group_order = len(Sn_tuple)
        else: self.group_order = self.associated_group.order

        self._element_holder = Sn_tuple

        self.display = self.display_cycles() + ' in %s group order %d' % (self.group_type, self.group_order)

        sym_logger.debug('element cycle representation is %s' % str(self.display))

        sym_logger.debug('Symmetric group element {} defined'.format(self.display))

    def __mul__(self, second):
        #Errors
        if not isinstance(second, SymGroupElem):
            raise TypeError('Invalid type for * operation with SymGroupElem')
        if self.group_order != second.group_order:
            raise GroupOrderError('Elements must be of the same order')
        sym_logger.debug('Elements are from symmetric group of group_order %d' % self.group_order)

        result = tuple(second._element_holder[j - 1] for j in self._element_holder)
        sym_logger.debug('result is %s' % (str(result)))
        if self.associated_group is None:
            return SymGroupElem(result)
        elif SymGroupElem(result) not in self.associated_group.elements:
            return SymGroupElem(result)
        else:
            return self.associated_group(result)

    def __call__(self, value):
        assert(value in self._element_holder)
        return self._element_holder[value - 1]

    def cycle_type(self):
        result = []
        cycle_list = self.cycles()
        for cycle in cycle_list:
            result.append(len(cycle))
        sym_logger.debug('element cycle type is %s' % str(result))
        return tuple(result)

    def display_cycles(self):
        cycle_display_string = ''
        cycle_list = self.cycles()
        for cycle in cycle_list:
            if len(cycle) > 1:
                cycle_display_string = cycle_display_string + str(cycle)
        if cycle_display_string == '':
            return '()'
        else: return cycle_display_string.replace(',','')

    def cycles(self):
        sym_logger.debug('Initialising get_cycle_representation method')
        num_list = tuple(range(1, self.group_order + 1))
        done = []
        cycles = []
        for num in num_list:
            if num in done:
                pass
            else:
                current_num = self._element_holder[num - 1]
                cycle = [num]
                while current_num != num:
                    done.append(current_num)
                    cycle.append(current_num)
                    current_num = self._element_holder[current_num - 1]
                done.append(num)
                cycles.append(tuple(cycle))
        if len(cycles) == 0:
            return ()
        else:
            return tuple(cycles)

    def permutation_parity(self):
        parity = 1
        for num in self.cycle_type():
            if num % 2 == 0:
                parity *= -1
        return parity

    sym_logger.info('SymGroup class defined')


dih_logger = logging.getLogger('dih_logger')
dih_logger.info('dih_logger created')


class DiGroup(FinGroup):
    dih_logger.info('Initiating DiGroup class')

    def __init__(self, order):
        # Errors
        if not isinstance(order, int):
            raise TypeError('order must be an integer')
        if not order > 1:
            raise ValueError('order must be greater than 1')

        dih_logger.info('Digroup(n) represents the symmetries of an n-sided polygon')
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

            self.generating_set = (generator1, generator2)

        for element in self.elements:
            element.associated_group = self
            element.group_type = 'Dihedral'

        super().__init__(self.elements, type = 'Dihedral', group_description = 'Dihedral order %d' % order)

        dih_logger.debug('self.elements created')

        dih_logger.info('Dihedral group of order %d created' % order)

    dih_logger.info('Dihedral class defined')

class AltGroup(FinGroup):
    sym_logger.info('Initiating AltGroup class')

    def __init__(self, order):
        # Errors
        if not isinstance(order, int):
            raise TypeError('order must be an integer')
        if not order > 1:
            raise ValueError('order must be greater than 1')

        self.order = order
        sym_logger.debug('AltGroup order is %d' % order)

        tuple_list = tuple(itertools.permutations(range(1, order + 1)))
        self.elements = tuple(SymGroupElem(g, associated_group = self) for g in tuple_list
                              if _tuple_parity(g) == 1)
        sym_logger.debug('self.elements created')

        for element in self.elements:
            element.associated_group = self
            element.group_type = 'Alternating'

        super().__init__(self.elements, type = 'Alternating', group_description = f'Alternating order {order}')

        sym_logger.info('Alternating group of order %d created' % order)


def _tuple_parity(tuple_to_sort):
    sym_logger.info('sorting %s with _tuple_parity method' % str(tuple_to_sort))
    list_to_sort = list(tuple_to_sort)
    parity = 1
    sorted = list(tuple_to_sort)
    sorted.sort()
    while sorted != list_to_sort:
        for n in range(len(list_to_sort) - 1):
            if list_to_sort[n] > list_to_sort[n+1]:
                list_to_sort[n], list_to_sort[n+1] = list_to_sort[n+1], list_to_sort[n]
                parity *= -1
    return parity


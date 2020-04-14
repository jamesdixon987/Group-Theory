import logging
from Model.Groups import *
from Model.Errors import *

fin_group_logger = logging.getLogger('fin_group_logger')
fin_group_logger.info('fin_group_logger created')

class FinGroup(Group):
    def __init__(self, elements, type = None, group_description = None):
        fin_group_logger.info('Initiating FinGroup object')

        super().__init__()

        self.finite = True

        self.type = type

        self.group_description = group_description

        self.elements = elements

        self.identity = FinGroup.get_identity(self.elements)

        self.generating_set = None

    def __iter__(self):
        fin_group_logger.debug('Initiating FinGroup iterator')
        # Iterate over the elements of the group, returning the identity first
        yield self.identity
        for g in self.elements:
            if g != self.identity:
                yield g

    def __call__(self, elem):
        calling_result = []
        if isinstance(elem, FinGroupElem):
            calling_result = [item for item in self.elements if item == elem]
        else:
            calling_result = [item for item in self.elements if item._element_holder == elem]
        if calling_result == []:
            raise GroupElementError
        fin_group_logger.debug('result is %s elem is %s' % (str(calling_result), str(elem)))
        return calling_result[0]

    def size(self):
        return len(self.elements)

    def show_elements(self):
        for element in self.elements:
            print(element.display)

    def is_abelian(self):
        return all(a * b == b * a for a in self.elements for b in self.elements)

    def is_subgroup(self, poss_sbgrp):
        return  all(any(g == n for g in self.elements) for n in poss_sbgrp.elements)

    def is_normal_subgroup(self, poss_norm_sbgrp):
        assert(isinstance(poss_norm_sbgrp, FinGroup))
        if self.is_subgroup(poss_norm_sbgrp):
            n = poss_norm_sbgrp.elements[1]
            return all(set(g * n for n in poss_norm_sbgrp.elements) == set(n * g for n in poss_norm_sbgrp.elements)
                   for g in self.elements)
        else:
            print(str(poss_norm_sbgrp) + ' is not a subgroup of ' + str(self))
            raise ValueError

    # Currently prints every element on a new line - thinking about what to do

    # def print_cayley_table(self):
    #     for a in self:
    #         for b in self:
    #             c = a*b
    #             print(str(c) + ',')
    #         print('')

    @classmethod
    def direct_product(cls, first, other):
        assert(isinstance(other, FinGroup))
        fin_group_logger.info('Initiating direct_product method with %s and %s'
                              % (first.group_description, other.group_description))
        elements = tuple(ProductGroupElem(_element_holder = (elem1,elem2))
                         for elem1 in first.elements for elem2 in other.elements)
        result_group = FinGroup(elements, type = 'Product of %s and %s' % (first.type, other.type),
                    group_description = 'Product of %s and %s' % (first.group_description, other.group_description))
        for elem in result_group.elements:
            elem.associated_group = result_group
        return result_group

    @classmethod
    def get_inverse(cls, g, group):
        fin_group_logger.info('Initiating FinGroup class method get_inverse')
        for other in group.elements:
            fin_group_logger.debug('Testing %s' % str(other.display))
            if other * g == group.identity:
                return other

        raise ValueError(g)

    @classmethod
    def get_identity(cls, elements):
        fin_group_logger.info('Initiating FinGroup class method get_identity')
        for g in elements:
            if (Group.is_identity(g)):
                fin_group_logger.info('Identity found')
                return g
            else:fin_group_logger.debug('element %s is not identity' %str(g.display))
        fin_group_logger.error('No identity element found')
        raise ValueError()


class FinGroupElem(GroupElem):
    def __init__(self, associated_group = None, _element_holder = None):
        fin_group_logger.info('Initiating FinGroupElem object')

        self.associated_group = associated_group

        self._element_holder = _element_holder

        super().__init__()

    def __pow__(self, power):
        assert(isinstance(power, int))
        if power == 0:
            return self.group_identity()
        elif power == 1:
            return self
        elif power > 1:
            if power % 2 == 1:
                return self * (self ** (power - 1))
            else:
                return (self * self) ** (int(power / 2))
        else:
            try:
                assert(self.associated_group is not None)
            except AssertionError:
                fin_group_logger.error('Cannot process negative powers without associated group')
                raise TypeError
            return (pow(self, -power)).inverse()

    def inverse(self):
        fin_group_logger.debug('Initialising FinGroupElem.inverse method')
        try:
            assert(self.associated_group is not None)
            fin_group_logger.debug('Element has associated group %s' %self.associated_group)
        except AssertionError:
            fin_group_logger.error('Cannot find inverse if element has no associated group')
            print(self.display)
            raise AttributeError
        if self._inverse_holder is None:
            self._inverse_holder = FinGroup.get_inverse(self, self.associated_group)
            return self._inverse_holder
        else: return self._inverse_holder

    def group_identity(self):
        fin_group_logger.debug('Initialising FinGroupElem.group_identity method')
        find_identity = self ** 2
        testing = find_identity * self
        while testing != self:
            find_identity *= self
            testing *= self
        return find_identity

    def order(self):
        fin_group_logger.debug('Initialising FinGroup.order method')
        return FinGroup.get_elem_order(self, self.group_identity())

    def get_elem_order(self):
        if self ** 2 == self:
            return 1
        else:
            testing = self ** 2
            count = 2
            while testing != self:
                testing *= self
                count += 1
            return count - 1

    def generate(self, *others):
        fin_group_logger.info('Initialising Helper.generate method')
        old_group = {self} | set(others)
        fin_group_logger.debug('Generating using elements')
        old_group_description = [elem.display for elem in old_group]
        gen_group_descr = 'Subgroup generated by %s' % str(old_group_description)

        generating_set = tuple(old_group)
        fin_group_logger.debug('Generating set has size %d' % len(old_group))
        fin_group_logger.debug('Generating set is %s' % str(old_group))

        new_elems = set(g ** n for g in old_group for n in range(g.get_elem_order())) ^ old_group
        while True:
            new_group = new_elems | set(a * b for a in new_elems for b in old_group) \
                        | set(b * a for a in new_elems for b in old_group) | old_group
            fin_group_logger.debug('New set has size %d' % len(new_group))
            if old_group == new_group: break
            else: old_group = new_group
            new_elems = set(g ** n for g in old_group for n in range(g.get_elem_order()))
        fin_group_logger.debug('New group has size %d' % len(new_group))

        generated_group = FinGroup(tuple(new_group), type='Generated subgroup', group_description=gen_group_descr)
        generated_group.generating_set = generating_set
        for element in generated_group.elements:
            element.associated_group = generated_group
        return generated_group


class ProductGroupElem(FinGroupElem):

    def __init__(self, _element_holder = None, associated_group = None):
        fin_group_logger.info('Initiating FinGroupElem object')

        super().__init__(associated_group = associated_group, _element_holder = _element_holder)

        self.display = (self._element_holder[0].display, self._element_holder[1].display)

        self.group_type = 'Product'

    def __mul__(self, other):
        assert(isinstance(other, ProductGroupElem))

        result = (self._element_holder[0] * other._element_holder[0],
                  self._element_holder[1] * other._element_holder[1])
        if self.associated_group is None:
            return ProductGroupElem(_element_holder=result)
        else:
            return self.associated_group(result)

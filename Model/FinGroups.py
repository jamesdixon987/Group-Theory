import logging
from Model.Groups import Group
from Model.Groups import GroupElem

fin_group_logger = logging.getLogger('fin_group_logger')
fin_group_logger.info('fin_group_logger created')

class FinGroup(Group):

    """
    WITHIN EACH SUBCLASS OF FINGROUP, THE FOLLOWING MUST BE DEFINED:

    Attributes:
     * .elements - a list of the elements
     * .type
     * .group_description

     Operations:

     Methods:
     """

    def __init__(self, elements, type = None, group_description = None, associated_group = None):
        fin_group_logger.info('Initiating FinGroup object')

        super().__init__()

        self.finite = True

        self.type = type

        self.group_description = group_description

        self.associated_group = associated_group

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
        if isinstance(elem, GroupElem):
            result = [item for item in self.elements if item == elem]
        else:
            result = [item for item in self.elements if item._element_holder == elem]
        return result[0]

    def size(self):
        return len(self.elements)

    def show_elements(self):
        for element in self.elements:
            print(element.display)

    def is_abelian(self):
        return all(a * b == b * a for a in self.elements for b in self.elements)

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

    """
    WITHIN EACH SUBCLASS OF FINGROUPELEM, THE FOLLOWING MUST BE DEFINED:

    Attributes:
     * element.display - a unique (within group) 'nice' display for each element. Used for __eq__ & __ne__
     * element._element_holder - a unique display used for searching for elements in group (e.g. in __mul__)

     Operations:
     * mul (*) - group binary operation between elements

     Methods:
     * group_identity - returns an element object, group identity
     """


    def __init__(self, associated_group = None, _element_holder = None):
        fin_group_logger.info('Initiating FinGroupElem object')

        self.associated_group = associated_group

        self._element_holder = _element_holder

        super().__init__()

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
        try:
            assert(self.associated_group is not None)
            fin_group_logger.debug('Element has associated group')
        except AssertionError:
            fin_group_logger.warning('Cannot find identity if element has no associated group')
            raise AttributeError
        return self.associated_group.identity

    def order(self):
        fin_group_logger.debug('Initialising FinGroup.order method')
        return FinGroup.get_elem_order(self, group_identity(self))

    def get_elem_order(self):
        testing = self
        count = 1
        while testing != self:
            testing *= self
            count += 1
        return count - 1

    def generate(self, *others):
        fin_group_logger.info('Initialising Helper.generate method')
        if isinstance(self, tuple):
            fin_group_logger.debug('Generating using tuple')
            old_group = set(self)
        else:
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

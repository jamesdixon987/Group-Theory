import logging

fin_group_logger = logging.getLogger('fin_group_logger')
fin_group_logger.info('fin_group_logger created')

class FinGroup:

    """
    WITHIN EACH SUBCLASS OF FINGROUP, THE FOLLOWING MUST BE DEFINED:

    Attributes:
     * .elements - a list of the elements
     * .identity - can be found using FinGroup classmethod get_inverse

     Operations:

     Methods:
     """

    def __init__(self, elements):
        fin_group_logger.info('Initiating FinGroup object')

        self.elements = elements

        self.abelian = all(a * b == b * a for a in self.elements for b in self.elements)

    def __iter__(self):
        fin_group_logger.debug('Initiating FinGroup iterator')
        # Iterate over the elements of the group, returning the identity first
        yield self.identity
        for g in self.elements:
            if g != self.identity:
                yield g

    def __contains__(self, item):
        return item in self.elements

    def size(self):
        return len(self.elements)

    @classmethod
    def get_inverse(cls, g, group):
        fin_group_logger.info('Initiating FinGroup class method get_inverse')
        for other in group.elements:
            fin_group_logger.debug('Testing %s' % other)
            if other * g == group.identity:
                return other

        raise ValueError(g)

    @classmethod
    def get_identity(cls, elements):
        fin_group_logger.info('Initiating FinGroup class method get_identity')
        for g in elements:
            if (cls.is_identity(g, elements)):
                fin_group_logger.info('Identity found')
                return g
            else:fin_group_logger.debug('element %s is not identity' %str(element.display))
        raise ValueError()

    @classmethod
    def is_identity(cls, possible_id, elements) -> bool:
        fin_group_logger.info('Initiating FinGroup class method is_identity')
        for element in elements:
            if not possible_id * element == element:
                return False

        return True

    @classmethod
    def get_elem_order(cls, elem, identity):
        testing = elem
        count = 1
        while testing != identity:
            testing *= elem
            count += 1
        return count

class FinGroupElem():

    """
    WITHIN EACH SUBCLASS OF FINGROUPELEM, THE FOLLOWING MUST BE DEFINED:

    Attributes:
     * .display - a unique (within group) display of the element. Used for __eq__ & __ne__

     Operations:
     * mul - group operation

     Methods:
     * group_identity - returns an object, group identity
     """


    def __init__(self):
        self._inverse_holder = None


    def __eq__(self, other):
        fin_group_logger.debug('1st element is %s, 2nd element is %s' %(str(self.display), str(other.display)))
        assert(self.group_order == other.group_order)
        fin_group_logger.debug('Elements are from symmetric group of group_order %d' % self.group_order)
        return self.display == other.display

    def __ne__(self, other):
        fin_group_logger.debug('1st element is %s, 2nd element is %s' %(str(self.display), str(other.display)))
        return not self.display == other.display

    def __str__(self):
        return str(self.display)

    def __pow__(self, power):
        assert(isinstance(power, int))
        if power == 0:
            return group_identity(self)
        elif power == 1:
            return self
        elif power > 1:
            return self * pow(self, power - 1)
        else:
            try:
                assert(self.associated_group != None)
            except AssertionError:
                sym_logger.error('Cannot process negative powers without associated group')
                raise TypeError
            return FinGroup.get_inverse(pow(self, -power), self.associated_group)

    def inverse(self, group):
        assert(isinstance(group, FinGroup))
        assert(self in group.elements)
        if self._inverse_holder == None:
            self._inverse_holder = FinGroup.get_inverse(self, group)
            return self._inverse_holder
        else: return self._inverse_holder

    def order(self):
        return FinGroup.get_elem_order(self, group_identity(self))

    def group_identity(self):
        try:
            assert(self.associated_group != None)
            fin_group_logger.debug('Element has associated group')
        except AssertionError:
            raise AttributeError
            fin_group_logger.warning('Cannot find identity if element has no associated group')
        return self.associated_group.identity

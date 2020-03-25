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

     Operations:

     Methods:
     """

    def __init__(self, elements):
        fin_group_logger.info('Initiating FinGroup object')

        Group.__init__(self)

        self.type = None

        self.Finite = True

        self.abelian = all(a * b == b * a for a in self.elements for b in self.elements)

        self.elements = elements

        self.identity = FinGroup.get_identity(self.elements)

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

    @classmethod
    def get_elem_order(cls, elem, identity):
        testing = elem
        count = 1
        while testing != identity:
            testing *= elem
            count += 1
        return count

class FinGroupElem(GroupElem):

    """
    WITHIN EACH SUBCLASS OF FINGROUPELEM, THE FOLLOWING MUST BE DEFINED:

    Attributes:
     * element.display - a unique (within group) display for each element. Used for __eq__ & __ne__

     Operations:
     * mul (*) - group binary operation between elements

     Methods:
     * group_identity - returns an element object, group identity
     """


    def __init__(self):

        fin_group_logger.info('Initiating Group object')

        GroupElem.__init__(self)

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
                fin_group_logger.error('Cannot process negative powers without associated group')
                raise TypeError
            return FinGroup.get_inverse(pow(self, -power), self.associated_group)

    def inverse(self, group):
        fin_group_logger.debug('Initialising FinGroupElem.inverse method')
        try:
            assert(self.associated_group != None)
            fin_group_logger.debug('Element has associated group %s' %group)
        except AssertionError:
            raise AttributeError
            fin_group_logger.warning('Cannot find inverse if element has no associated group')
        if self._inverse_holder == None:
            self._inverse_holder = FinGroup.get_inverse(self, group)
            return self._inverse_holder
        else: return self._inverse_holder

    def order(self):
        fin_group_logger.debug('Initialising FinGroup.order method')
        return FinGroup.get_elem_order(self, group_identity(self))

    def group_identity(self):
        fin_group_logger.debug('Initialising FinGroupElem.group_identity method')
        try:
            assert(self.associated_group != None)
            fin_group_logger.debug('Element has associated group')
        except AssertionError:
            raise AttributeError
            fin_group_logger.warning('Cannot find identity if element has no associated group')
        return self.associated_group.identity

    def generate(self, *others):
        # Not that this returns the element tuple for a new group. It does not intialise the group.
        fin_group_logger.info('Initialising FinGroupElem.generate method')
        old_group = set(others) | {self}
        fin_group_logger.debug('Generating set has size %d' % len(old_group))
        while True:
            new_group = old_group | set(a * b for a in old_group for b in old_group)
            fin_group_logger.debug('New set has size %d' % len(new_group))
            if old_group == new_group: break
            else: old_group = new_group

        return tuple(new_group)

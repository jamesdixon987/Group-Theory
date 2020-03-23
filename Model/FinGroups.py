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

    @classmethod
    def get_inverse(cls, element, group):
        fin_group_logger.info('Initiating FinGroup class method get_inverse')
        for other in group.elements:
            fin_group_logger.debug('Testing %s' % other)
            if other * element == group.identity:
                return other

        raise ValueError(element)

    @classmethod
    def get_identity(cls, elements):
        fin_group_logger.info('Initiating FinGroup class method get_identity')
        for element in elements:
            if (cls.is_identity(element, elements)):
                fin_group_logger.info('Identity found')
                return element
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
     * pow - power group operation

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

    def inverse(self, group):
        assert(isinstance(group, FinGroup))
        assert(self in group.elements)
        if self._inverse_holder == None:
            self._inverse_holder = FinGroup.get_inverse(self, group)
            return self._inverse_holder
        else: return self._inverse_holder

    def order(self):
        return FinGroup.get_elem_order(self, group_identity(self))

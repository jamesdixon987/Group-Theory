import logging

group_logger = logging.getLogger('group_logger')
group_logger.info('group_logger created')

class Group:

    """
    WITHIN EACH SUBCLASS OF GROUP, THE FOLLOWING MUST BE DEFINED:

    Attributes:
    * .type
    * .group_description


    Operations:

    Methods:

    """

    def __init__(self, identity = None, type = None, group_description = None, finite = False):
        group_logger.info('Initiating Group object')

        self.finite = finite

        self.type = type

        self.group_description = group_description

        self.identity = identity

    def __contains__(self, item):
        assert isinstance(item, GroupElem)
        return any(item == element for element in self.elements)

    def __hash__(self):
        return hash(str(self.elements))

    # def __eq__(self, other):
    #     test_equal = all(
    #                     any(other_elem == self_elem for other_elem in other.elements)
    #                                 for self_elem in self.elements)

    def operation(self, first_element, second_element):
        assert(first_element in self.elements and second_element in self.elements)
        return first_element * second_element

    @classmethod
    def is_identity(cls, possible_id) -> bool:
        group_logger.info('Initiating FinGroup class method is_identity')
        if possible_id * possible_id == possible_id:
            return True
        else: return False

    @classmethod
    def is_inverse(cls, first_elem, second_elem) -> bool:
        assert (isinstance(first_elem, GroupElem))
        assert (isinstance(second_elem, GroupElem))
        group_logger.info('Initiating FinGroup class method is_inverse')
        return cls.is_identity(first_elem * second_elem)

class GroupElem:

    """
    WITHIN EACH SUBCLASS OF GROUPELEM, THE FOLLOWING MUST BE DEFINED:

    Attributes:
     * .display - a unique (within group) display of the element. Used for __eq__ & __ne__

     Operations:

     Methods:
     """


    def __init__(self, group_type=None):

        group_logger.info('Initiating Group object')

        self._inverse_holder = None

        self.group_type = group_type

    def __eq__(self, other):
        group_logger.debug('1st element is %s, 2nd element is %s' %(str(self.display), str(other.display)))
        return self.display == other.display

    def __ne__(self, other):
        group_logger.debug('1st element is %s, 2nd element is %s' %(str(self.display), str(other.display)))
        return not self.display == other.display

    def __str__(self):
        return str(self.display)

    def __hash__(self):
        return hash(self.display)

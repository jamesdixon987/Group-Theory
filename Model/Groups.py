import logging

group_logger = logging.getLogger('group_logger')
group_logger.info('group_logger created')

class Group:

    """
    WITHIN EACH SUBCLASS OF GROUP, THE FOLLOWING MUST BE DEFINED:

    Attributes:

     Operations:

     Methods:
     """

    def __init__(self):
        group_logger.info('Initiating Group object')

        self.elements = []

    def __hash__(self):
        return hash(self.elements)

    @classmethod
    def is_identity(cls, possible_id) -> bool:
        group_logger.info('Initiating FinGroup class method is_identity')
        if possible_id * possible_id == possible_id:
            return True
        else: return False

class GroupElem:

    """
    WITHIN EACH SUBCLASS OF GROUPELEM, THE FOLLOWING MUST BE DEFINED:

    Attributes:
     * .display - a unique (within group) display of the element. Used for __eq__ & __ne__

     Operations:

     Methods:
     """


    def __init__(self):

        group_logger.info('Initiating Group object')

        self._inverse_holder = None

        self.group_type = None

    def __eq__(self, other):
        group_logger.debug('1st element is %s, 2nd element is %s' %(str(self.display), str(other.display)))
        group_logger.info('%s group_order %s' % (str(self.display), self.group_order))
        group_logger.info('%s group_order %s' % (str(self.display), other.group_order))
        assert(self.group_order == other.group_order)
        group_logger.debug('Elements are from symmetric group of group_order %d' % self.group_order)
        return self.display == other.display

    def __ne__(self, other):
        group_logger.debug('1st element is %s, 2nd element is %s' %(str(self.display), str(other.display)))
        return not self.display == other.display

    def __str__(self):
        return str(self.display)

    def __hash__(self):
        return hash(self.display)

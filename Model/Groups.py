import logging

group_logger = logging.getLogger('group_logger')
group_logger.info('group_logger created')

class Group:
    def __init__(self, identity = None, type = None, group_description = None, finite = False):
        group_logger.info('Initiating Group object')

        self.finite = finite

        self.type = type

        self.group_description = group_description

        self.identity = identity

    def __contains__(self, item):
        return any(item == element for element in self.elements)

    def __hash__(self):
        return hash(str(self.elements))

    def __eq__(self, other):
        test_equal = all(
                        any(other_elem == self_elem for other_elem in other.elements)
                                    for self_elem in self.elements)
        return test_equal

    def operation(self, first_element, second_element):
        if first_element in self.elements and second_element in self.elements:
            return first_element * second_element
        else: raise ValueError('group operation must be called with elements of the group')

    @classmethod
    def is_identity(cls, possible_id) -> bool:
        if isinstance(possible_id, GroupElem):
            if possible_id * possible_id == possible_id:
                return True
            else: return False
        else: raise TypeError('GroupElem objects expected')

    @classmethod
    def is_inverse(cls, first_elem, second_elem) -> bool:
        if isinstance(first_elem, GroupElem) and isinstance(second_elem, GroupElem):
            return cls.is_identity(first_elem * second_elem)
        else: raise TypeError('GroupElem objects expected')

class GroupElem:
    def __init__(self, group_type=None):

        group_logger.info('Initiating Group object')

        self._inverse_holder = None

        self.group_type = group_type

    def __eq__(self, other):
        if isinstance(self, GroupElem) and isinstance(other, GroupElem):
            return self.display == other.display

    def __ne__(self, other):
        return not self.display == other.display

    def __str__(self):
        return str(self.display)

    def __hash__(self):
        return hash(self.display)

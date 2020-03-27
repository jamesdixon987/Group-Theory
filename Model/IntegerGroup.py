import logging
from Model.Groups import Group
from Model.Groups import GroupElem

integer_group_logger = logging.getLogger('integer_group_logger')
integer_group_logger.info('integer_group_logger created')

class IntegerGroup(Group):
    integer_group_logger.info('Initiating IntegerGroup class')

    def __init__(self):
        integer_group_logger.info('Initiating IntegerGroup object')

        self.elements = [IntegerGroupElem(-1, self, _from_IntegerGroup_init = True),
                         IntegerGroupElem(0, self, _from_IntegerGroup_init = True),
                         IntegerGroupElem(1, self, _from_IntegerGroup_init = True)]

        for elem in self.elements:
            elem.group_identity = self.elements[1]
        self.identity = self.elements[1]

        self._current_element_list = {-1, 0, 1}

        self.type = 'Integer'
        self.group_description =  'Integers under addition'

        integer_group_logger.warning('IntegerGroup is initialised with a current element list of {-1, 0, 1}. Other elements are added as needed. ')

    def __call__(self, called_integer_element):
        integer_group_logger.info('Initiating IntegerGroup call')
        assert(isinstance(called_integer_element, int))

        called_integer_element_object = IntegerGroupElem(called_integer_element, self)

        if self.check_integer_initialised(called_integer_element):
            return called_integer_element_object
        else:
            self.initialise_integer(called_integer_element_object)
            return called_integer_element_object

    def check_integer_initialised(self, new_poss_integer):
        assert(isinstance(new_poss_integer, int) or isinstance(new_poss_integer, IntegerGroupElem))

        if isinstance(new_poss_integer, int):
            return new_poss_integer in self._current_element_list
        elif isinstance(new_poss_integer, IntegerGroupElem):
            return new_poss_integer.value in self._current_element_list

    def initialise_integer(self, new_integer_element):
        assert(isinstance(new_integer_element, int) or isinstance(new_integer_element, IntegerGroupElem))
        assert(not self.check_integer_initialised(new_integer_element))

        if isinstance(new_integer_element, int):
            self._current_element_list.add(new_integer_element)
            self.elements.append(IntegerGroupElem(new_integer_element, self))

        elif isinstance(new_integer_element, IntegerGroupElem):
            self._current_element_list.add(new_integer_element.value)
            self.elements.append(new_integer_element)
            new_integer_element.associated_group = self

    def get_inverse(self, integer_element):
        assert(integer_element in self._current_element_list)
        return self(-integer_element)


class IntegerGroupElem(GroupElem):
    integer_group_logger.info('Initiating IntegerGroupElem class')

    def __init__(self, new_integer, associated_group = None, _from_IntegerGroup_init = False):
        assert(isinstance(new_integer, int))
        integer_group_logger.info('Initiating IntegerGroupElem object %d' %new_integer)

        GroupElem.__init__(self)

        self.display = '%d in %s' %(new_integer, u'\u2124')

        self.value = new_integer

        self.group_type = 'Integer'

        self.associated_group = associated_group

        if _from_IntegerGroup_init:
            self.group_identity = None
        else: self.group_identity = None if associated_group == None else self.associated_group.identity

        integer_group_logger.debug('associated group is %s' %associated_group)

    def __mul__(self, other):
        assert(isinstance(other, IntegerGroupElem))
        integer_group_logger.debug('Operation on %s and %s' %(self.display, other.display))

        if self.associated_group is not None:
            result = IntegerGroupElem(self.value + other.value, self.associated_group)
            if not self.associated_group.check_integer_initialised(result):
                self.associated_group.initialise_integer(result)
        else: result = IntegerGroupElem(self.value + other.value)
        return result

    def inverse(self):
        integer_group_logger.debug('Initialising IntegerGroupElem.inverse method')
        try:
            assert(self.associated_group is not None)
            integer_group_logger.debug('Element has associated group %s' %self.associated_group)
        except AssertionError:
            integer_group_logger.error('Cannot find inverse if element has no associated group')
            raise AttributeError
        return self.associated_group(-self.value)



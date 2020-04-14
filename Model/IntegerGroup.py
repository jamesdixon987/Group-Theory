import logging
from Model.Groups import Group
from Model.Groups import GroupElem

integer_group_logger = logging.getLogger('integer_group_logger')
integer_group_logger.info('integer_group_logger created')

class IntegerGroup(Group):

    def __init__(self):

        self.elements = [IntegerGroupElem(-1, self, _from_IntegerGroup_init = True),
                         IntegerGroupElem(0, self, _from_IntegerGroup_init = True),
                         IntegerGroupElem(1, self, _from_IntegerGroup_init = True)]

        for elem in self.elements:
            elem.group_identity = self.elements[1]

        self._current_element_list = {-1, 0, 1}

        super().__init__(identity = self.elements[1], type = 'Integer',
                       group_description = 'Integers under addition', finite = False)

        integer_group_logger.info('IntegerGroup is initialised with a current element list of {-1, 0, 1}. '
                                     'Other elements are added as needed. ')

    def __call__(self, called_integer_element):
        integer_group_logger.info('Initiating IntegerGroup call')
        assert(isinstance(called_integer_element, int))

        called_integer_element_object = IntegerGroupElem(called_integer_element, self)

        if self.check_integer_initialised(called_integer_element):
            pass
        else: self.initialise_integer(called_integer_element_object)
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

        super().__init__(group_type = 'Integer')

        self.display = '%d in %s' %(new_integer, u'\u2124')

        self.value = new_integer

        self.associated_group = associated_group

        if _from_IntegerGroup_init:
            self.group_identity = None
        else: self.group_identity = None if associated_group is None else self.associated_group.identity

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

    def __pow__(self, power):
        assert(isinstance(power, int))
        return self.associated_group(self.value * power)

    def inverse(self):
        integer_group_logger.debug('Initialising IntegerGroupElem.inverse method')
        if self.associated_group is None:
            error_message = 'Cannot find inverse if element has no associated group'
            integer_group_logger.error(error_message)
            raise AttributeError(error_message)

        integer_group_logger.debug('Element has associated group %s' %self.associated_group)
        return self.associated_group(-self.value)



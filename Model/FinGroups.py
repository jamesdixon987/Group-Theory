import logging

fin_group_logger = logging.getLogger('fin_group_logger')
fin_group_logger.info('fin_group_logger created')

class FinGroup:
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
                return element

        raise ValueError()

    @classmethod
    def is_identity(cls, possible_id, elements) -> bool:
        fin_group_logger.info('Initiating FinGroup class method is_identity')
        for element in elements:
            if not possible_id * element == element:
                return False

        return True


class FinGroupElement:
    def __init__(self, element):
        self.element = element

    def __eq__(self, other):
        return self.element == other.element

    def __str__(self):
        return f"Group element: {str(self.element)}"

    def __pow__(self, element, power):
        if (power == 0):
            return self.group_id
        elif power > 0:
            return element * pow(element, power - 1)
        else:
            return self.inverse[pow(element, -power)]

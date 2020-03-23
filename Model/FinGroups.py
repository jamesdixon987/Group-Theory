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





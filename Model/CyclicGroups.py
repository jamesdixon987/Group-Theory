import logging
from Model.FinGroups import FinGroup
from Model.FinGroups import FinGroupElem

cyc_logger = logging.getLogger('cyc_logger')
cyc_logger.info('Cyc logger created')


class CycGroup(FinGroup):
    cyc_logger.info('Initiating CycGroup class')

    def __init__(self, order):
        assert(isinstance(order, int) and order > 1)

        self.order = order
        cyc_logger.debug('order is %d' % order)

        element_list = tuple(range(order))
        cyc_logger.debug('element list created')
        self.elements = tuple(CycGroupElem(g, self.order, associated_group=self) for g in element_list)
        cyc_logger.debug('self.elements created')

        super().__init__(self.elements, type = 'Cyclic', group_description = 'Cyclic order %d' % order)

        cyc_logger.info('Symmetric group of order %d created' % order)

    cyc_logger.info('CycGroup class defined')


class CycGroupElem(FinGroupElem):
    cyc_logger.info('Initiating CycGroupElem class')

    def __init__(self, ZnInt, group_order, associated_group = None):
        cyc_logger.debug('Creating instance of CycGroupElem')
        assert(isinstance(ZnInt, int))
        assert(ZnInt >= 0)

        try:
            assert(group_order > ZnInt)
        except AssertionError:
            cyc_logger.warning(' %d is too large and  will be reduced modulo %d, resulting in %d.'
                               % (ZnInt, group_order, ZnInt % group_order))
            ZnInt = ZnInt % group_order

        super().__init__(associated_group = associated_group)

        self.group_order = group_order
        cyc_logger.debug('Group is order %d' % group_order)

        self._number = ZnInt

        self.display = "%s (mod %s)" % (ZnInt, group_order)
        self._element_holder = ZnInt

        self.group_type = 'Cyclic'
    cyc_logger.info('CycGroupElem class defined')

    def __mul__(self, second):
        cyc_logger.debug('1st element is %s, 2nd element is %s' % (str(self.display), str(second.display)))
        assert(isinstance(second, CycGroupElem))
        try:
            assert(self.group_order == second.group_order)
        except AssertionError:
            cyc_logger.error('Groups of elements are of different sizes')
            raise TypeError
        cyc_logger.debug('Elements are from cyclic group of group_order %d' % self.group_order)
        result = (self._number + second._number) % self.group_order
        cyc_logger.debug('result is %s' % (str(result)))
        if self.associated_group is None:
            return CycGroupElem(result, self.group_order)
        else:
            return self.associated_group(result)

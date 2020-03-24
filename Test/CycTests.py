import unittest

from Model.CyclicGroups import CycGroup
from Model.CyclicGroups import CycGroupElem
from Model.FinGroups import FinGroup
from Model.FinGroups import FinGroupElem


class test_group(unittest.TestCase):
    def test_cyc_group(self):
        for n in range(2, 12):
            C = CycGroup(n)
            self.assertEqual(C.order, n)
            self.assertEqual(len(C.elements), n)
            self.assertTrue(isinstance(C.elements, tuple))
            self.assertEqual(C.identity, CycGroupElem(0, n))

            iter_group = iter(C)
            count = 0
            while count < n:
                a = next(iter_group)
                self.assertTrue(FinGroup.get_inverse(a, C) * a == C.identity)
                count += 1

    def test_cyc_group_elem(self):
        C = CycGroup(4)
        element = CycGroupElem(2, 4)
        self.assertTrue(C.identity == CycGroupElem(0, 4))
        for n in [0, 1, 2, 3]:
            elem = CycGroupElem(n, 4)
            elem.associated_group = C
            self.assertIn(elem, C.elements)
            self.assertEqual(elem.group_order, C.order)
            self.assertEqual(elem.display, '%d (mod 4)' %n)
            self.assertEqual(CycGroupElem.inverse(elem, C) * elem, C.identity)
            self.assertTrue(elem == elem)
            self.assertFalse(elem != elem)
            self.assertTrue(elem**2 == elem * elem)
            self.assertEqual(elem**-2,FinGroup.get_inverse(elem**2, C))

import unittest

from math import factorial
from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.FinGroups import FinGroup
from Model.FinGroups import FinGroupElem


class test_group(unittest.TestCase):
    def test_sym_group(self):
        for n in range(2, 8):
            S = SymGroup(n)
            self.assertEqual(S.order, n)
            self.assertEqual(len(S.elements), factorial(n))
            self.assertEqual(S.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertTrue(all(FinGroup.get_inverse(a) * a == S.identity) for a in S.elements)

    def test_sym_group_elem(self):
        S = SymGroup(4)
        element = SymGroupElem((2,1,4,3))
        self.assertTrue(S.identity == SymGroupElem((1,2,3,4)))
        self.assertEqual(SymGroupElem.get_cycle_representation(element), ((1,2),(3,4)))
        self.assertEqual(element.cycle_type, (2,2))
        for n in [(1,2,3,4), (1,2,4,3), (3,2,1,4), (3,2,4,1)]:
            elem = SymGroupElem(n)
            elem.associated_group = S
            self.assertIn(elem, S.elements)
            self.assertEqual(elem.group_order, S.order)
            self.assertEqual(n, elem.display)
            self.assertEqual(SymGroupElem.inverse(elem, S) * elem, S.identity)
            self.assertTrue(elem == elem)
            self.assertFalse(elem != elem)
            self.assertEqual(elem**-2,FinGroup.get_inverse(elem**2, S))


if __name__ == "__main__":
    unittest.main()

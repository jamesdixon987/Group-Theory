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

    def test_sym_group_elem(self):
        S = SymGroup(4)
        fixed_element = SymGroupElem((2,1,4,3))

        self.assertTrue(S.identity == SymGroupElem((1,2,3,4)))

        self.assertEqual(SymGroupElem.get_cycle_representation(fixed_element), ((1,2),(3,4)))
        self.assertEqual(SymGroupElem.cycle_type(fixed_element), (2,2))

        for n in [(1,2,3,4), (1,2,4,3), (3,2,1,4), (3,2,4,1)]:
            elem = SymGroupElem(n)
            elem.associated_group = S

            self.assertIn(elem, S.elements)
            self.assertEqual(elem.group_order, S.order)
            self.assertEqual(elem.group_type, 'Symmetric')

            self.assertEqual(n, elem.tuple_rep)
            self.assertEqual(S.operation(elem, fixed_element), elem * fixed_element)
            self.assertEqual(SymGroupElem.inverse(elem, S) * elem, S.identity)
            self.assertTrue(elem == elem)
            self.assertFalse(elem != elem)
            self.assertTrue(elem**2 == elem * elem)
            self.assertEqual(elem**-2,FinGroup.get_inverse(elem**2, S))


if __name__ == "__main__":
    unittest.main()

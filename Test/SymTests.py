import unittest

from math import factorial
from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.SymmetricGroups import DiGroup

class test_group(unittest.TestCase):
    def test_sym_group(self):
        for n in range(2, 7):
            S = SymGroup(n)
            self.assertTrue(S.finite)
            self.assertEqual(S.order, n)
            self.assertEqual(len(S.elements), factorial(n))
            self.assertEqual(S.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertTrue(S.is_identity(S.identity))

    def test_sym_group_elem(self):
        S = SymGroup(4)
        fixed_element = SymGroupElem((2,1,4,3))

        self.assertTrue(S.identity == SymGroupElem((1,2,3,4)))

        self.assertEqual(SymGroupElem.get_cycle_representation(fixed_element), ((1,2),(3,4)))
        self.assertEqual(SymGroupElem.cycle_type(fixed_element), (2,2))
        self.assertEqual(fixed_element.get_elem_order(group = S), 2)

        for n in [(1,2,3,4), (1,2,4,3), (3,2,1,4), (3,2,4,1)]:
            elem = SymGroupElem(n)
            elem.associated_group = S

            self.assertIn(elem, S.elements)
            self.assertEqual(elem.group_order, S.order)
            self.assertEqual(elem.group_type, 'Symmetric')

            self.assertEqual(n, elem._element_holder)

    def test_dih_group(self):
        for n in range(3, 12):
            D = DiGroup(n)
            self.assertTrue(D.finite)
            self.assertEqual(D.order, n)
            self.assertEqual(D.size(), 2 * n)
            self.assertEqual(len(D.elements), 2 * n)
            self.assertEqual(D.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertEqual(D.elements[2].group_type, 'Dihedral')

if __name__ == "__main__":
    unittest.main()

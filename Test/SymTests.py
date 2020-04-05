import unittest

from math import factorial
from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.SymmetricGroups import DiGroup
from Model.SymmetricGroups import AltGroup


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
        fixed_element2 = SymGroupElem((2,3,4,1))

        self.assertTrue(S.identity == SymGroupElem((1,2,3,4)))

        self.assertTrue(S(fixed_element) in S)
        self.assertTrue(S(fixed_element2) in S)
        self.assertTrue(fixed_element in S)
        self.assertTrue(fixed_element2 in S)


        self.assertEqual(fixed_element.cycles(), ((1,2),(3,4)))
        self.assertEqual(fixed_element.cycle_type(), (2,2))
        self.assertEqual(fixed_element.get_elem_order(), 2)
        self.assertEqual(fixed_element.permutation_parity(), 1)

        self.assertEqual(fixed_element2.cycles(), ((1,2,3,4),))
        self.assertEqual(fixed_element2.cycle_type(), (4,))
        self.assertEqual(fixed_element2.get_elem_order(), 4)
        self.assertEqual(fixed_element2.permutation_parity(), -1)

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

    def test_alt_group(self):
        for n in range(3, 7):
            A = AltGroup(n)

            self.assertTrue(A.finite)
            self.assertEqual(A.order, n)
            self.assertEqual(A.size(), factorial(n)/2)
            self.assertEqual(len(A.elements), factorial(n)/2)
            self.assertEqual(A.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertEqual(A.elements[1].group_type, 'Alternating')

if __name__ == "__main__":
    unittest.main()

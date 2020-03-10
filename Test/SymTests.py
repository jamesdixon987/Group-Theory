import unittest

from math import factorial
from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.FinGroups import FinGroup


class test_group(unittest.TestCase):
    def test_sym_group(self):
        for n in range(2, 10):
            S = SymGroup(n)
            self.assertEqual(S.order, n)
            self.assertEqual(len(S.elements), factorial(n))
            self.assertEqual(S.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertTrue(all(FinGroup.get_inverse(a) * a == S.identity) for a in S.elements)

    def test_sym_group_elem(self):
        for n in [(1,2,3,4), (1,2,4,3), (3,2,1,4), (3,2,4,1)]:
            elem = SymGroupElem(n)
            S = SymGroup(4)
            self.assertIn(elem, S.elements)
            self.assertEqual(elem.group_order, S.order)
            self.assertEqual(n, elem.display)
            self.assertEqual(elem.group_identity, S.identity)
            self.assertEqual(elem.group_identity, elem * elem.inverse(S))


if __name__ == "__main__":
    unittest.main()

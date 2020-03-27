import unittest

from math import factorial
from Model.IntegerGroup import IntegerGroup
from Model.IntegerGroup import IntegerGroupElem


class test_group(unittest.TestCase):
    def test_int_group(self):
        Z = IntegerGroup()
        self.assertEqual(Z.identity, Z(0))
        self.assertTrue(Z.is_identity(Z.identity))
        for elem in Z.elements:
            self.assertTrue(isinstance(elem, IntegerGroupElem))
            self.assertTrue(Z.check_integer_initialised(elem))

    def test_int_group_elem(self):
        Z = IntegerGroup()
        fixed_elem = Z(100)
        self.assertIn(fixed_elem.inverse(), Z.elements)
        self.assertIn(fixed_elem, Z.elements)

        loose_elem = IntegerGroupElem(553)
        self.assertNotIn(loose_elem, Z.elements)
        self.assertIs(loose_elem.associated_group, None)
        self.assertEqual(loose_elem.value, 553)

        for n in range(1, 8):
            elem = Z.elements[2] ** n
            self.assertIn(elem, Z.elements)
            self.assertIs(elem.group_identity, Z.identity)
            self.assertEqual(elem.value, n)

            self.assertIn(fixed_elem * elem, Z.elements)
            self.assertEqual(fixed_elem * elem, elem * fixed_elem)

            neg_elem = Z(-n)
            self.assertTrue(Z.is_inverse(neg_elem, elem))
            self.assertTrue(Z.is_inverse(elem, neg_elem))
            self.assertEqual(neg_elem.value, -n)
            self.assertEqual(neg_elem.value, -elem.value)





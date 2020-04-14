import unittest

import logging
group_test_logger = logging.getLogger('group_test_logger')
logging.basicConfig(level=logging.WARNING)
group_test_logger.info('group_test_logger created')

from math import factorial
from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.SymmetricGroups import DiGroup
from Model.SymmetricGroups import AltGroup
from Model.CyclicGroups import CycGroup
from Model.CyclicGroups import CycGroupElem
from Model.FinGroups import FinGroup
from Model.IntegerGroup import IntegerGroup
from Model.IntegerGroup import IntegerGroupElem


class test_sym_groups(unittest.TestCase):

    def test_basic_sym_group(self):
        for n in range(2, 7):
            S = SymGroup(n)
            self.assertTrue(S.finite)
            self.assertEqual(S.order, n)
            self.assertEqual(len(S.elements), factorial(n))
            self.assertEqual(S.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertTrue(S.is_identity(S.identity))

    def test_basic_dih_group(self):
        for n in range(3, 12):
            D = DiGroup(n)

            self.assertTrue(D.finite)
            self.assertEqual(D.order, n)
            self.assertEqual(D.size(), 2 * n)
            self.assertEqual(len(D.elements), 2 * n)
            self.assertEqual(D.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertEqual(D.elements[1].group_type, 'Dihedral')

    def test_basic_alt_group(self):
        for n in range(3, 7):
            A = AltGroup(n)

            self.assertTrue(A.finite)
            self.assertEqual(A.order, n)
            self.assertEqual(A.size(), factorial(n)/2)
            self.assertEqual(len(A.elements), factorial(n)/2)
            self.assertEqual(A.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertEqual(A.elements[1].group_type, 'Alternating')

    global fixed_element
    global fixed_element2
    global S
    S = SymGroup(4)
    fixed_element = SymGroupElem((2,1,4,3))
    fixed_element2 = SymGroupElem((2,3,4,1))

    def test_basic_sym_group_elem(self):

        self.assertTrue(isinstance(fixed_element, SymGroupElem))
        self.assertTrue(isinstance(fixed_element2, SymGroupElem))
        self.assertTrue(S.identity == SymGroupElem((1,2,3,4)))

    def test_sym_group_elem_cycles_parity(self):
        self.assertEqual(fixed_element.cycles(), ((1,2),(3,4)))
        self.assertEqual(fixed_element.cycle_type(), (2,2))
        self.assertEqual(fixed_element.get_elem_order(), 2)
        self.assertEqual(fixed_element.permutation_parity(), 1)

        self.assertEqual(fixed_element2.cycles(), ((1,2,3,4),))
        self.assertEqual(fixed_element2.cycle_type(), (4,))
        self.assertEqual(fixed_element2.get_elem_order(), 4)
        self.assertEqual(fixed_element2.permutation_parity(), -1)

    def test_sym_group_elems_in_group(self):
        self.assertTrue(S(fixed_element) in S)
        self.assertTrue(S(fixed_element2) in S)
        self.assertTrue(fixed_element in S)
        self.assertTrue(fixed_element2 in S)

        for n in [(1,2,3,4), (1,2,4,3), (3,2,1,4), (3,2,4,1)]:
            elem = SymGroupElem(n)
            elem.associated_group = S

            self.assertIn(elem, S.elements)
            self.assertEqual(elem.group_order, S.order)
            self.assertEqual(elem.group_type, 'Symmetric')

            self.assertEqual(n, elem._element_holder)


class test_cyc_groups(unittest.TestCase):

    def test_cyc_group(self):
        for n in range(2, 12):
            C = CycGroup(n)

            self.assertTrue(C.finite)
            self.assertEqual(C.type, 'Cyclic')
            self.assertTrue(C.is_abelian())

            self.assertEqual(C.order, n)
            self.assertEqual(len(C.elements), n)
            self.assertTrue(isinstance(C.elements, tuple))

            self.assertEqual(C.identity, CycGroupElem(0, n))

            self.assertEqual(C.elements[0].associated_group, C)

            iter_group = iter(C)
            count = 0
            while count < n:
                a = next(iter_group)
                self.assertTrue(FinGroup.get_inverse(a, C) * a == C.identity)
                self.assertTrue(a in C)
                count += 1

    def test_cyc_group_elem(self):
        C = CycGroup(4)
        fixed_element = CycGroupElem(2, 4)
        self.assertTrue(C.identity == CycGroupElem(0, 4))
        for n in [0, 1, 2, 3]:
            elem = CycGroupElem(n, 4)
            elem.associated_group = C
            self.assertEqual(elem._number, n)
            self.assertEqual(elem._element_holder, n)
            self.assertIn(elem, C.elements)
            self.assertIn(elem, C)
            self.assertIn(elem * fixed_element, C)
            self.assertEqual(elem.group_order, C.order)
            self.assertEqual(elem.display, '%d (mod 4)' %n)


class test_int_group(unittest.TestCase):
    global Z, fixed_elem
    Z = IntegerGroup()
    fixed_elem = Z(100)

    def test_int_group_basic(self):
        self.assertEqual(Z.type, 'Integer')
        self.assertEqual(Z.group_description, 'Integers under addition')
        self.assertFalse(Z.finite)

    def test_int_group_calling(self):
        self.assertEqual(Z.identity, Z(0))
        self.assertTrue(Z.is_identity(Z.identity))

        self.assertFalse(Z.check_integer_initialised(8))
        fixed_elem = Z(8)
        self.assertTrue(Z.check_integer_initialised(8))
        self.assertIn(fixed_elem, Z.elements)
        self.assertIn(8, Z._current_element_list)

        self.assertFalse(Z.check_integer_initialised(-8))
        Z.initialise_integer(-8)
        self.assertTrue(Z.check_integer_initialised(-8))

        self.assertEqual(Z(-8), Z.get_inverse(8))
        Z.initialise_integer(9)
        self.assertEqual(Z(-9), Z.get_inverse(9))

        for elem in Z.elements:
            self.assertTrue(isinstance(elem, IntegerGroupElem))
            self.assertTrue(Z.check_integer_initialised(elem))

    def test_int_group_elem_basic(self):

        self.assertIn(fixed_elem.inverse(), Z.elements)
        self.assertIn(fixed_elem, Z.elements)

        for n in range(1, 8):
            elem = Z.elements[2] ** n
            self.assertIn(elem, Z.elements)
            self.assertIn(n, Z._current_element_list)
            self.assertIs(elem.group_identity, Z.identity)
            self.assertEqual(elem.value, n)

            self.assertIn(fixed_elem * elem, Z.elements)
            self.assertEqual(fixed_elem * elem, elem * fixed_elem)

            neg_elem = Z(-n)
            self.assertTrue(Z.is_inverse(neg_elem, elem))
            self.assertTrue(Z.is_inverse(elem, neg_elem))
            self.assertEqual(neg_elem.value, -n)
            self.assertEqual(neg_elem.value, -elem.value)

    def test_int_group_elem_loose(self):
        loose_elem = IntegerGroupElem(553)
        self.assertNotIn(loose_elem, Z.elements)
        self.assertIs(loose_elem.associated_group, None)
        self.assertEqual(loose_elem.value, 553)


class test_groups(unittest.TestCase):
    global group_list, inf_group_list
    group_list = []
    # Please note that groups must have size at least 5 to be added to this list.
    for n in range(4,7):
        group_list.append(SymGroup(n))
        group_list.append(AltGroup(n))
    for n in range(7, 12):
        generated_group_creator1 = list(range(2,n))
        generated_group_creator1.append(1)
        group_list.append(SymGroupElem.generate(SymGroupElem(tuple(generated_group_creator1))))

        group_list.append(CycGroup(n))
        group_list.append(DiGroup(n))

    group_list.append(SymGroupElem.generate(
        SymGroupElem((2,3,4,5,1)),SymGroupElem((2,1,4,3,5))))

    group_list.append(FinGroup.direct_product(SymGroup(3), DiGroup(3)))
    group_list.append(FinGroup.direct_product(CycGroup(5), DiGroup(4)))
    group_list.append(FinGroup.direct_product(SymGroup(3), CycGroup(4)))

    def test_list_finite_groups_basic(self):
        for G in group_list:
            self.assertTrue(isinstance(G.elements, tuple))
            self.assertEqual(G.size(), len(G.elements))
            self.assertTrue(G.finite)

    def test_list_finite_groups_elems(self):
        for G in group_list:
            fixed_element = G.elements[1]

            iter_group = iter(G)
            count = 0
            while count < 5:
                elem = next(iter_group)

                self.assertIn(elem, G.elements)
                self.assertIs(elem, G(elem._element_holder))
                self.assertIs(elem.associated_group, G)

                self.assertEqual(G.get_inverse(elem, G) * elem, G.identity)

                self.assertEqual(G.operation(elem, fixed_element), elem * fixed_element)

                self.assertTrue(elem == elem)
                self.assertFalse(elem != elem)

                self.assertIs(elem, elem**1)
                self.assertIs(elem.inverse(), elem**-1)
                self.assertTrue(elem**2 == elem * elem)
                self.assertEqual(elem**-2,G.get_inverse(elem**2, G))

                count += 1

    inf_group_list = group_list[1:]
    inf_group_list.append(IntegerGroup())

    def test_all_groups_basic(self):
        for G in inf_group_list:

            self.assertTrue(isinstance(hash(G), int))
            self.assertIsNot(G.type, None)
            self.assertIsNot(G.group_description, None)

    def test_all_groups_elems(self):
        for G in inf_group_list:

            elem1 = G.elements[0]
            elem2 = G.elements[1]

            self.assertTrue(G.is_identity(G.identity))
            self.assertTrue(G.is_inverse(elem1, elem1.inverse()))
            self.assertTrue(G.is_inverse(elem2, elem2.inverse()))

            self.assertTrue(isinstance(G.elements, tuple) or isinstance(G.elements, list))
            self.assertTrue(elem1 in G)

            self.assertEqual(elem1.associated_group, G)
            self.assertEqual(elem1.associated_group, elem2.associated_group)

            self.assertEqual(elem1 * elem1, G.operation(elem1, elem1))
            self.assertEqual(elem1 * elem2, G.operation(elem1, elem2))
            self.assertEqual(elem2 * elem1, G.operation(elem2, elem1))
            self.assertEqual(elem2 * elem2, G.operation(elem2, elem2))

            self.assertIsNot(elem1.group_type, None)
            self.assertEqual(elem1.group_type, elem2.group_type)

    def test_generate(self):
        self.assertEqual(SymGroup(4), SymGroupElem.generate(SymGroupElem((2,1,3,4)), SymGroupElem((2,3,4,1))))
        self.assertEqual(2, len(SymGroupElem.generate(SymGroupElem((2,1,3,4))).elements))
        self.assertEqual(4, len(SymGroupElem.generate(SymGroupElem((2,3,4,1))).elements))

    def test_subgroups_and_homomorphisms(self):
        G = SymGroup(4)

        N1 = SymGroupElem.generate(SymGroupElem((2,1,3,4)), SymGroupElem((2,3,4,1)))
        N2 = SymGroupElem.generate(SymGroupElem((1,3,4,2)), SymGroupElem((2,3,1,4)),
                                       SymGroupElem((4,2,1,3)), SymGroupElem((4,1,3,2)))
        N3 = AltGroup(4)

        H1 = SymGroupElem.generate(SymGroupElem((2,1,3,4)))
        H2 = SymGroupElem.generate(SymGroupElem((2,3,1,4)))

        self.assertTrue(G.is_subgroup(N1))
        self.assertTrue(G.is_subgroup(N2))
        self.assertTrue(G.is_subgroup(N3))
        self.assertTrue(G.is_subgroup(H1))
        self.assertTrue(G.is_subgroup(H2))

        self.assertTrue(G.is_normal_subgroup(N1))
        self.assertTrue(G.is_normal_subgroup(N2))
        self.assertTrue(G.is_normal_subgroup(N3))
        self.assertFalse(G.is_normal_subgroup(H1))
        self.assertFalse(G.is_normal_subgroup(H2))


if __name__ == "__main__":
    unittest.main()

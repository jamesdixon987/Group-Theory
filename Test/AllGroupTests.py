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


class test_groups(unittest.TestCase):
    def test_all_groups(self):
        self.assertEqual(SymGroup(4), SymGroupElem.generate(SymGroupElem((2,1,3,4)), SymGroupElem((2,3,4,1))))
        group_list = [IntegerGroup()]
        for n in range(3,6):
            group_list.append(SymGroup(n))
            group_list.append(AltGroup(n))

        for n in range(7, 12):
            generated_group_creator = list(range(2,n))
            generated_group_creator.append(1)
            group_list.append(SymGroupElem.generate(SymGroupElem(tuple(generated_group_creator))))

            group_list.append(CycGroup(n))
            group_list.append(DiGroup(n))

        for G in group_list:

            elem1 = G.elements[0]
            elem2 = G.elements[1]

            self.assertTrue(isinstance(hash(G), int))
            self.assertIsNot(G.type, None)
            self.assertIsNot(G.group_description, None)

            self.assertTrue(G.is_identity(G.identity))
            self.assertTrue(G.is_inverse(elem1, elem1.inverse()))
            self.assertTrue(G.is_inverse(elem2, elem2.inverse()))

            self.assertTrue(isinstance(G.elements, tuple) or isinstance(G.elements, list))
            self.assertTrue(elem1 in G)

            self.assertEqual(elem1.associated_group, G)
            self.assertEqual(elem1.associated_group, elem2.associated_group)

            self.assertEqual(elem1 * elem2, G.operation(elem1, elem2))
            self.assertEqual(elem1 * elem1, G.operation(elem1, elem1))
            self.assertEqual(elem2 * elem1, G.operation(elem2, elem1))
            self.assertEqual(elem2 * elem2, G.operation(elem2, elem2))

            self.assertNotEqual(elem1.group_type, None)
            self.assertEqual(elem1.group_type, elem2.group_type)

    def test_finite_groups(self):
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

        for G in group_list:

            # if G.generating_set is not None:
            #     self.assertEqual(SymGroupElem.generate(G.generating_set).elements, G.elements)

            self.assertTrue(isinstance(G.elements, tuple))
            self.assertEqual(G.size(), len(G.elements))

            self.assertTrue(G.finite)

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


if __name__ == "__main__":
    unittest.main()

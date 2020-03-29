import unittest

import logging
group_test_logger = logging.getLogger('group_test_logger')
logging.basicConfig(level=logging.WARNING)
group_test_logger.info('group_test_logger created')


from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.SymmetricGroups import DiGroup
from Model.CyclicGroups import CycGroup
from Model.CyclicGroups import CycGroupElem
from Model.FinGroups import FinGroup
from Model.IntegerGroup import IntegerGroup
from Model.IntegerGroup import IntegerGroupElem


class test_group(unittest.TestCase):
    def test_all_groups(self):
        group_list = [IntegerGroup()]
        for n in range(2,6):
            group_list.append(SymGroup(n))

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
        for n in range(3,7):
            group_list.append(SymGroup(n))
        for n in range(7, 12):
            generated_group_creator1 = list(range(2,n))
            generated_group_creator1.append(1)
            group_list.append(SymGroupElem.generate(SymGroupElem(tuple(generated_group_creator1))))

            group_list.append(CycGroup(n))
            group_list.append(DiGroup(n))

        group_list.append(SymGroupElem.generate(
            SymGroupElem((2,3,4,5,1)),SymGroupElem((2,1,4,3,5))))
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


if __name__ == "__main__":
    unittest.main()

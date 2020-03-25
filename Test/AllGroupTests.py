import unittest

from Model.Groups import Group
from Model.Groups import GroupElem
from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.CyclicGroups import CycGroup
from Model.CyclicGroups import CycGroupElem
from Model.FinGroups import FinGroup
from Model.FinGroups import FinGroupElem
from Model.IntegerGroup import IntegerGroup
from Model.IntegerGroup import IntegerGroupElem


class test_group(unittest.TestCase):
    def test_all_groups(self):
        group_list = [IntegerGroup()]
        for n in range(2,6):
            group_list.append(SymGroup(n))
            group_list.append(CycGroup(n))
        for G in group_list:
            elem1 = G.elements[0]
            elem2 = G.elements[1]

            self.assertTrue(isinstance(G.elements, tuple) or isinstance(G.elements, list))

            self.assertEqual(elem1.associated_group, G)
            self.assertEqual(elem1.associated_group, elem2.associated_group)

            self.assertEqual(elem1 * elem2, G.operation(elem1, elem2))
            self.assertEqual(elem1 * elem1, G.operation(elem1, elem1))

            self.assertNotEqual(elem1.group_type, None)
            self.assertEqual(elem1.group_type, elem2.group_type)


    def test_finite_groups(self):
        group_list = []
        # Please note that groups must have size at least 5 to be added to this list.
        for n in range(3,6):
            group_list.append(SymGroup(n))
        for n in range(6, 12):
            group_list.append(CycGroup(n))
        for G in group_list:
            self.assertTrue(isinstance(G.elements, tuple))
            iter_group = iter(G)
            count = 0
            while count < 5:
                a = next(iter_group)
                self.assertTrue(FinGroup.get_inverse(a, G) * a == G.identity)
                count += 1

if __name__ == "__main__":
    unittest.main()

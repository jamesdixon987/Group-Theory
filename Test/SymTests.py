import unittest
import logging
from math import factorial
from Model.SymmetricGroups import SymGroup
from Model.SymmetricGroups import SymGroupElem
from Model.FinGroups import FinGroup

sym_test_logger = logging.getLogger('Sym Test Logger')
logging.basicConfig(level=logging.INFO)
sym_test_logger.info('Sym test logger created')

class test_group(unittest.TestCase):
    sym_test_logger.info('Defining test_group class')
    def test_sym_group(self):
        for n in range(2, 10):
            S = SymGroup(n)
            self.assertEqual(S.order, n)
            self.assertEqual(len(S.elements), factorial(n))
            self.assertEqual(S.identity, SymGroupElem(tuple(range(1, n + 1))))
            self.assertTrue(all(FinGroup.get_inverse(a) * a == S.identity) for a in S.elements)

if __name__ == "__main__":
    unittest.main()

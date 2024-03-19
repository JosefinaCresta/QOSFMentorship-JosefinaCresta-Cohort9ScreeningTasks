import unittest
from src.classical_comparison import less_than_k

class TestClassicalComparison(unittest.TestCase):

    def test_less_than_k(self):
        self.assertEqual(less_than_k(5, [1, 2, 6, 4, 8]), [1, 2, 4])
        self.assertEqual(less_than_k(10, [11, 9, 10, 8]), [9, 8])
        self.assertEqual(less_than_k(0, [-1, -2, 1, 2]), [-1, -2])

if __name__ == '__main__':
    unittest.main()

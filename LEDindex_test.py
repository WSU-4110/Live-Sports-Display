import sys
sys.path.append('C:/Users/17344/Desktop/djangotest')
from unittest import TestCase
from Unit_Testing_Functions import getLedIndex

class TestGetLedIndex(TestCase):

    def test_even_x(self):
        height = 8
        x_even = 2
        y = 3
        expected_index_even = (95 - x_even) * height + y
        self.assertEqual(getLedIndex(x_even, y, height), expected_index_even)

    def test_odd_x(self):
        height = 8
        x_odd = 3
        y = 4
        expected_index_odd = (95 - x_odd) * height + (7 - y)
        self.assertEqual(getLedIndex(x_odd, y, height), expected_index_odd)

    def test_edge_cases(self):
        height = 8
        max_x = 95
        min_x = 0
        y = 0
        expected_index_top_left = (95 - min_x) * height + y  
        self.assertEqual(getLedIndex(min_x, y, height), expected_index_top_left)
        expected_index_top_right = (95 - max_x) * height + (7 - y)  
        self.assertEqual(getLedIndex(max_x, y, height), expected_index_top_right)

if __name__ == '__main__':
    import unittest
    unittest.main()

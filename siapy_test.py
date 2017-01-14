import unittest
from siapy import Sia

class SiaTest(unittest.TestCase):
    def test_get_version(self):
        sia = Sia()
        self.assertEqual(sia.get_version(), '1.0.3')

if __name__ == '__main__':
    unittest.main()

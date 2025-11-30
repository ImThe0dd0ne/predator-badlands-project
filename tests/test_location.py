import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.location import Location


class TestLocation(unittest.TestCase):

    def test_init(self):
        loc = Location(3, 4)
        self.assertEqual(loc.get_x(), 3)
        self.assertEqual(loc.get_y(), 4)

    def test_init_zero(self):
        loc = Location(0, 0)
        self.assertEqual(loc.get_x(), 0)
        self.assertEqual(loc.get_y(), 0)

    def test_setters(self):
        loc = Location(1, 1)
        loc.set_x(5)
        loc.set_y(8)
        self.assertEqual(loc.get_x(), 5)
        self.assertEqual(loc.get_y(), 8)

    def test_equals(self):
        loc1 = Location(3, 4)
        loc2 = Location(3, 4)
        loc3 = Location(5, 6)
        self.assertTrue(loc1.equals(loc2))
        self.assertFalse(loc1.equals(loc3))

    def test_equals_with_non_location(self):
        loc = Location(3, 4)
        self.assertFalse(loc.equals("not a location"))
        self.assertFalse(loc.equals(None))

    def test_str(self):
        loc = Location(3, 4)
        self.assertEqual(str(loc), "Location(x=3, y=4)")


if __name__ == '__main__':
    unittest.main()
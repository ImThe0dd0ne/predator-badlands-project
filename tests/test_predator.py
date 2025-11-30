import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.predator import Predator
from utils.location import Location
from environment.grid import Grid

class PredatorTests(unittest.TestCase):

    def test_predator_creation(self):
        start_pos = Location(5, 5)
        hunter = Predator("Dek", start_pos)
        
        self.assertEqual(hunter.get_name(), "Dek")
        self.assertEqual(hunter.get_honor_score(), 0)
        self.assertEqual(hunter.get_trophy_count(), 0)
        self.assertFalse(hunter.is_carrying())

    def test_honor_goes_up_and_down(self):
        hunter = Predator("Dek", Location(0, 0))
        
        hunter.add_honor(50)
        self.assertEqual(hunter.get_honor_score(), 50)
        
        hunter.lose_honor(20)
        self.assertEqual(hunter.get_honor_score(), 30)
        
        # Should never go negative
        hunter.lose_honor(100)
        self.assertEqual(hunter.get_honor_score(), 0)

    def test_collecting_trophies(self):
        hunter = Predator("Dek", Location(0, 0))
        
        hunter.add_trophy("Creature skull")
        self.assertEqual(hunter.get_trophy_count(), 1)
        self.assertEqual(hunter.get_honor_score(), 10)  # Bonus honor
        
        hunter.add_trophy("Monster skull")
        self.assertEqual(hunter.get_trophy_count(), 2)
        self.assertIn("Creature skull", hunter.get_trophies())

    def test_carrying_stuff(self):
        hunter = Predator("Dek", Location(0, 0))
        item = "synthetic"
        
        # Should be able to pick up
        success = hunter.pickup(item)
        self.assertTrue(success)
        self.assertTrue(hunter.is_carrying())
        self.assertEqual(hunter.get_carried_item(), item)
        
        # Can't carry two things
        success = hunter.pickup("another_item")
        self.assertFalse(success)
        
        # Should be able to drop
        dropped = hunter.put_down()
        self.assertEqual(dropped, item)
        self.assertFalse(hunter.is_carrying())

    def test_moving_around_grid(self):
        grid = Grid(20, 20)
        start = Location(5, 5)
        hunter = Predator("Dek", start)
        grid.place_agent(hunter, start)
        
        # Try moving to next spot
        next_spot = Location(6, 5)
        moved = hunter.move_to(next_spot, grid)
        
        self.assertTrue(moved)
        self.assertTrue(hunter.get_location().equals(next_spot))
        self.assertIsNone(grid.get_agent_at(start))
        self.assertEqual(grid.get_agent_at(next_spot), hunter)

    def test_map_symbols(self):
        dek = Predator("Dek", Location(0, 0))
        father = Predator("Father", Location(1, 1))
        brother = Predator("Brother", Location(2, 2))
        unknown = Predator("Stranger", Location(3, 3))
        
        self.assertEqual(dek.get_symbol(), "D")
        self.assertEqual(father.get_symbol(), "F")
        self.assertEqual(brother.get_symbol(), "B")
        self.assertEqual(unknown.get_symbol(), "P")  # Default


if __name__ == '__main__':
    unittest.main()
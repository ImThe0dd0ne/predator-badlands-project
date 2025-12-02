import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.synthetic import Synthetic
from agents.predator import Predator
from utils.location import Location
from environment.grid import Grid

class AndroidTests(unittest.TestCase):

    def test_android_creation(self):
        start = Location(5, 5)
        android = Synthetic("Thia", start, damaged=True)
        
        self.assertEqual(android.get_name(), "Thia")
        self.assertTrue(android.is_damaged())
        self.assertFalse(android.can_move())

    def test_fixing_android(self):
        android = Synthetic("Thia", Location(0, 0), health=40, damaged=True)
        # Now starts with 40/80 HP
    
        android.repair(30)  # Should go to 70/80
    
        self.assertEqual(android.get_health(), 70)
        self.assertFalse(android.is_damaged())
        self.assertTrue(android.can_move())
        
        android.repair(30)

    def test_knowledge_storage(self):
        android = Synthetic("Thia", Location(0, 0))
        
        android.learn_fact("boss_weakness", "vulnerable to plasma")
        android.learn_fact("map_data", "exit up north")
        
        self.assertEqual(android.recall_fact("boss_weakness"), "vulnerable to plasma")
        self.assertEqual(android.recall_fact("map_data"), "exit up north")
        self.assertIsNone(android.recall_fact("unknown"))

    def test_giving_advice(self):
        android = Synthetic("Thia", Location(0, 0))
        
        tip = android.give_advice("fighting the adversary")
        self.assertIsInstance(tip, str)
        self.assertGreater(len(tip), 0)

    def test_scanning_area(self):
        grid = Grid(20, 20)
        android = Synthetic("Thia", Location(10, 10))
        grid.place_agent(android, Location(10, 10))
        
        hunter = Predator("Dek", Location(12, 10))
        grid.place_agent(hunter, Location(12, 10))
        
        scans = android.scan_area(grid, distance=3)
        
        self.assertIsInstance(scans, list)
        self.assertGreater(len(scans), 0)

    def test_android_map_icon(self):
        android = Synthetic("Thia", Location(0, 0))
        self.assertEqual(android.get_symbol(), "S")


if __name__ == '__main__':
    unittest.main()
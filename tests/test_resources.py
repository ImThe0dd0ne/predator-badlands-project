import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mechanics.resources import ResourceManager, ResourceTracker
from agents.predator import Predator
from utils.location import Location

class ResourceTests(unittest.TestCase):

    def test_resource_manager_creation(self):
        rm = ResourceManager()
        self.assertIsNotNone(rm)

    def test_empty_terrain_cost(self):
        rm = ResourceManager()
        cost = rm.movement_cost("empty", carrying=False)
        self.assertEqual(cost, 5)

    def test_carrying_increases_cost(self):
        rm = ResourceManager()
        normal = rm.movement_cost("empty", carrying=False)
        with_load = rm.movement_cost("empty", carrying=True)
        self.assertGreater(with_load, normal)

    def test_terrain_passable(self):
        rm = ResourceManager()
        self.assertTrue(rm.can_walk_here("empty"))
        self.assertTrue(rm.can_walk_here("trap"))
        self.assertFalse(rm.can_walk_here("obstacle"))

    def test_hazard_effects(self):
        rm = ResourceManager()
        hunter = Predator("Dek", Location(0, 0))
        start_hp = hunter.get_health()
        
        rm.apply_hazard(hunter, "trap")
        
        self.assertLess(hunter.get_health(), start_hp)


class TrackerTests(unittest.TestCase):

    def test_tracker_creation(self):
        hunter = Predator("Dek", Location(0, 0))
        tracker = ResourceTracker(hunter)
        self.assertIsNotNone(tracker)

    def test_damage_tracking(self):
        hunter = Predator("Dek", Location(0, 0))
        tracker = ResourceTracker(hunter)
        
        tracker.record_damage(20)
        tracker.record_damage(15)
        
        self.assertEqual(tracker.total_damage(), 35)

    def test_stamina_tracking(self):
        hunter = Predator("Dek", Location(0, 0))
        tracker = ResourceTracker(hunter)
        
        tracker.record_stamina(10)
        tracker.record_stamina(5)
        
        self.assertEqual(tracker.total_stamina(), 15)

    def test_turn_counting(self):
        hunter = Predator("Dek", Location(0, 0))
        tracker = ResourceTracker(hunter)
        
        tracker.add_turn()
        tracker.add_turn()
        tracker.add_turn()
        
        self.assertEqual(tracker.turns_alive(), 3)

    def test_statistics(self):
        hunter = Predator("Dek", Location(0, 0))
        tracker = ResourceTracker(hunter)
        
        tracker.record_damage(20)
        tracker.add_turn()
        
        stats = tracker.get_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn("damage_taken", stats)
        self.assertIn("turns_survived", stats)


if __name__ == '__main__':
    unittest.main()
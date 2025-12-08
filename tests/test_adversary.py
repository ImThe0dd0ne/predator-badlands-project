import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.adversary import Adversary
from agents.predator import Predator
from utils.location import Location

class BossTests(unittest.TestCase):

    def test_boss_creation(self):
        start = Location(10, 10)
        boss = Adversary(start)
        
        self.assertEqual(boss.get_health(), 500)
        self.assertEqual(boss.get_max_health(), 500)
        self.assertEqual(boss.get_anger_level(), 5)
        self.assertTrue(boss.is_alive())

    def test_anger_goes_up(self):
        boss = Adversary(Location(0, 0))
        starting_anger = boss.get_anger_level()
        
        boss.get_more_angry(2)
        self.assertEqual(boss.get_anger_level(), starting_anger + 2)
        
        boss.get_more_angry(10)
        self.assertEqual(boss.get_anger_level(), 10)

    def test_boss_attacks(self):
        boss = Adversary(Location(0, 0))
        hunter = Predator("Dek", Location(1, 1))
        start_hp = hunter.get_health()
        
        damage_dealt = boss.attack_enemy(hunter)
        
        self.assertGreater(damage_dealt, 0)
        self.assertLess(hunter.get_health(), start_hp)

    def test_getting_hit_makes_angrier(self):
        boss = Adversary(Location(0, 0))
        start_anger = boss.get_anger_level()
        
        boss.take_damage(30) 
        
        self.assertGreater(boss.get_anger_level(), start_anger)

    def test_boss_symbol(self):
        boss = Adversary(Location(0, 0))
        self.assertEqual(boss.get_symbol(), "A")


if __name__ == '__main__':
    unittest.main()
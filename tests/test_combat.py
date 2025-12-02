import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mechanics.combat import Combat
from agents.predator import Predator
from agents.adversary import Adversary
from utils.location import Location

class FightTests(unittest.TestCase):

    def test_damage_calculation(self):
        # damage is a reasonable number
        attacker = Predator("Dek", Location(0, 0))
        defender = Adversary(Location(1, 1))
        
        damage = Combat.calculate_hit(attacker, defender)
        
        self.assertIsInstance(damage, int)
        self.assertGreater(damage, 0)

    def test_successful_attack(self):
        attacker = Predator("Dek", Location(0, 0))
        defender = Adversary(Location(1, 1))
        start_hp = defender.get_health()
        
        hit_success, damage = Combat.fight(attacker, defender)
        
        self.assertTrue(hit_success)
        self.assertGreater(damage, 0)
        self.assertLess(defender.get_health(), start_hp)

    def test_attack_without_stamina(self):
        attacker = Predator("Dek", Location(0, 0))
        defender = Adversary(Location(1, 1))
        
        # uses up all the stamina
        attacker.use_stamina(attacker.get_stamina())
        
        hit_success, damage = Combat.fight(attacker, defender)
        
        self.assertFalse(hit_success)
        self.assertEqual(damage, 0)

    def test_can_fight_check(self):
        attacker = Predator("Dek", Location(0, 0))
        defender = Adversary(Location(1, 1))
        
        self.assertTrue(Combat.can_fight(attacker, defender))
        
        # kill the defender
        defender.kill()
        self.assertFalse(Combat.can_fight(attacker, defender))


if __name__ == '__main__':
    unittest.main()
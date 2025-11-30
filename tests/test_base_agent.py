import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.base_agent import BaseAgent
from utils.location import Location

# Simple test character
class TestDude(BaseAgent):
    def act(self, grid):
        # Just stand for testing
        pass
    
    def get_symbol(self):
        return "X"


class TestBaseAgentStuff(unittest.TestCase):

    def test_basic_setup(self):
        start = Location(2, 2)
        dude = TestDude(start, health=100, stamina=80)
        
        self.assertTrue(dude.get_location().equals(start))
        self.assertEqual(dude.get_health(), 100)
        self.assertEqual(dude.get_stamina(), 80)
        self.assertTrue(dude.is_alive())

    def test_moving_around(self):
        dude = TestDude(Location(0, 0))
        new_spot = Location(5, 5)
        dude.set_location(new_spot)
        self.assertTrue(dude.get_location().equals(new_spot))

    def test_getting_hurt(self):
        dude = TestDude(Location(1, 1), health=100)
        dude.take_damage(25)
        self.assertEqual(dude.get_health(), 75)
        self.assertTrue(dude.is_alive())

    def test_dying_from_damage(self):
        dude = TestDude(Location(0, 0), health=40)
        dude.take_damage(50)
        self.assertEqual(dude.get_health(), 0)
        self.assertFalse(dude.is_alive())

    def test_healing_up(self):
        dude = TestDude(Location(3, 3), health=100)
        dude.take_damage(30)
        dude.heal(15)
        self.assertEqual(dude.get_health(), 85)

    def test_healing_limits(self):
        dude = TestDude(Location(0, 0), health=100)
        dude.take_damage(10)
        dude.heal(50)
        self.assertEqual(dude.get_health(), 100)

    def test_using_stamina(self):
        dude = TestDude(Location(0, 0), stamina=100)
        worked = dude.use_stamina(30)
        self.assertTrue(worked)
        self.assertEqual(dude.get_stamina(), 70)

    def test_not_enough_stamina(self):
        dude = TestDude(Location(0, 0), stamina=25)
        worked = dude.use_stamina(30)
        self.assertFalse(worked)
        self.assertEqual(dude.get_stamina(), 25)

    def test_resting_helps(self):
        dude = TestDude(Location(0, 0), stamina=100)
        dude.use_stamina(40)
        dude.rest(15)
        self.assertEqual(dude.get_stamina(), 75)

    def test_cant_rest_too_much(self):
        dude = TestDude(Location(0, 0), stamina=100)
        dude.use_stamina(10)
        dude.rest(50)
        self.assertEqual(dude.get_stamina(), 100)

    def test_manual_kill(self):
        dude = TestDude(Location(0, 0))
        dude.kill()
        self.assertFalse(dude.is_alive())
        self.assertEqual(dude.get_health(), 0)


if __name__ == '__main__':
    unittest.main()
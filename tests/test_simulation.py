import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulation import Simulation

class GameTests(unittest.TestCase):

    def test_game_creation(self):
        game = Simulation(20, 20)
        self.assertIsNotNone(game)
        self.assertEqual(game.current_turn(), 0)
        self.assertFalse(game.is_running())

    def test_game_setup(self):
        game = Simulation(20, 20)
        game.setup()
        
        self.assertTrue(game.is_running())
        self.assertIsNotNone(game.get_dek())
        self.assertIsNotNone(game.get_thia())
        self.assertIsNotNone(game.get_boss())

    def test_single_turn(self):
        game = Simulation(20, 20)
        game.setup()
        
        start_turn = game.current_turn()
        game.do_turn()
        
        self.assertEqual(game.current_turn(), start_turn + 1)

    def test_dek_starts_alive(self):
        game = Simulation(20, 20)
        game.setup()
        
        dek = game.get_dek()
        self.assertTrue(dek.is_alive())

    def test_game_over_on_dek_death(self):
        game = Simulation(20, 20)
        game.setup()
        
        dek = game.get_dek()
        dek.kill()
        
        game.do_turn()
        
        self.assertTrue(game.game_ended())
        self.assertFalse(game.did_win())

    def test_victory_on_boss_death(self):
        game = Simulation(20, 20)
        game.setup()
        
        boss = game.get_boss()
        boss.kill()
        
        game.do_turn()
        
        self.assertTrue(game.game_ended())
        self.assertTrue(game.did_win())

    def test_full_game_run(self):
        game = Simulation(20, 20)
        results = game.run_game(max_turns=20)
        
        self.assertIsInstance(results, dict)
        self.assertIn("turns", results)
        self.assertIn("won", results)

    def test_getting_stats(self):
        game = Simulation(20, 20)
        game.setup()
        game.do_turn()
        game.do_turn()
        
        stats = game.get_results()
        
        self.assertIsInstance(stats, dict)
        self.assertIn("dek_honor", stats)
        self.assertIn("turns_survived", stats)


if __name__ == '__main__':
    unittest.main()
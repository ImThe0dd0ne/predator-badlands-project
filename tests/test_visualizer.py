import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.visualizer import ConsoleVisualizer
from simulation import Simulation

class DisplayTests(unittest.TestCase):

    def test_visualizer_creation(self):
        viz = ConsoleVisualizer()
        self.assertIsNotNone(viz)

    def test_grid_drawing(self):
        game = Simulation(10, 10)
        game.setup()
        
        viz = ConsoleVisualizer()
        output = viz.draw_grid(game.get_grid(), show_numbers=False)
        
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 0)
        self.assertIn("|", output)

    def test_grid_with_coordinates(self):
        game = Simulation(10, 10)
        game.setup()
        
        viz = ConsoleVisualizer()
        output = viz.draw_grid(game.get_grid(), show_numbers=True)
        
        self.assertIn("0", output)

    def test_full_game_display(self):
        game = Simulation(10, 10)
        game.setup()
        
        viz = ConsoleVisualizer()
        output = viz.show_game_state(game)
        
        self.assertIsInstance(output, str)
        self.assertIn("Dek status", output)
        self.assertIn("Boss status", output)
        self.assertIn("Map key", output)

    def test_results_display(self):
        viz = ConsoleVisualizer()
        numbers = {
            "turns_survived": 50,
            "dek_honor": 120,
            "won": True
        }
        
        output = viz.show_results(numbers)
        
        self.assertIsInstance(output, str)
        self.assertIn("Final results", output)
        self.assertIn("50", output)


if __name__ == '__main__':
    unittest.main()
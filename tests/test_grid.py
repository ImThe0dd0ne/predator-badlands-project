import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from environment.grid import Grid
from environment.cell import CellType
from utils.location import Location


class TestGrid(unittest.TestCase):

    def test_init_default(self):
        grid = Grid()
        self.assertEqual(grid.get_width(), 20)
        self.assertEqual(grid.get_height(), 20)

    def test_init_custom_size(self):
        grid = Grid(30, 25)
        self.assertEqual(grid.get_width(), 30)
        self.assertEqual(grid.get_height(), 25)

    def test_normalize_location(self):
        grid = Grid(20, 20)
        
        loc = Location(21, 5)
        norm = grid.normalize_location(loc)
        self.assertEqual(norm.get_x(), 1)
        self.assertEqual(norm.get_y(), 5)
        
        loc = Location(5, 21)
        norm = grid.normalize_location(loc)
        self.assertEqual(norm.get_x(), 5)
        self.assertEqual(norm.get_y(), 1)

    def test_get_cell(self):
        grid = Grid()
        loc = Location(5, 5)
        cell = grid.get_cell(loc)
        self.assertIsNotNone(cell)
        self.assertEqual(cell.get_cell_type(), CellType.EMPTY)

    def test_set_cell_type(self):
        grid = Grid()
        loc = Location(5, 5)
        grid.set_cell_type(loc, CellType.OBSTACLE)
        cell = grid.get_cell(loc)
        self.assertEqual(cell.get_cell_type(), CellType.OBSTACLE)

    def test_place_and_remove_agent(self):
        grid = Grid()
        loc = Location(5, 5)
        agent = "test_agent"
        
        success = grid.place_agent(agent, loc)
        self.assertTrue(success)
        self.assertEqual(grid.get_agent_at(loc), agent)
        
        success = grid.place_agent("another_agent", loc)
        self.assertFalse(success)
        
        grid.remove_agent(loc)
        self.assertIsNone(grid.get_agent_at(loc))

    def test_get_adjacent_locations(self):
        grid = Grid(20, 20)
        loc = Location(5, 5)
        adjacent = grid.get_adjacent_locations(loc)
        
        self.assertEqual(len(adjacent), 4)
        expected_coords = [(5, 4), (5, 6), (4, 5), (6, 5)]
        actual_coords = [(l.get_x(), l.get_y()) for l in adjacent]
        for coord in expected_coords:
            self.assertIn(coord, actual_coords)


if __name__ == '__main__':
    unittest.main()
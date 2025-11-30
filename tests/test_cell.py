import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from environment.cell import Cell, CellType


class TestCell(unittest.TestCase):
    """the unit tests for cell"""

    def test_init_default(self):
        cell = Cell()
        self.assertEqual(cell.get_cell_type(), CellType.EMPTY)
        self.assertIsNone(cell.get_occupant())

    def test_init_with_type(self):
        cell = Cell(CellType.OBSTACLE)
        self.assertEqual(cell.get_cell_type(), CellType.OBSTACLE)

    def test_set_cell_type(self):
        cell = Cell()
        cell.set_cell_type(CellType.TRAP)
        self.assertEqual(cell.get_cell_type(), CellType.TRAP)

    def test_occupant(self):
        cell = Cell()
        occupant = "test_agent"
        cell.set_occupant(occupant)
        self.assertEqual(cell.get_occupant(), occupant)

    def test_is_empty(self):
        cell = Cell()
        self.assertTrue(cell.is_empty())
        cell.set_occupant("agent")
        self.assertFalse(cell.is_empty())

    def test_is_walkable(self):
        cell = Cell(CellType.EMPTY)
        self.assertTrue(cell.is_walkable())
        
        cell.set_cell_type(CellType.OBSTACLE)
        self.assertFalse(cell.is_walkable())


if __name__ == '__main__':
    unittest.main()
from typing import Optional, List, Tuple
from environment.cell import Cell, CellType
from utils.location import Location


class Grid:
    
    def __init__(self, width: int = 20, height: int = 20):
        self.__width: int = width
        self.__height: int = height
        self.__cells: List[List[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)
        ]

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def normalize_location(self, location: Location) -> Location:
        normalized_x = location.get_x() % self.__width
        normalized_y = location.get_y() % self.__height
        return Location(normalized_x, normalized_y)

    def is_valid_location(self, location: Location) -> bool:
        return True 

    def get_cell(self, location: Location) -> Cell:
        norm_loc = self.normalize_location(location)
        return self.__cells[norm_loc.get_y()][norm_loc.get_x()]

    def set_cell_type(self, location: Location, cell_type: CellType) -> None:
        cell = self.get_cell(location)
        cell.set_cell_type(cell_type)

    def place_agent(self, agent: object, location: Location) -> bool:
        cell = self.get_cell(location)
        if cell.get_occupant() is not None:
            return False
        cell.set_occupant(agent)
        return True

    def remove_agent(self, location: Location) -> None:
        cell = self.get_cell(location)
        cell.set_occupant(None)

    def get_agent_at(self, location: Location) -> Optional[object]:
        cell = self.get_cell(location)
        return cell.get_occupant()

    def get_adjacent_locations(self, location: Location) -> List[Location]:
        x, y = location.get_x(), location.get_y()
        adjacent = [
            Location(x, y - 1),      # Up
            Location(x, y + 1),      # Down
            Location(x - 1, y),      # Left
            Location(x + 1, y)       # Right
        ]
        return [self.normalize_location(loc) for loc in adjacent]

    def is_walkable(self, location: Location) -> bool:
        cell = self.get_cell(location)
        return cell.is_walkable()

    def __str__(self) -> str:
        return f"Grid({self.__width}x{self.__height})"
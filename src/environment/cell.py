from enum import Enum
from typing import Optional


class CellType(Enum):
    EMPTY = "empty"
    OBSTACLE = "obstacle"
    TRAP = "trap"
    CREATURE = "creature"
    PREDATOR = "predator"
    SYNTHETIC = "synthetic"
    ADVERSARY = "adversary"


class Cell:

    def __init__(self, cell_type: CellType = CellType.EMPTY):
        self.__cell_type: CellType = cell_type
        self.__occupant: Optional[object] = None

    def get_cell_type(self) -> CellType:
        return self.__cell_type

    def set_cell_type(self, cell_type: CellType) -> None:
        self.__cell_type = cell_type

    def get_occupant(self) -> Optional[object]:
        return self.__occupant

    def set_occupant(self, occupant: Optional[object]) -> None:
        self.__occupant = occupant

    def is_empty(self) -> bool:
        return self.__cell_type == CellType.EMPTY and self.__occupant is None

    def is_walkable(self) -> bool:
        return self.__cell_type in [CellType.EMPTY, CellType.TRAP] and self.__occupant is None

    def __str__(self) -> str:
        if self.__occupant is not None:
            return f"Cell({self.__cell_type.value}, occupied)"
        return f"Cell({self.__cell_type.value})"
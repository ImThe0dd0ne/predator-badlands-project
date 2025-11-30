from abc import ABC, abstractmethod
from utils.location import Location
from typing import Optional

class BaseAgent(ABC):
    # Base character stats
    def __init__(self, location: Location, health: int = 100, stamina: int = 100):
        self.__location = location
        self.__health = health
        self.__max_health = health
        self.__stamina = stamina  
        self.__max_stamina = stamina
        self.__alive = True

    # Where the character is
    def get_location(self) -> Location:
        return self.__location

    def set_location(self, location: Location) -> None:
        self.__location = location

    # Health management
    def get_health(self) -> int:
        return self.__health

    def get_max_health(self) -> int:
        return self.__max_health

    def set_health(self, health: int) -> None:
        # health wont go out of bounds set
        self.__health = max(0, min(health, self.__max_health))
        if self.__health <= 0:
            self.__alive = False

    def take_damage(self, damage: int) -> None:
        self.set_health(self.__health - damage)

    def heal(self, amount: int) -> None:
        self.set_health(self.__health + amount)

    # stamina/energy system
    def get_stamina(self) -> int:
        return self.__stamina

    def get_max_stamina(self) -> int:
        return self.__max_stamina

    def set_stamina(self, stamina: int) -> None:
        self.__stamina = max(0, min(stamina, self.__max_stamina))

    def use_stamina(self, amount: int) -> bool:
        # Check if theres enough stamina first
        if self.__stamina >= amount:
            self.set_stamina(self.__stamina - amount)
            return True
        return False

    def rest(self, amount: int = 20) -> None:
        # Recover some stamina
        self.set_stamina(self.__stamina + amount)

    # check of life
    def is_alive(self) -> bool:
        return self.__alive

    def kill(self) -> None:
        self.__alive = False
        self.__health = 0

    @abstractmethod
    def act(self, grid) -> None:
        # What the character does each turn
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        #Character icon for display
        pass

    def __str__(self) -> str:
        status = "alive" if self.__alive else "dead"
        return f"{self.__class__.__name__}(HP:{self.__health}/{self.__max_health}, Stamina:{self.__stamina}/{self.__max_stamina}, {status})"
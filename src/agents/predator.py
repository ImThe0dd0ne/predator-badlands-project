from agents.base_agent import BaseAgent
from utils.location import Location
import random

class Predator(BaseAgent):
    # Yautja hunter with its honor system
    def __init__(self, name: str, location: Location, health: int = 150, stamina: int = 120):
        super().__init__(location, health, stamina)
        self.__name = name
        self.__honor = 0
        self.__trophies = []
        self.__carrying = None

    def get_name(self):
        return self.__name

    def get_honor_score(self):
        return self.__honor

    def add_honor(self, amount: int):
        self.__honor += amount

    def lose_honor(self, amount: int):
        self.__honor = max(0, self.__honor - amount)

    def add_trophy(self, trophy_desc: str):
        self.__trophies.append(trophy_desc)
        self.add_honor(10)

    def get_trophies(self):
        return self.__trophies[:]

    def get_trophy_count(self):
        return len(self.__trophies)

    def is_carrying(self):
        return self.__carrying is not None

    def pickup(self, item):
        if self.__carrying is None:
            self.__carrying = item
            return True
        return False

    def put_down(self):
        carried = self.__carrying
        self.__carrying = None
        return carried

    def get_carried_item(self):
        return self.__carrying

    def move_to(self, new_spot: Location, game_grid) -> bool:
        # Moving while carrying costs more stamina
        stamina_needed = 10 if self.is_carrying() else 5
        
        if not self.use_stamina(stamina_needed):
            return False

        if not game_grid.is_walkable(new_spot):
            return False

        game_grid.remove_agent(self.get_location())
        self.set_location(new_spot)
        game_grid.place_agent(self, new_spot)
        return True

    def hunt(self, target) -> bool:
        if not self.use_stamina(20):
            return False

        damage = random.randint(20, 40)
        target.take_damage(damage)

        if not target.is_alive():
            skull = f"{target.__class__.__name__} skull"
            self.add_trophy(skull)
            return True

        return False

    def act(self, game_grid):
        if not self.is_alive():
            return

        # Takes a break if tired
        if self.get_stamina() < 20:
            self.rest(30)
            return

        # Looks around for moves
        nearby = game_grid.get_adjacent_locations(self.get_location())
        possible_moves = [spot for spot in nearby if game_grid.is_walkable(spot)]

        # Gos somewhere random
        if possible_moves:
            chosen = random.choice(possible_moves)
            self.move_to(chosen, game_grid)

    def get_symbol(self) -> str:
        if self.__name == "Dek":
            return "D"
        elif self.__name == "Father":
            return "F"
        elif self.__name == "Brother":
            return "B"
        return "P"

    def __str__(self) -> str:
        status = "alive" if self.is_alive() else "dead"
        return f"{self.__name}(HP:{self.get_health()}/{self.get_max_health()}, Stamina:{self.get_stamina()}/{self.get_max_stamina()}, Honor:{self.__honor}, Trophies:{len(self.__trophies)})"
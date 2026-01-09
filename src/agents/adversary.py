from agents.base_agent import BaseAgent
from utils.location import Location
import random

class Adversary(BaseAgent):
    def __init__(self, location: Location, health: int = 500, stamina: int = 200):
        super().__init__(location, health, stamina)
        self.__anger = 5 
        self.__base_damage = 30  # Starting damage

    def get_anger_level(self):
        return self.__anger

    def get_more_angry(self, boost: int = 1):
        # Can't get more than max anger
        self.__anger = min(10, self.__anger + boost)

    def get_base_damage(self):
        return self.__base_damage

    def attack_enemy(self, target: BaseAgent) -> int:
        # Attacks cost stamina
        if not self.use_stamina(15):
            return 0  

        damage = self.__base_damage + (self.__anger * 2)
        # Some random variation in hits
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))
        
        target.take_damage(damage)
        return damage

    def take_damage(self, damage: int) -> None:
        super().take_damage(damage)
        # gets angrier when its hit harder
        if damage > 20:
            self.get_more_angry(1)

    def move_toward_target(self, target_spot: Location, grid) -> bool:
        # In pursuit however it costs stamina to do so
        if not self.use_stamina(8):
            return False

        current_pos = self.get_location()
        
        # fgigure out which way to go
        x_diff = target_spot.get_x() - current_pos.get_x()
        y_diff = target_spot.get_y() - current_pos.get_y()

        move_x = 0 if x_diff == 0 else (1 if x_diff > 0 else -1)
        move_y = 0 if y_diff == 0 else (1 if y_diff > 0 else -1)

        # gos toward the bigger distance
        if abs(x_diff) > abs(y_diff):
            new_spot = Location(current_pos.get_x() + move_x, current_pos.get_y())
        else:
            new_spot = Location(current_pos.get_x(), current_pos.get_y() + move_y)

        new_spot = grid.normalize_location(new_spot)

        # moves if possible
        if grid.is_walkable(new_spot):
            grid.remove_agent(current_pos)
            self.set_location(new_spot)
            grid.place_agent(self, new_spot)
            return True

        return False

    def act(self, grid):
        # What the boss does each turn
        if not self.is_alive():
            return

        # Rests if stamina meter is low
        if self.get_stamina() < 30:
            self.rest(40)
            return

        nearby_spots = grid.get_adjacent_locations(self.get_location())
        open_spots = [spot for spot in nearby_spots if grid.is_walkable(spot)]

        if open_spots:
            chosen_spot = random.choice(open_spots)
            if grid.is_walkable(chosen_spot):
                grid.remove_agent(self.get_location())
                self.set_location(chosen_spot)
                grid.place_agent(self, chosen_spot)

    def get_symbol(self) -> str:
        # The map icon for the boss
        return "A"

    def __str__(self) -> str:
        status = "alive" if self.is_alive() else "dead"
        return f"Boss(HP:{self.get_health()}/{self.get_max_health()}, Anger:{self.__anger}, Stamina:{self.get_stamina()}/{self.get_max_stamina()})"
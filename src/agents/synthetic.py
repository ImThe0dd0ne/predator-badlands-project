from agents.base_agent import BaseAgent
from utils.location import Location

class Synthetic(BaseAgent):
    # Thia is damaged but intelligent
    def __init__(self, name: str, location: Location, health: int = 80, damaged: bool = True):
        # call super with the max health at 80, then reduces if needed
        super().__init__(location, 80, stamina=50)  # Max HP is 80
        self.__name = name
        self.__damaged = damaged
        self.__knowledge = {}
        self.__cant_move = damaged
        
        # If starting with less than max health, reduce it
        if health < 80:
            self.take_damage(80 - health)

    def get_name(self):
        return self.__name

    def is_damaged(self):
        return self.__damaged

    def can_move(self):
        return not self.__cant_move

    def repair(self, amount: int):
        self.heal(amount)
        # able move if its health is good enough
        if self.get_health() > 60:
            self.__cant_move = False
            self.__damaged = False

    def learn_fact(self, topic: str, info: str):
        self.__knowledge[topic] = info

    def recall_fact(self, topic: str):
        return self.__knowledge.get(topic)

    def give_advice(self, situation: str) -> str:
        if "adversary" in situation.lower():
            return "wait you need to really be careful here"
        elif "stamina" in situation.lower():
            return "You could rest first"
        elif "hunt" in situation.lower():
            return "You must remember your code you follow only fight those which are worth being hunted"
        else:
            return "you need to be watch out and be smart here"

    def scan_area(self, grid, distance: int = 3):
        findings = []
        current_spot = self.get_location()

        for dx in range(-distance, distance + 1):
            for dy in range(-distance, distance + 1):
                check_spot = Location(
                    current_spot.get_x() + dx,
                    current_spot.get_y() + dy
                )
                check_spot = grid.normalize_location(check_spot)

                thing = grid.get_agent_at(check_spot)
                if thing and thing != self:
                    findings.append(
                        f"Found {thing.__class__.__name__} at ({check_spot.get_x()}, {check_spot.get_y()})"
                    )

        return findings

    def act(self, grid):
        # cant act alone when its too damaged
        if not self.is_alive() or self.__cant_move:
            return

    def get_symbol(self) -> str:
        return "S"

    def __str__(self):
        status = "broken" if self.__damaged else "working"
        mobility = "stuck" if self.__cant_move else "mobile"
        return f"{self.__name} (Android) - HP:{self.get_health()}/{self.get_max_health()}, {status}, {mobility}"
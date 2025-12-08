class ResourceManager:
    #tracks the resource costs and terrain difficulty with stamina, traps, obstacles

    def __init__(self):
        self.__terrain_costs = {
            "empty": 5,
            "trap": 10,
            "obstacle": 999 
        }
        self.__carrying_penalty = 5

    def movement_cost(self, terrain: str, carrying: bool = False):
        # how much stamina is needed to move through here
        base_cost = self.__terrain_costs.get(terrain, 5)
        
        if carrying:
            base_cost += self.__carrying_penalty
        
        return base_cost

    def can_walk_here(self, terrain: str):
        # is the terrain passable
        cost = self.__terrain_costs.get(terrain, 5)
        return cost < 999

    def apply_hazard(self, agent, hazard_type: str):
        # environment dangers affects the agents
        if hazard_type == "trap":
            agent.take_damage(15)
            agent.use_stamina(10)
        elif hazard_type == "storm":
            agent.use_stamina(20)
        elif hazard_type == "heat":
            agent.use_stamina(5)


class ResourceTracker:
    # keeps the stats on agent resource usage

    def __init__(self, agent):
        self.__agent = agent
        self.__damage_taken = 0
        self.__stamina_used = 0
        self.__turns_survived = 0

    def record_damage(self, amount: int):
        self.__damage_taken += amount

    def record_stamina(self, amount: int):
        self.__stamina_used += amount

    def add_turn(self):
        self.__turns_survived += 1

    def total_damage(self):
        return self.__damage_taken

    def total_stamina(self):
        return self.__stamina_used

    def turns_alive(self):
        return self.__turns_survived

    def get_stats(self):
        # all of the tracked numbers
        return {
            "damage_taken": self.__damage_taken,
            "stamina_used": self.__stamina_used,
            "turns_survived": self.__turns_survived,
            "current_health": self.__agent.get_health(),
            "current_stamina": self.__agent.get_stamina()
        }
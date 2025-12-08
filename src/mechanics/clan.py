class ClanRank:
    # these are the levels in the predator society
    UNBLOODED = 0
    BLOODED = 1
    HONORED = 2
    ELITE = 3
    ELDER = 4


class Clan:
    # manages the predators society and honor rules

    def __init__(self, name: str):
        self.__name = name
        self.__members = []
        self.__honor_levels = {
            ClanRank.UNBLOODED: 0,
            ClanRank.BLOODED: 50,
            ClanRank.HONORED: 150,
            ClanRank.ELITE: 300,
            ClanRank.ELDER: 500
        }

    def get_clan_name(self):
        return self.__name

    def add_hunter(self, predator):
        if predator not in self.__members:
            self.__members.append(predator)

    def remove_hunter(self, predator):
        if predator in self.__members:
            self.__members.remove(predator)

    def get_hunters(self):
        return self.__members[:]

    def get_rank(self, honor_score: int):
        # what rank does this honor score give
        for rank in [ClanRank.ELDER, ClanRank.ELITE, ClanRank.HONORED, ClanRank.BLOODED, ClanRank.UNBLOODED]:
            if honor_score >= self.__honor_levels[rank]:
                return rank
        return ClanRank.UNBLOODED

    def judge_action(self, action_type: str, details: dict):
        # how much honor that is needed for the action to take place
        honor_change = 0

        if action_type == "hunt_worthy":
            honor_change = 20
        elif action_type == "beat_boss":
            honor_change = 100
        elif action_type == "get_trophy":
            honor_change = 10
        elif action_type == "hunt_weak":
            honor_change = -30
        elif action_type == "run_away":
            honor_change = -10
        elif action_type == "help_clanmate":
            honor_change = 15
        elif action_type == "break_code":
            honor_change = -50

        return honor_change

    def challenge(self, challenger, challenged):
        # hunters challenges another
        if challenger in self.__members and challenged in self.__members:
            return challenger.is_alive() and challenged.is_alive()
        return False

    def exile_hunter(self, predator):
        # kicked out of the clan
        self.remove_hunter(predator)
        predator.lose_honor(100)


class HonorLogger:
    # Keeps track of honor events

    def __init__(self, predator):
        self.__predator = predator
        self.__history = []

    def log_event(self, event_type: str, honor_change: int, description: str):
        event = {
            "type": event_type,
            "honor_change": honor_change,
            "description": description,
            "total_honor": self.__predator.get_honor_score()
        }
        self.__history.append(event)

    def get_history(self):
        return self.__history[:]

    def get_big_events(self):
        # Only significant honor changes
        return [e for e in self.__history if abs(e["honor_change"]) >= 20]
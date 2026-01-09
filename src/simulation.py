from environment.grid import Grid
from environment.cell import CellType
from agents.predator import Predator
from agents.synthetic import Synthetic
from agents.adversary import Adversary
from mechanics.combat import Combat
from mechanics.resources import ResourceManager, ResourceTracker
from mechanics.clan import Clan, HonorLogger
from utils.location import Location
import random

class Simulation:
    #Main game engine - runs everything

    def __init__(self, grid_width: int = 20, grid_height: int = 20):
        self.__grid = Grid(grid_width, grid_height)
        self.__turn = 0
        self.__running = False
        self.__game_over = False
        self.__won = False
        
        #Game characters
        self.__dek = None
        self.__thia = None
        self.__boss = None
        self.__father = None
        self.__brother = None
        
        #Game systems
        self.__resources = ResourceManager()
        self.__clan = Clan("Dark Blade Clan")
        
        #Tracking
        self.__dek_tracker = None
        self.__dek_honor_log = None
        
        #Stats
        self.__stats = {
            "turns": 0,
            "fights": 0,
            "hunts": 0,
            "honor_gained": 0,
            "honor_lost": 0
        }

    def setup(self):
        #Puts everything in starting positions
        #Dek starts
        dek_start = Location(2, 2)
        self.__dek = Predator("Dek", dek_start, health=150, stamina=120)
        self.__grid.place_agent(self.__dek, dek_start)
        self.__clan.add_hunter(self.__dek)
        
        #Tracks Dek
        self.__dek_tracker = ResourceTracker(self.__dek)
        self.__dek_honor_log = HonorLogger(self.__dek)
        
        #Thia (damaged android)
        thia_start = Location(3, 3)
        self.__thia = Synthetic("Thia", thia_start, health=60, damaged=True)
        self.__grid.place_agent(self.__thia, thia_start)
        
        #Thia knows info
        self.__thia.learn_fact("boss_location", "Far north area")
        self.__thia.learn_fact("boss_weakness", "Gets reckless when angry")
        
        #Boss enemy
        boss_start = Location(18, 18)
        self.__boss = Adversary(boss_start, health=500, stamina=200)
        self.__grid.place_agent(self.__boss, boss_start)
        
        #Father
        father_start = Location(10, 10)
        self.__father = Predator("Father", father_start, health=180, stamina=140)
        self.__father.add_honor(200)
        self.__grid.place_agent(self.__father, father_start)
        self.__clan.add_hunter(self.__father)
        
        #Brother
        brother_start = Location(8, 8)
        self.__brother = Predator("Brother", brother_start, health=160, stamina=130)
        self.__brother.add_honor(100)
        self.__grid.place_agent(self.__brother, brother_start)
        self.__clan.add_hunter(self.__brother)
        
        #Adds obstacles and traps
        self.__add_obstacles()
        self.__add_traps()
        
        self.__running = True

    def __add_obstacles(self):
        #Places some rocks and barriers
        for _ in range(15):
            x = random.randint(0, self.__grid.get_width() - 1)
            y = random.randint(0, self.__grid.get_height() - 1)
            spot = Location(x, y)
            
            if self.__grid.get_agent_at(spot) is None:
                self.__grid.set_cell_type(spot, CellType.OBSTACLE)

    def __add_traps(self):
        #Places some dangerous areas
        for _ in range(10):
            x = random.randint(0, self.__grid.get_width() - 1)
            y = random.randint(0, self.__grid.get_height() - 1)
            spot = Location(x, y)
            
            cell = self.__grid.get_cell(spot)
            if (self.__grid.get_agent_at(spot) is None and 
                cell.get_cell_type() == CellType.EMPTY):
                self.__grid.set_cell_type(spot, CellType.TRAP)

    def do_turn(self):
        #Run one game turn
        if not self.__running or self.__game_over:
            return

        self.__turn += 1
        self.__stats["turns"] = self.__turn
        
        #Track Dek's turn
        if self.__dek and self.__dek.is_alive():
            self.__dek_tracker.add_turn()
        
        #Everyone takes their turn
        self.__dek_turn()
        self.__thia_turn()
        self.__father_turn()
        self.__brother_turn()
        self.__boss_turn()
        
        self.__check_end()

    def __dek_turn(self):
        #Deks turn
        if not self.__dek or not self.__dek.is_alive():
            return
        
        self.__dek.act(self.__grid)
        
        dek_spot = self.__dek.get_location()
        cell = self.__grid.get_cell(dek_spot)
        if cell.get_cell_type() == CellType.TRAP:
            self.__resources.apply_hazard(self.__dek, "trap")
            self.__dek_tracker.record_damage(15)

    def __thia_turn(self):
        #Thias turn
        if not self.__thia or not self.__thia.is_alive():
            return
        if self.__dek and self.__dek.is_alive():
            dek_spot = self.__dek.get_location()
            thia_spot = self.__thia.get_location()
            
            distance = abs(dek_spot.get_x() - thia_spot.get_x()) + abs(dek_spot.get_y() - thia_spot.get_y())
            
            if distance <= 2:
                scans = self.__thia.scan_area(self.__grid, distance=4)

    def __father_turn(self):
        if not self.__father or not self.__father.is_alive():
            return
        self.__father.act(self.__grid)

    def __brother_turn(self):
        if not self.__brother or not self.__brother.is_alive():
            return
        self.__brother.act(self.__grid)

    def __boss_turn(self):
        if not self.__boss or not self.__boss.is_alive():
            return
        
        #The boss hunts and finds Dek if he is close
        if self.__dek and self.__dek.is_alive():
            dek_spot = self.__dek.get_location()
            boss_spot = self.__boss.get_location()
            
            distance = abs(dek_spot.get_x() - boss_spot.get_x()) + abs(dek_spot.get_y() - boss_spot.get_y())
            
            if distance <= 5:
                #Then Chases after Dek
                self.__boss.move_toward_target(dek_spot, self.__grid)
                
                #And attacks if hes right next to Dek
                if distance <= 1:
                    damage = self.__boss.attack_enemy(self.__dek)
                    if damage > 0:
                        self.__dek_tracker.record_damage(damage)
                        self.__stats["fights"] += 1
            else:
                #Wanders around
                self.__boss.act(self.__grid)

    def __check_end(self):
        #Checks if the game ended
        #Loses if Dek ends up dead
        if self.__dek and not self.__dek.is_alive():
            self.__game_over = True
            self.__won = False
            self.__running = False
            return
        
        #Wins if the boss dies
        if self.__boss and not self.__boss.is_alive():
            self.__game_over = True
            self.__won = True
            self.__running = False
            
            #Honor is gained after beating the boss
            honor_gain = self.__clan.judge_action("beat_boss", {})
            self.__dek.add_honor(honor_gain)
            self.__dek_honor_log.log_event(
                "beat_boss", 
                honor_gain, 
                "Defeated the ultimate adversary"
            )
            self.__stats["honor_gained"] += honor_gain

    def run_game(self, max_turns: int = 100):
        #This runs the whole game
        self.setup()
        
        while self.__running and self.__turn < max_turns:
            self.do_turn()
        
        return self.get_results()

    def get_results(self):
        #The Game stats overview
        results = self.__stats.copy()
        
        if self.__dek:
            results["dek_hp"] = self.__dek.get_health()
            results["dek_stamina"] = self.__dek.get_stamina()
            results["dek_honor"] = self.__dek.get_honor_score()
            results["dek_trophies"] = self.__dek.get_trophy_count()
        
        if self.__dek_tracker:
            results["dek_damage"] = self.__dek_tracker.total_damage()
            results["dek_stamina_used"] = self.__dek_tracker.total_stamina()
        
        results["won"] = self.__won
        results["turns_survived"] = self.__turn
        
        return results

    def get_grid(self):
        return self.__grid

    def get_dek(self):
        return self.__dek

    def get_thia(self):
        return self.__thia

    def get_boss(self):
        return self.__boss

    def current_turn(self):
        return self.__turn

    def is_running(self):
        return self.__running

    def game_ended(self):
        return self.__game_over

    def did_win(self):
        return self.__won

    def get_clan(self):
        return self.__clan
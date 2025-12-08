from environment.grid import Grid
from environment.cell import CellType

class ConsoleVisualizer:
    #visual game state shown in the terminal

    def __init__(self):
        self.__symbols = {
            "empty": ".",
            "obstacle": "#",
            "trap": "^"
        }

    def draw_grid(self, grid: Grid, show_numbers: bool = False):
        #draws the grid
        width = grid.get_width()
        height = grid.get_height()
        
        picture = []
        
        #Top 
        if show_numbers:
            header = "   " + "".join(f"{i % 10}" for i in range(width))
            picture.append(header)
        
        picture.append("  +" + "-" * width + "+")
        
        #Each of the rows
        for y in range(height):
            row_chars = []
            for x in range(height):
                from utils.location import Location
                spot = Location(x, y)
                char = self.__get_char(grid, spot)
                row_chars.append(char)
            
            if show_numbers:
                row_str = f"{y:2}|" + "".join(row_chars) + "|"
            else:
                row_str = "  |" + "".join(row_chars) + "|"
            
            picture.append(row_str)
        
        #Bottom
        picture.append("  +" + "-" * width + "+")
        
        return "\n".join(picture)

    def __get_char(self, grid: Grid, location):
        #This determines what character for which location
        character = grid.get_agent_at(location)
        if character is not None:
            return character.get_symbol()
        
        #Checks the cell type for terrains
        cell = grid.get_cell(location)
        cell_type = cell.get_cell_type()
        
        if cell_type == CellType.OBSTACLE:
            return "#"
        elif cell_type == CellType.TRAP:
            return "^"
        else:
            return "."

    def show_game_state(self, game):
        display = []
        
        display.append("=" * 50)
        display.append(f"PREDATOR: BADLANDS - Turn {game.current_turn()}")
        display.append("=" * 50)
        display.append("")
        
        #The games world
        display.append(self.draw_grid(game.get_grid(), show_numbers=True))
        display.append("")
        
        #What is what
        display.append("Map Key:")
        display.append("  D = Dek (You)")
        display.append("  S = Thia (Android)")
        display.append("  A = Adversary (Boss)")
        display.append("  F = Father")
        display.append("  B = Brother")
        display.append("  # = Rock/Obstacle")
        display.append("  ^ = Trap")
        display.append("  . = Empty ground")
        display.append("")
        
        #Deks status
        dek = game.get_dek()
        if dek and dek.is_alive():
            display.append("DEK STATUS:")
            display.append(f"  Health: {dek.get_health()}/{dek.get_max_health()}")
            display.append(f"  Stamina: {dek.get_stamina()}/{dek.get_max_stamina()}")
            display.append(f"  Honor: {dek.get_honor_score()}")
            display.append(f"  Trophies: {dek.get_trophy_count()}")
            display.append(f"  Position: ({dek.get_location().get_x()}, {dek.get_location().get_y()})")
        else:
            display.append("DEK: DEAD")
        
        display.append("")
        
        #The vboss status
        boss = game.get_boss()
        if boss and boss.is_alive():
            display.append("BOSS STATUS:")
            display.append(f"  Health: {boss.get_health()}/{boss.get_max_health()}")
            display.append(f"  Anger: {boss.get_anger_level()}/10")
            display.append(f"  Position: ({boss.get_location().get_x()}, {boss.get_location().get_y()})")
        else:
            display.append("BOSS: DEFEATED!")
        
        display.append("")
        
        #The game status
        if game.game_ended():
            display.append("=" * 50)
            if game.did_win():
                display.append("VICTORY! Dek proved his worth!")
            else:
                display.append("DEFEAT! Dek has fallen...")
            display.append("=" * 50)
        
        return "\n".join(display)

    def show_results(self, stats: dict):
        #The final results displayed
        display = []
        
        display.append("=" * 50)
        display.append("FINAL RESULTS")
        display.append("=" * 50)
        display.append("")
        
        display.append(f"Turns Survived: {stats.get('turns_survived', 0)}")
        display.append(f"Battles Fought: {stats.get('fights', 0)}")
        display.append(f"Honor Earned: {stats.get('honor_gained', 0)}")
        display.append("")
        
        display.append(f"Final Health: {stats.get('dek_hp', 0)}")
        display.append(f"Final Stamina: {stats.get('dek_stamina', 0)}")
        display.append(f"Final Honor: {stats.get('dek_honor', 0)}")
        display.append(f"Trophies Collected: {stats.get('dek_trophies', 0)}")
        display.append("")
        
        display.append(f"Total Damage Taken: {stats.get('dek_damage', 0)}")
        display.append(f"Total Stamina Used: {stats.get('dek_stamina_used', 0)}")
        display.append("")
        
        if stats.get('won', False):
            display.append("OUTCOME: VICTORY")
        else:
            display.append("OUTCOME: DEFEAT")
        
        display.append("=" * 50)
        
        return "\n".join(display)
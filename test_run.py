import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from simulation import Simulation
from utils.visualizer import ConsoleVisualizer

print('Full sim test')
print('=' * 50)

game = Simulation(10, 10)
viz = ConsoleVisualizer()
game.setup()

print('Initial state:')
print(viz.show_game_state(game))

for turn in range(1, 11):
    input(f'Press enter for turn {turn}...')
    game.do_turn()
    print(f'After turn {turn}:')
    print(viz.show_game_state(game))
    
    if game.game_ended():
        print('Game over!')
        break

print('\\n' + '=' * 50)
print('The final results:')
print('=' * 50)
results = game.get_results()
print(viz.show_results(results))

print('Simulation done and everything is working!')

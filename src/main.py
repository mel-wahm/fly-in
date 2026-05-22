from parser import MapParser
from models import Connection, Zone
from graph import Graph
from visualizer import Renderer
import os
import arcade

maps = [
    'maps/easy/01_linear_path.txt', #0 
    'maps/easy/02_simple_fork.txt', #1
    'maps/easy/03_basic_capacity.txt', #2 
    'maps/medium/01_dead_end_trap.txt', #3
    'maps/medium/02_circular_loop.txt', #4
    'maps/medium/03_priority_puzzle.txt', #5
    'maps/hard/01_maze_nightmare.txt', #6 
    'maps/hard/02_capacity_hell.txt', #7
    'maps/hard/03_ultimate_challenge.txt', #8
    'maps/challenger/01_the_impossible_dream.txt' #9
    ]
parser = MapParser(maps[1])
parser.parse_map()

# graph = Graph(parser.zones, parser.connections)
# graph.adjacency_list()
# for gr, d in graph.graph.items():
#     print(gr, "---->", d)

red_color = '\033[91m'
green_color = '\033[92m'
end_color = '\033[0m'
bald_access = '\033[1m'
try:
    r = Renderer(parser, parser.connections)
    arcade.run()
except KeyboardInterrupt:
    os.system("clear")
    print(f"{bald_access}{green_color}--------------------------------------{end_color}")
    print(f"{bald_access}{red_color} The program was stopped by the user{end_color}")
    print(f"{bald_access}{green_color}--------------------------------------{end_color}")
    print()
except Exception as e:
    print(f"{bald_access}{red_color}Error:", e)
from parser import MapParser ; from visualizer import Renderer ;import warnings
from pathfinder import Pathfinder ; from graph import Graph ; from simulation import Drone, Simulator
from pydantic import ValidationError; import arcade
warnings.filterwarnings("ignore")
maps = [
    'maps/easy/00_nigga.txt', 'maps/easy/01_linear_path.txt',  'maps/easy/02_simple_fork.txt', 'maps/easy/03_basic_capacity.txt',  
    'maps/medium/01_dead_end_trap.txt', 'maps/medium/02_circular_loop.txt', 'maps/medium/03_priority_puzzle.txt', 
    'maps/hard/01_maze_nightmare.txt',  'maps/hard/02_capacity_hell.txt', 'maps/hard/03_ultimate_challenge.txt', 
    'maps/challenger/01_the_impossible_dream.txt' #9
    ]
red_color = '\033[91m' ; green_color = '\033[92m' ; end_color = '\033[0m'; bold_font = '\033[1m'
yellow_color = '\033[93m' ; light_blue_color = '\033[94m' ; blue_color = '\033[34m'
print('⯧fr')

parser = MapParser(maps[0])
parser.parse_map()

drones = Simulator(parser)
# for drone in drones.drones:
    # print(drone.id, drone.current_zone, drone.waiting)
# graph = Graph(parser.zones, parser.connections)
# paths = Pathfinder(graph, parser).pathfinding()
# print(paths)
# renderer = Renderer(parser, parser.connections, paths)
# try:
#     arcade.run()
# except KeyboardInterrupt:
#     print(red_color, " \n\nProgram Ended.", end_color)

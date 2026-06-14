from parser import MapParser
from visualizer import Renderer
import os
import arcade
import warnings
from pathfinder import Pathfinder
from graph import Graph
from simulation import Drone, Simulator
from pydantic import ValidationError

warnings.filterwarnings("ignore")
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


red_color = '\033[91m'
green_color = '\033[92m'
end_color = '\033[0m'
bold_font = '\033[1m'
yellow_color = '\033[93m'
light_blue_color = '\033[94m'
blue_color = '\033[34m'

os.system("clear")
parser = MapParser(maps[0])
parser.parse_map()
r = Renderer(parser, parser.connections)
arcade.run()
lines = [
f"{green_color}███████╗{end_color} {blue_color}██╗     {end_color} {yellow_color}██╗   ██╗{end_color} {red_color}██╗{end_color} {light_blue_color}███╗   ██╗{end_color}",
f"{green_color}██╔════╝{end_color} {blue_color}██║     {end_color} {yellow_color}╚██╗ ██╔╝{end_color} {red_color}██║{end_color} {light_blue_color}████╗  ██║{end_color}",
f"{green_color}█████╗  {end_color} {blue_color}██║     {end_color} {yellow_color} ╚████╔╝ {end_color} {red_color}██║{end_color} {light_blue_color}██╔██╗ ██║{end_color}",
f"{green_color}██╔══╝  {end_color} {blue_color}██║     {end_color} {yellow_color}  ╚██╔╝  {end_color} {red_color}██║{end_color} {light_blue_color}██║╚██╗██║{end_color}",
f"{green_color}██║     {end_color} {blue_color}███████╗{end_color} {yellow_color}   ██║   {end_color} {red_color}██║{end_color} {light_blue_color}██║ ╚████║{end_color}",
f"{green_color}╚═╝     {end_color} {blue_color}╚══════╝{end_color} {yellow_color}   ╚═╝   {end_color} {red_color}╚═╝{end_color} {light_blue_color}╚═╝  ╚═══╝{end_color}",
f"\n{green_color}---------------By: mel-wahm---------------{end_color}",
]
for line in lines:
    print(line)
connections = Graph(parser.zones, parser.connections)
finder = Pathfinder(connections, parser)
path = finder.pathfinding()
finder.construct_path(path)
print('\n\n\n', green_color, finder.final_path, end_color, '\n\n\n')


#     for line in lines:
#         print(line)
#     arcade.run()
# except KeyboardInterrupt:
#     os.system("clear")
#     print(f"{bold_font}{green_color}--------------------------------------{end_color}")
#     print(f"{bold_font}{red_color} The program was stopped by the user{end_color}")
#     print(f"{bold_font}{green_color}--------------------------------------{end_color}")
#     print()
# except Exception as e:
#     print(f"{bold_font}{red_color}Error:", e)

# try:
#     parser = MapParser(maps[0])
#     parser.parse_map()
#     graph = Graph(parser.zones, parser.connections)
#     pathfinder = Pathfinder(graph, parser)
#     pathfinder.pathfinding()
#     print(pathfinder.final_path)
# except KeyboardInterrupt:
#     os.system("clear")
#     print(f"{bold_font}{green_color}--------------------------------------{end_color}")
#     print(f"{bold_font}{red_color} The program was stopped by the user{end_color}")
#     print(f"{bold_font}{green_color}--------------------------------------{end_color}")
#     print()
# except ValidationError as e:
#     for err in e.errors():
#         print(f"{red_color}Error", err['msg'], end_color)
# except Exception as e:
#     print(f"{bold_font}{red_color}Error:", e)




# try:
#     parser = MapParser(maps[0])
#     parser.parse_map()
#     graph = Graph(parser.zones, parser.connections)
#     drones = Simulator(parser)
#     # visualizer = Renderer(parser, parser.connections)
#     # arcade.run()
#     # for drone in drones.drones:
#     #     print(drone.id)
#     finder = Pathfinder(graph, parser)
#     finder.pathfinding()
#     print(finder.final_path)

# except KeyboardInterrupt:
#     os.system("clear")
#     print(f"{bold_font}{green_color}--------------------------------------{end_color}")
#     print(f"{bold_font}{red_color} The program was stopped by the user{end_color}")
#     print(f"{bold_font}{green_color}--------------------------------------{end_color}")
#     print()
# except ValidationError as e:
#     for err in e.errors():
#         print(f"{red_color}Error", err['msg'], end_color)
# except Exception as e:
#     print(f"{bold_font}{red_color}Error:", e)

# for map in maps:

from parser import MapParser ; from visualizer import Renderer ;import warnings
from pathfinder import Pathfinder ; from graph import Graph ; from simulation import Drone, Simulator
from pydantic import ValidationError; import arcade
from time import sleep
warnings.filterwarnings("ignore")
maps = [
    'maps/easy/01_linear_path.txt',  'maps/easy/02_simple_fork.txt', 'maps/easy/03_basic_capacity.txt',  
    'maps/medium/01_dead_end_trap.txt', 'maps/medium/02_circular_loop.txt', 'maps/medium/03_priority_puzzle.txt', 
    'maps/hard/01_maze_nightmare.txt',  'maps/hard/02_capacity_hell.txt', 'maps/hard/03_ultimate_challenge.txt', 
    'maps/challenger/01_the_impossible_dream.txt' #9
    ]
red_color = '\033[91m' ; green_color = '\033[92m' ; end_color = '\033[0m'; bold_font = '\033[1m'
yellow_color = '\033[93m' ; light_blue_color = '\033[94m' ; blue_color = '\033[34m'

# for map in maps:
#     print(map.split('/')[-1].split('.')[0], end=' ')
try:
    parser = MapParser(maps[7])
    parser.parse_map()
    graph = Graph(parser.zones, parser.connections)
    paths = Pathfinder(graph, parser).pathfinding()
    # for num, path in enumerate(paths):
        # for cost, path1 in path:
        # print(num + 1, ' -->', path)
    # print(paths)
    simu_paths = []
    for cost, path in paths.items():
        if cost < min(paths) + 1.5:
            for p in paths[cost]:
                simu_paths += [p]

    s_path = []
    for path in simu_paths:
        current_path = {}
        for key, value in zip(path, path[1:]):
            current_path[key] = value
        s_path.append(current_path)
    
    states = Simulator(parser, s_path, graph).simulating()
    # print(max(states))
    for turn, state in states.items():
        print(turn, ' --> ', state)
        print()
    instance = Renderer(parser, states)
    arcade.run()
    # print(states[max(states)])
    # Renderer(parser, states)
    # arcade.run()
except KeyboardInterrupt:
    print()

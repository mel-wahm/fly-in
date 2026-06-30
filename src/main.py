from parser import MapParser, NegativeError ; from visualizer import Renderer ;import warnings
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
scores = {
    maps[0]: 6,
    maps[1]: 8,
    maps[2]: 6,
    maps[3]: 12,
    maps[4]: 15,
    maps[5]: 12,
    maps[6]: 30,
    maps[7]: 35,
    maps[8]: 45,
    maps[9]: 45,
}
red_color = '\033[91m' ; green_color = '\033[92m' ; end_color = '\033[0m'; bold_font = '\033[1m'
yellow_color = '\033[93m' ; light_blue_color = '\033[94m' ; blue_color = '\033[34m'


try:
    parser = MapParser(maps[9])
    parser.parse_map()
    graph = Graph(parser)
    paths = Pathfinder(graph, parser).pathfinding()
    # print(paths)
    simu_paths = []
    for cost, path in paths.items():
        if cost < min(paths) + 0.7:
            for p in paths[cost]:
                simu_paths += [p]
    # simu_paths = paths[min(paths)]
    s_path = []
    for path in simu_paths:
        current_path = {}
        for key, value in zip(path, path[1:]):
            current_path[key] = value
        s_path.append(current_path)
    
    states = Simulator(parser, s_path, graph).simulating()
    
    instance = Renderer(parser, states)
    arcade.run()

except KeyboardInterrupt:
    print()
except ValidationError as e:
    for error in e.errors():
        print(bold_font, red_color, error['msg'], end_color, sep='')
except NegativeError as e:
    print(bold_font, red_color, e, end_color, sep='')
except ValueError as e:
    print(bold_font, red_color, e, end_color, sep='')

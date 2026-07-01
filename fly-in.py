import sys
from parser import MapParser, NegativeError
from visualizer import Renderer
import warnings
from pathfinder import Pathfinder
from graph import Graph
from simulation import Simulator
from pydantic import ValidationError
import arcade
warnings.filterwarnings("ignore")
red_color = '\033[91m'
green_color = '\033[92m'
end_color = '\033[0m'
bold_font = '\033[1m'
yellow_color = '\033[93m'
light_blue_color = '\033[94m'
blue_color = '\033[34m'

try:
    parser = MapParser(sys.argv[1])
    parser.parse_map()
    print(green_color, "Parsing successful", end_color, sep='')
    graph = Graph(parser)
    paths = Pathfinder(graph, parser).pathfinding()
    simu_paths = []
    for cost, path in paths.items():
        if cost < min(paths) + 0.7:
            for p in paths[cost]:
                simu_paths += [p]
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

from parser import MapParser
from models import Connection, Zone
from graph import Graph
import pprint

parser = MapParser("maps/easy/03_basic_capacity.txt")
parser.parse_map()

graph = Graph(parser.zones, parser.connections)
graph.adjacency_list()
for gr, d in graph.graph.items():
    print(gr, "---->", d)
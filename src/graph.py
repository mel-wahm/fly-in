from models import Zone, Connection
from typing import Dict, Tuple, List


class Graph():


    def __init__(self, zones, connections):
        self.zones : Dict[str, Zone] = zones 
        self.connections : List [Connection] = connections
        self.graph :  Dict[str, List[Tuple[str, int]]] = {}
        self.adjacency_list()


    def adjacency_list(self):
        for con in self.connections:
            first_zone, second_zone = con.connection
            cap = con.max_link_capacity
            if not self.graph.get(first_zone):
                self.graph[first_zone] = []
            if not self.graph.get(second_zone):
                self.graph[second_zone] = []
            self.graph[first_zone].append((second_zone, cap))
            self.graph[second_zone].append((first_zone, cap))

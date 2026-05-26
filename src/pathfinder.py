from graph import Graph
from parser import MapParser
from models import Zone_Role
from models import Zone_Type
import heapq


class Pathfinder():
    def __init__(self, graph: Graph, parser: MapParser):
        self.graph = graph
        self.zones = parser.zones
        self.distances = {zone: float("inf") for zone in self.zones}
        self.start_zone = None
        self.final_path = dict()
        for zone in self.distances:
            if self.zones[zone].role == Zone_Role.start_hub:
                self.distances[zone] = 0
                self.start_zone = zone
    
    def pathfinding(self):
        queue = []
        heapq.heappush(queue, (self.distances[self.start_zone], self.start_zone))
        visited = {}
        while queue:
            zone_cost, current_zone = heapq.heappop(queue)
            if current_zone in visited:
                continue
            else:
                for zone, _ in self.graph.graph[current_zone]:
                    if self.zones[zone].zone == Zone_Type.blocked:
                        continue
                    way = 2 if self.zones[zone].zone == Zone_Type.restricted else 1
                    print(way)

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
        self.end_zone = None
        self.final_path = []
        for zone in self.distances:
            if self.zones[zone].role == Zone_Role.start_hub:
                self.start_zone = zone
                self.distances[zone] = 0
            if self.zones[zone].role == Zone_Role.end_hub:
                self.end_zone = zone
    
    def pathfinding(self):
        queue = []
        came_from = {}
        heapq.heappush(queue, (self.distances[self.start_zone], self.start_zone))
        visited = set()

        while queue:
            zone_cost, current_zone = heapq.heappop(queue)
            if current_zone in visited:
                continue
            visited.add(current_zone)
            for zone, _ in self.graph.graph[current_zone]:
                if self.zones[zone].zone == Zone_Type.blocked:
                    continue
                way = 2 if self.zones[zone].zone == Zone_Type.restricted else 1
                if zone_cost + way < self.distances[zone]:
                    self.distances[zone] = way + zone_cost
                    heapq.heappush(queue, (self.distances[zone], zone))
                    came_from[zone] = current_zone
        if self.end_zone not in visited:
            raise ValueError("The goal zone is unreachable")
        #constructing path
        current_zone = self.end_zone
        self.final_path.append(current_zone)
        while True:
            current_zone = came_from[current_zone]
            self.final_path.append(current_zone)
            if current_zone == self.start_zone:
                break
        self.final_path = self.final_path[::-1]

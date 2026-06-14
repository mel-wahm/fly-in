from graph import Graph
from parser import MapParser
from models import Zone_Role
from models import Zone_Type
import heapq


class Pathfinder():
    def __init__(self, graph: Graph, parser: MapParser):
        self.graph = graph
        self.zones = parser.zones
        self.costs = {zone: float("inf") for zone in self.zones}
        self.start_zone = None
        self.end_zone = None
        self.final_path = []
        self.way_cost = {
            Zone_Type.normal: 1,
            Zone_Type.priority: 2,
            Zone_Type.restricted: 3,
            Zone_Type.blocked: 1
        }
        for zone_name, zone in self.zones.items():
            if zone.role == Zone_Role.start_hub:
                self.start_zone = zone_name
                self.costs[zone_name] = 0
            if zone.role == Zone_Role.end_hub:
                self.end_zone = zone_name


    def pathfinding(self):
        heap = [(0, self.start_zone)]
        came_from = {}

        while heap:
            current_cost, current_zone = heapq.heappop(heap)
            if current_cost > self.costs[current_zone]:
                continue 
            if current_zone == self.end_zone:
                break
            for next_zone, _ in self.graph.graph[current_zone]:
                next_type = self.zones[next_zone].zone
                if next_zone != self.end_zone and next_type == Zone_Type.blocked:
                    continue
                if self.costs[next_zone] > current_cost + self.way_cost[next_type]:
                    self.costs[next_zone] = current_cost + self.way_cost[next_type]
                    came_from[next_zone] = current_zone
                    heapq.heappush(heap, (self.costs[next_zone], next_zone))

        return came_from
    
    def construct_path(self, came_from):
        if self.end_zone not in came_from:
            raise ValueError("The End Goal Is Not Reachable.")
        self.final_path.append(self.end_zone)
        current_zone = self.end_zone
        while current_zone in came_from:
            current_zone = came_from[current_zone]
            self.final_path.append(current_zone)
        
        self.final_path = self.final_path[::-1]
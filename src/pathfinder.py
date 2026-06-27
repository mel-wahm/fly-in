from graph import Graph
from parser import MapParser
from models import Zone_Role
from models import Zone_Type
import heapq
from typing import Dict
from time import sleep

class Pathfinder():
    def __init__(self, graph: Graph, parser: MapParser):
        self.graph = graph
        self.zones = parser.zones
        self.costs = {zone: float("inf") for zone in self.zones}
        self.start_zone = None
        self.end_zone = None
        self.final_path = []
        self.way_cost = {
            Zone_Type.priority: 0.9,
            Zone_Type.normal: 1,
            Zone_Type.restricted: 3,
            Zone_Type.blocked: -1
        }
        for zone_name, zone in self.zones.items():
            if zone.role == Zone_Role.start_hub:
                self.start_zone = zone_name
            if zone.role == Zone_Role.end_hub:
                self.end_zone = zone_name


    def pathfinding(self):
        queue : list[tuple]= [(0, [self.start_zone])]
        paths : Dict[int, list] = {}
        total_paths_found = 0
        while queue and total_paths_found < 4:
            current_cost, current_path = heapq.heappop(queue)
            current_zone = current_path[-1]
            if current_zone == self.end_zone:
                if current_cost in paths:
                    paths[current_cost].append(current_path)
                else:
                    paths[current_cost] = [current_path]
                total_paths_found += 1
                continue
            for next_zone, next_mlc in self.graph.graph[current_zone]:
                max_drones = self.zones[next_zone].max_drones
                if next_zone in current_path:
                    continue
                next_type = self.way_cost[self.zones[next_zone].zone]
                if next_type == -1:
                    continue
                next_cost = next_type + (1 / min(next_mlc, max_drones))
                # print((current_cost + next_cost, current_path + [next_zone]))
                heapq.heappush(queue, (current_cost + next_cost, current_path + [next_zone]))
            # print('\n\n')
        if not paths:
            raise ValueError("The End Goal Is Not Reachable.")
        return paths

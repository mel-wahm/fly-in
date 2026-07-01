from typing import Any, Dict, List, Optional, Tuple
from parser import MapParser
from models import Zone_Type


class Drone():
    def __init__(self, id: str, current_zone: str) -> None:
        self.id = id
        self.current_zone = current_zone
        self.previous_zone: Optional[str] = None
        self.waiting = False
        self.arrived = False
        self.first_half = False

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return self.id


class Simulator():
    def __init__(self, parser: MapParser, path: List, graph: Any) -> None:
        self.graph = graph
        self.turns = 0
        self.states: Dict = {}
        self.parser = parser
        assert self.parser.start_hub is not None
        self.drones = [Drone("D" + str(i + 1),
                       self.parser.start_hub.name)
                       for i in range(self.parser.nb_drones)]
        self.path = path
        self.connections = {}
        for c in self.graph.connections:
            self.connections[c.connection] = c.max_link_capacity
        self.colors = {
            "Red": "\033[1;31m",
            "Green": "\033[1;32m",
            "Yellow": "\033[1;33m",
            "Blue": "\033[1;34m",
            "Purple": "\033[1;35m",
            "Cyan": "\033[1;36m",
            "White": "\033[1;37m",
            "End": "\033[0m"
        }

    def simulating(self) -> Dict:
        self.states[self.turns] = {d: d.current_zone for d in self.drones}
        while any(not drone.arrived for drone in self.drones):
            print(self.colors["Red"], self.turns + 1, self.colors["End"])
            final_connections: Dict[Tuple[str, str], int] = {}
            for id, drone in enumerate(self.drones):
                # skipping arrived or waiting drones
                if drone.arrived:
                    continue
                if drone.waiting:
                    print(self.colors["Green"], drone.id,
                          drone.current_zone, self.colors["End"])
                    drone.waiting = False
                    continue

                # initializing next_zone and
                # connections between it and the next zone
                next_zone = self.path[id % len(self.path)][drone.current_zone]
                direct_connection = (drone.current_zone, next_zone)\
                    in self.connections
                next_connection = (drone.current_zone, next_zone)\
                    if direct_connection else (next_zone, drone.current_zone)
                previous_connection = None
                assert self.parser.start_hub is not None
                if drone.current_zone != self.parser.start_hub.name:
                    direct_connection2 = (drone.previous_zone,
                                          drone.current_zone) \
                        in self.connections
                    previous_connection = (drone.previous_zone,
                                           drone.current_zone)\
                        if direct_connection2 else\
                        (drone.current_zone, drone.previous_zone)

                if self.parser.zones[next_zone].max_drones > 0 \
                   and self.connections[next_connection] > 0:
                    if self.parser.zones[next_zone].zone\
                     == Zone_Type.restricted:
                        drone.waiting = True
                        print(self.colors["Blue"], drone.id,
                              drone.current_zone, '-',
                              next_zone, self.colors["End"])

                    else:
                        print(self.colors["Green"],
                              drone.id, next_zone,
                              self.colors["End"])
                    # freeing space for coming drones
                    if previous_connection:
                        self.connections[previous_connection] += 1
                    self.parser.zones[drone.current_zone].max_drones += 1

                    # updating zones
                    drone.previous_zone = drone.current_zone
                    drone.current_zone = next_zone

                    # reserving space for drone in the next zone
                    self.connections[next_connection] -= 1
                    self.parser.zones[next_zone].max_drones -= 1
                    assert self.parser.end_hub is not None
                    if drone.current_zone == self.parser.end_hub.name:
                        drone.arrived = True
                        final_connections[next_connection]\
                            = final_connections.get(next_connection, 0) + 1
            print()

            for connection, count in final_connections.items():
                self.connections[connection] += count
            self.turns += 1
            self.states[self.turns] = {d: d.current_zone for d in self.drones}
        return self.states

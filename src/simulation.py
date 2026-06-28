from parser import MapParser
from time import sleep
from models import Zone_Type
class Drone():
    def __init__(self, id, current_zone):
        self.id = id
        self.current_zone = current_zone
        self.previous_zone = None
        self.waiting = False
        self.arrived = False
        self.first_half = False
    
    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
class Simulator():
    def __init__(self, parser: MapParser, path, graph):
        self.graph = graph
        self.drones = [Drone("D" + str(i + 1), parser.start_hub.name) for i in range(parser.nb_drones)]
        self.turns = 0
        self.states = {}
        self.parser = parser
        self.path = path
        self.connections = {}
        for connection in self.graph.connections:
            self.connections[connection.connection] = connection.max_link_capacity
        

    def simulating(self):
        self.states[self.turns] = {d:d.current_zone for d in self.drones}
        while any(not drone.arrived for drone in self.drones):
            final_connections = {}
            for id, drone in enumerate(self.drones):
                #skipping arrived or waiting drones
                if drone.arrived:
                    continue
                if drone.waiting:
                    drone.waiting = False
                    continue

                #initializing next_zone and connections between it and the next zone 
                next_zone = self.path[id % len(self.path)][drone.current_zone]
                direct_connection = (drone.current_zone, next_zone) in self.connections
                next_connection = (drone.current_zone, next_zone)\
                    if direct_connection else (next_zone, drone.current_zone)
                previous_connection = None
                if drone.current_zone != self.parser.start_hub.name:
                    direct_connection2 = (drone.previous_zone, drone.current_zone) in self.connections
                    previous_connection = (drone.previous_zone, drone.current_zone)\
                        if direct_connection2 else (drone.current_zone, drone.previous_zone)

                if self.parser.zones[next_zone].max_drones > 0 \
                    and self.connections[next_connection] > 0:
                    if self.parser.zones[next_zone].zone == Zone_Type.restricted:
                        drone.waiting = True

                    #freeing space for coming drones      
                    if previous_connection:
                        self.connections[previous_connection] += 1
                    self.parser.zones[drone.current_zone].max_drones += 1

                    #updating zones
                    drone.previous_zone = drone.current_zone
                    drone.current_zone = next_zone

                    #reserving space for drone in the next zone
                    self.connections[next_connection] -= 1
                    self.parser.zones[next_zone].max_drones -= 1
                    if drone.current_zone == self.parser.end_hub.name:
                        drone.arrived = True
                        final_connections[next_connection] = final_connections.get(next_connection, 0) + 1
            for connection, count in final_connections.items():
                self.connections[connection] += count
            self.turns += 1
            self.states[self.turns] = {d : d.current_zone for d in self.drones}
        for turn, state in self.states.items():
            print(turn, ' --> ', state)
            print()
        return self.states

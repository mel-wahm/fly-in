from parser import MapParser
from time import sleep
from models import Zone_Type
class Drone():
    def __init__(self, id, current_zone):
        self.id = id
        self.current_zone = current_zone
        self.waiting = False
        self.arrived = False

class Simulator():
    def __init__(self, parser: MapParser, path, graph):
        self.graph = graph
        self.drones = [Drone("D" + str(i + 1), parser.start_hub.name) for i in range(parser.nb_drones)]
        self.turns = 0
        self.states = {}
        self.parser = parser
        self.path = path
        self.capacities = {connection.connection[1]: connection.max_link_capacity 
                           for connection in parser.connections}
        self.connections = {}
        for connection in self.graph.connections:
            self.connections[connection.connection] = connection.max_link_capacity
        # print(self.capacities)        

    def simulating(self):
        while any(not drone.arrived for drone in self.drones):
            self.states[self.turns] = [(d.id, d.current_zone) for d in self.drones]
            for id, drone in enumerate(self.drones):
                #skipping arrived or waiting drones
                if drone.arrived:
                    continue
                if drone.current_zone == self.parser.end_hub.name:
                    drone.arrived = True
                    continue
                if drone.waiting:
                    drone.waiting = False
                    continue

                #initializing next_zone and connections between it and the next zone 
                next_zone = self.path[id % len(self.path)][drone.current_zone]
                direct_connection = self.connections.get((drone.current_zone, next_zone))
                connection = (drone.current_zone, next_zone) \
                    if direct_connection else (next_zone, drone.current_zone)
                print(connection)

                if self.parser.zones[next_zone].max_drones > 0:
                    if self.parser.zones[next_zone].zone == Zone_Type.restricted:
                        drone.waiting = True
                    self.parser.zones[drone.current_zone].max_drones += 1
                    self.connections[connection] += 1
                    drone.current_zone = next_zone
                    self.connections[connection] -= 1
                    self.parser.zones[next_zone].max_drones -= 1
            self.turns += 1
        return self.states

            


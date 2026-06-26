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
    def __init__(self, parser: MapParser, path):
        self.drones = [Drone("D" + str(i + 1), parser.start_hub.name) for i in range(parser.nb_drones)]
        self.turns = 0
        self.states = {}
        self.parser = parser
        self.path = path
        self.capacities = {connection.connection[1]: connection.max_link_capacity 
                           for connection in parser.connections}
        # print(self.capacities)        

    def simulating(self):
        while any(not drone.arrived for drone in self.drones):
            self.states[self.turns] = [(d.id, d.current_zone) for d in self.drones]
            for id, drone in enumerate(self.drones):
                if drone.current_zone == self.parser.end_hub.name:
                    drone.arrived = True
                    continue
                if drone.arrived:
                    continue
                if drone.waiting:
                    drone.waiting = False
                    continue
                next_zone = self.path[id % len(self.path)][drone.current_zone]
                if self.parser.zones[next_zone].max_drones :
                    if self.parser.zones[next_zone].zone == Zone_Type.restricted:
                        drone.waiting = True
                    if drone.current_zone != self.parser.start_hub.name:
                        self.parser.zones[drone.current_zone].max_drones += 1
                        # self.capacities[drone.current_zone] += 1
                    drone.current_zone = next_zone
                    self.parser.zones[next_zone].max_drones -= 1
                    # self.capacities[next_zone] -= 1
            self.turns += 1
        print(self.states)
        return self.states

            


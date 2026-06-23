from parser import MapParser

class Drone():
    def __init__(self, id, current_zone):
        self.id = id
        self.current_zone = current_zone
        self.waiting = False
        self.arrived = False

class Simulator():
    def __init__(self, parser: MapParser):
        self.drones = [Drone("D" + str(i + 1), parser.start_hub.name) for i in range(parser.nb_drones)]

        while all(not drone.arrived for drone in self.drones):
            for drone in self.drones:
                if drone.current_zone == parser.end_hub.name:
                    drone.arrived = True
                    continue
                
                



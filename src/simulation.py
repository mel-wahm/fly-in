from parser import MapParser

class Drone():
    def __init__(self, id):
        self.id = id
        self.pos = 0

class Simulator():
    def __init__(self, parser: MapParser):
        # self.drones = [Drone("D" + str(i + 1)) for i in range(parser.nb_drones)]
        pass
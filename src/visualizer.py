import arcade
from parser import MapParser

class Renderer(arcade.Window):
    def __init__(self):
        super().__init__(1280,  720,  "Charlie Kirk.")
    
    def on_draw(self):
        self.clear()


t = Renderer()
arcade.run()
import arcade
from math import sin

class Render(arcade.Window):
    def __init__(self):
        super().__init__(1980, 1080, "Rotation_")
        self.progress = 0

    def on_update(self, delta_time):
        self.progress += delta_time

    def on_draw(self):
        self.clear()
        base = sin(self.progress) * 10
        cx, cy = (self.width / 2, self.height / 2)
        arcade.draw_line(cx - base, cy - base, cx + base, cy + 100 + base, arcade.color.ORANGE_PEEL, 10)
Render()
arcade.run()

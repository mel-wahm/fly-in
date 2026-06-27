import arcade
from math import sin
class Render(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, 'testing window', fullscreen=True)
        self.progress = 0
    def on_update(self, delta_time):
        self.progress += delta_time * 5
    def on_draw(self):
        d = sin(self.progress) * 10
        self.clear()
        r, b, g, _ = arcade.color.WHITE
        arcade.draw_circle_filled(self.width / 2, self.height / 2, 80, arcade.color.GREEN)
        arcade.draw_circle_filled(self.width / 2, self.height / 2, 35 + d, (r, b, g, 150))
        arcade.draw_circle_filled(self.width / 2, self.height / 2, 22 + d, (r, b, g, 200))


if __name__ == "__main__":
    Render()
    arcade.run()
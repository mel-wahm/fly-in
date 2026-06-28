import arcade
# def mupper(s):
#     return s.upper()
colors = "RED GREEN BLUE YELLOW ORANGE PURPLE PINK WHITE BLACK GRAY CYAN MAGENTA MAROON OLIVE TEAL LIME GOLD BROWN SILVER".split()
# colors = ['OLIVE_DRAB']
class Renderer(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, fullscreen=True )
        self.drag_x = 0
        self.drag_y = 0

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.drag_x += dx
        self.drag_y += dy

    def on_draw(self):
        self.clear()
        for num, color in enumerate(colors):
            h , w = self.height // 2, self.width // 2
            if color == "BLACK":
                r, g, b = (26, 26, 26)
            else:
                r, g, b = getattr(arcade.color, color.upper())[:3]

            if num < len(colors) - 1:
                arcade.draw_line(w - 500 + num * 200 + self.drag_x, h + self.drag_y,
                                 w - 500 + num * 200 + 200 + self.drag_x, h + self.drag_y, (255, 255, 255), 6.56)
            arcade.draw_circle_filled(w - 500 + num * 200 + self.drag_x,
                                      h + self.drag_y, 40, (r, g, b, 30))
            arcade.draw_circle_filled(w - 500 + num * 200 + self.drag_x,
                                      h + self.drag_y, 31, (r, g, b, 47))
            arcade.draw_circle_filled(w - 500 + num * 200 + self.drag_x,
                                      h + self.drag_y, 25, (r, g, b, 255))

if __name__ == "__main__":
    Renderer()
    arcade.run()
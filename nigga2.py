import arcade

class Render(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, 'testing window', fullscreen=True)
    
    def on_draw(self):
        arcade.draw_circle_filled(self.width / 2, self.height / 2, 45, arcade.color.RED)
        arcade.draw_rect_outline(arcade.rect.XYWH(self.width / 2, self.height / 2, 100, 100), 
                                arcade.color.YALE_BLUE)
if __name__ == "__main__":
    colors = [c for c in dir(arcade.color) if c.isupper()]
    r, g, b, a = getattr(arcade.color, "NAVAJO_WHITE")
    print(r, g, b)
    # for color in colors:
    #     c = getattr(arcade.color, color)
    #     r, g, b, a = c
    #     # print(a)
    #     rr, gg, bb = (40, 150, 120)
    #     if a < 255:
    #         print(color)
    # Render()
    # arcade.run()
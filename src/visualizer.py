import arcade
import random
from models import Zone_Role

class Renderer(arcade.Window):
    def __init__(self, parser, connections):
        super().__init__(1980, 1080, parser.map_path, fullscreen=True)
        self.parser = parser
        self.connections = connections
        cors = [zone.coordinates for zone in self.parser.zones.values()]
        self.avg_x = sum(cor[0] for cor in cors) / len(cors)
        self.avg_y = sum(cor[1] for cor in cors) / len(cors)
        self.drag_x = 0
        self.drag_y = 0
        self.start_pos = parser
        self.wallpaper = arcade.load_texture('photos/wallpaper5.jpg')
        self.drone_png = arcade.load_texture('photos/drone2.png')
        self.t = 0
        for zone_name, zone in self.parser.zones.items():
            if zone.role == Zone_Role.start_hub:
                start_zone = zone_name
                self.start_pos = parser.zones[start_zone].coordinates
            elif zone.role == Zone_Role.end_hub:
                end_zone = zone_name
                self.end_pos = parser.zones[end_zone].coordinates
        

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.drag_x += dx
        self.drag_y += dy


    def on_update(self, delta_time):
        pass


    def on_draw(self):
        self.clear()
        w_rect = arcade.rect.XYWH(self.width / 2, self.height / 2, 1920, 1080)
        arcade.draw_texture_rect(self.wallpaper, w_rect)
        pos_x = (self.width / 2) + self.drag_x
        pos_y = (self.height / 2) + self.drag_y

        #drawing connection
        for con in self.connections:
            x_cord1, y_cord1 = self.parser.zones[con.connection[0]].coordinates 
            x_cord2, y_cord2 = self.parser.zones[con.connection[1]].coordinates
            x_cord1 = pos_x + (x_cord1 - self.avg_x) * 150
            y_cord1 = pos_y + (y_cord1 - self.avg_y) * 150
            x_cord2 = pos_x + (x_cord2 - self.avg_x) * 150
            y_cord2 = pos_y + (y_cord2 - self.avg_y) * 150
            arcade.draw_line(x_cord1, y_cord1, x_cord2, y_cord2, arcade.color.WHITE, 7)

        #drawing zones
        for name, zone in self.parser.zones.items():
            self.t += self.delta_time * 30
            # print(self.t)
            sx, sy = self.start_pos
            sy = self.height / 2 + (sy - self.avg_y) * 150
            sx = self.width / 2 + (sx - self.avg_x) * 150 + self.t
            ex, ey = self.end_pos
            d_rect = arcade.rect.XYWH(sx + self.drag_x, sy + self.drag_y, 40, 40)
            color = arcade.color.LIGHT_BLUE
            if zone.color:
                try:
                    color_name = zone.color.upper().replace("DARK", "DARK_")\
                        .replace("LIGHT", "LIGHT_").replace("__", "_")
                    color = getattr(arcade.color, color_name)
                except Exception:
                        pass
            x, y = zone.coordinates
            arcade.draw_circle_filled(pos_x + (x - self.avg_x) * 150,
                                      pos_y + (y - self.avg_y) * 150,
                                      30, color)
            arcade.draw_text(name, pos_x + (x - self.avg_x) * 150,
                             pos_y + 45 + (y - self.avg_y) * 150,
                             arcade.color.WHITE, 12, anchor_x="center")
            arcade.draw_texture_rect(self.drone_png, d_rect)

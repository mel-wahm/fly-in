import arcade

from models import Zone_Role
from pathfinder import Pathfinder
from math import sqrt


class Renderer(arcade.Window):
    def center_coordinates(self, coords: tuple[int, int]):
        x, y = coords
        x = (self.width / 2) + self.drag_x + (x - self.avg_x) * 150
        y = (self.height / 2) + self.drag_y + (y - self.avg_y) * 150
        return (x, y)


    def __init__(self, parser, connections, final_path):
        super().__init__(1980, 1080, parser.map_path)
        self.parser = parser
        self.connections = connections
        self.final_path = final_path
        self.speed = 150
        self.sec = 0
        # average map coordinates, used to center everything on screen
        cors = [zone.coordinates for zone in self.parser.zones.values()]
        self.avg_x = sum(cor[0] for cor in cors) / len(cors)
        self.avg_y = sum(cor[1] for cor in cors) / len(cors)
        # drag offset for panning the map
        self.drag_x = 0
        self.drag_y = 0

        # textures
        self.wallpaper = arcade.load_texture('photos/wallpaper7.jpg')
        self.drone_png = arcade.load_texture('photos/drone2.png')

        self.index = 1

        # self.next = self.center_coordinates(self.parser.zones[self.final_path[1]].coordinates)
        
        # find start/end hub positions
        for zone_name, zone in self.parser.zones.items():
            if zone.role == Zone_Role.start_hub:
                start_zone = zone_name
                self.start_pos = parser.zones[start_zone].coordinates
            elif zone.role == Zone_Role.end_hub:
                end_zone = zone_name
                self.end_pos = parser.zones[end_zone].coordinates

        self.drone_x, self.drone_y = self.center_coordinates(self.start_pos)
        


    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.drag_x += dx
        self.drag_y += dy
        self.drone_x += dx
        self.drone_y += dy

    def on_update(self, delta_time):
        road_len = len(self.final_path)
        # for a, b in zip(range(road_len), range(1, road_len)):
        #     current_zone = self.parser.zones[self.final_path[a]]
        #     next_zone = self.parser.zones[self.final_path[b]]
        #     cx, cy = current_zone.coordinates
        #     nx, ny = next_zone.coordinates
        #     sx = self.width / 2 + (cx - self.avg_x) * 150
        #     sy = self.height / 2 + (cy - self.avg_y) * 150
        #     ex = self.width / 2 + (nx - self.avg_x) * 150
        #     ey= self.height / 2 + (ny - self.avg_y) * 150
        #     while self.dx < ex or self.dy < ey:
        #         delta_x = ex - sx
        #         delta_y = ey - sy
        #         hypo = sqrt(delta_x ** 2 + delta_y ** 2)

        #         x_rate = delta_x / hypo
        #         y_rate = delta_y / hypo
        #         budget = self.delta_time * self.speed

        #         self.dx += x_rate * budget
        #         self.dy += y_rate * budget
        #         d_rect = arcade.rect.XYWH(self.dx, self.dy, 30, 30)



    def on_draw(self):
        self.clear()

        # background
        w_rect = arcade.rect.XYWH(self.width / 2, self.height / 2, 1920, 1080)
        arcade.draw_texture_rect(self.wallpaper, w_rect)

        

        # --- draw connections ---
        for con in self.connections:
            x_cord1, y_cord1 = self.center_coordinates(self.parser.zones[con.connection[0]].coordinates)
            x_cord2, y_cord2 = self.center_coordinates(self.parser.zones[con.connection[1]].coordinates)
            arcade.draw_line(x_cord1, y_cord1, x_cord2, y_cord2, arcade.color.WHITE, 10)

        # --- draw zones ---

        arcade.rect.XYWH(self.drone_x, self.drone_y, 30, 30)
        for name, zone in self.parser.zones.items():
            # zone color
            color = arcade.color.LIGHT_BLUE
            if zone.color:
                try:
                    color_name = zone.color.upper().replace("DARK", "DARK_") \
                        .replace("LIGHT", "LIGHT_").replace("__", "_")
                    color = getattr(arcade.color, color_name)
                except Exception:
                    pass

            x, y = self.center_coordinates(zone.coordinates)

            arcade.draw_circle_filled(x, y, 30, color)
            arcade.draw_text(name, x, y + 45,
                              arcade.color.WHITE, 12, anchor_x="center")

        
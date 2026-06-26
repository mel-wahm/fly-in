import arcade

from models import Zone_Role
from pathfinder import Pathfinder
from math import sqrt


class Renderer(arcade.Window):
    def center_coordinates(self, coords: tuple[int, int]):
        x, y = coords
        x = (self.width / 2) + self.drag_x + (x - self.avg_x) * 160
        y = (self.height / 2) + self.drag_y + (y - self.avg_y) * 160
        return (x, y)


    def __init__(self, parser, states):
        super().__init__(1980, 1080, parser.map_path)
        self.parser = parser
        self.connections = parser.connections
        self.speed = 150
        self.states = states
        # for turn, state in self.states.items():
        #     print(turn, ' --> ', state)
        # average map coordinates, used to center everything on screen
        cors = [zone.coordinates for zone in self.parser.zones.values()]
        xs = [c[0] for c in cors]
        ys = [c[1] for c in cors]

        self.avg_x = (min(xs) + max(xs)) / 2
        self.avg_y = (min(ys) + max(ys)) / 2
        # drag offset for panning the map
        self.drag_x = 0
        self.drag_y = 0

        # textures
        self.drone_png = arcade.load_texture('photos/drone2.png')
        self.wallpaper = arcade.load_texture('photos/wallpaper7.jpg')
        self.index = 1

        # find start/end hub positions
        for zone_name, zone in self.parser.zones.items():
            if zone.role == Zone_Role.start_hub:
                start_zone = zone_name
                self.start_pos = parser.zones[start_zone].coordinates
            elif zone.role == Zone_Role.end_hub:
                end_zone = zone_name
                self.end_pos = parser.zones[end_zone].coordinates
        self.drone_x, self.drone_y = self.center_coordinates(self.start_pos)

        #indexs
        self.turns = 0
        self.times = 0
        
    # def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
    #     if scroll_y > 0:
    #         self.zoom *= 1.1
    #     elif scroll_y < 0:
    #         self.zoom /= 1.1
    #     self.zoom = max(0.1, min(self.zoom, 10))

    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.drag_x += dx
        self.drag_y += dy

    def on_update(self, delta_time):
        self.times += delta_time
        if self.times > 1 and self.turns < len(self.states) - 1:
            self.turns += 1
            self.times = 0
        else:
            return

        


    def on_draw(self):
        # self.wallpaper = arcade.load_texture('photos/video_frames/frame_'+ f"{self.index % 565 + 1:05d}" +'.jpg')
        # if self.index > 565:
        #     self.index = 1
        
        # self.index += 1
        self.clear()

        # background
        w_rect = arcade.rect.XYWH(self.width / 2, self.height / 2, 1920, 1080)
        arcade.draw_texture_rect(self.wallpaper, w_rect)

        

        # --- draw connections ---
        for con in self.connections:
            x_cord1, y_cord1 = self.center_coordinates(self.parser.zones[con.connection[0]].coordinates)
            x_cord2, y_cord2 = self.center_coordinates(self.parser.zones[con.connection[1]].coordinates)
            arcade.draw_line(x_cord1, y_cord1, x_cord2, y_cord2, arcade.color.WHITE, 4)

        # --- draw zones ---

        arcade.rect.XYWH(self.drone_x, self.drone_y, 15, 15)
        for name, zone in self.parser.zones.items():
            # zone color
            color = arcade.color.LIGHT_BLUE
            if zone.color:
                if zone.color.upper() == 'BLACK':
                    color = arcade.color.WHITE
                else:
                    try:
                        color_name = zone.color.upper().replace("DARK", "DARK_") \
                            .replace("LIGHT", "LIGHT_").replace("__", "_")
                        color = getattr(arcade.color, color_name)
                    except Exception:
                        pass

            x, y = self.center_coordinates(zone.coordinates)
            
            

            # arcade.draw_circle_filled(x, y, 25, getattr(arcade.color, self.outlines[name]))
            arcade.draw_circle_filled(x, y, 20, color)
            name='\n'.join(name.split('_'))
            for i, line in enumerate(name.split('\n')):
                arcade.draw_text(line, x, y + 65 - i * 15,
                                arcade.color.WHITE, 12, anchor_x="center")
        for _, zone in self.states[self.turns]:
            x, y = self.center_coordinates(self.parser.zones[zone].coordinates)
            arcade.draw_circle_filled(x, y, 10, arcade.color.RED)

        
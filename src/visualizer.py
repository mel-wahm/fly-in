import arcade

from models import Zone_Role, Zone_Type
from pathfinder import Pathfinder
from math import sin

class Renderer(arcade.Window):
    def center_coordinates(self, coords: tuple[int, int]):
        x, y = coords
        x = (self.width / 2) + self.drag_x + (x - self.avg_x) * 160
        y = (self.height / 2) + self.drag_y + (y - self.avg_y) * 160
        return (x, y)


    def __init__(self, parser, states):
        super().__init__(1980, 1080, parser.map_path, fullscreen=False)
        self.parser = parser
        self.connections = parser.connections
        self.speed = 150
        self.states = states
        self.progress = 0

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
        self.progress += delta_time * 3

    def on_draw(self):
        second = int(self.time)
        # self.wallpaper = arcade.load_texture('photos/video_frames/frame_'+ f"{self.index % 565 + 1:05d}" +'.jpg')
        # if self.index > 565:
        #     self.index = 1
        
        # self.index += 1
        self.clear()

        # background
        r, g, b = arcade.color.RIFLE_GREEN[:3]
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height),
            (r, g, b, 55)
        )

        for g in range(0, self.height, 4):
                arcade.draw_line(0, g, self.width, g, (222, 222, 222, 70))
        for g in range(0, self.height, 80):
                arcade.draw_line(0, g, self.width, g, (240, 198, 162, 80))
        for g in range(0, self.width, 80):
                arcade.draw_line(g, 0, g, self.height, (240, 198, 162, 80))
# 
        # arcade.draw_rect_outline(arcade.rect.XYWH(self.width / 2, self.height / 2,
                                    # 1500, 830), arcade.color.YELLOW, 1, 0)

        # --- draw connections ---
        for con in self.connections:
            color = arcade.color.LIGHT_BLUE
            first_zone = self.parser.zones[con.connection[0]]
            if first_zone.color:
                if first_zone.color.upper() == 'BLACK':
                    color = arcade.color.WHITE
                else:
                    try:
                        color_name = first_zone.color.upper().replace("DARK", "DARK_") \
                            .replace("LIGHT", "LIGHT_").replace("__", "_")
                        color = getattr(arcade.color, color_name)
                    except Exception:
                        pass

            x_cord1, y_cord1 = self.center_coordinates(self.parser.zones[con.connection[0]].coordinates)
            x_cord2, y_cord2 = self.center_coordinates(self.parser.zones[con.connection[1]].coordinates)
            arcade.draw_line(x_cord1, y_cord1, x_cord2, y_cord2, color, 4)

        arcade.rect.XYWH(self.drone_x, self.drone_y, 15, 15)
        self.turns += 1
        # --- draw zones ---

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
            
            r, g, b = color[:3]
            increment = sin(self.progress) * 5

            arcade.draw_circle_filled(x, y, 48 + increment, (r, g, b, 30))
            arcade.draw_circle_filled(x, y, 42 + increment, (r, g, b, 60))
            arcade.draw_circle_filled(x, y, 38 + increment, (r, g, b, 90))
            arcade.draw_circle_filled(x, y, 32, color)

            name='\n'.join(name.split('_'))
            for i, line in enumerate(name.split('\n')):
                arcade.draw_text(line, x, y + 65 - i * 15,
                                arcade.color.WHITE, 12, anchor_x="center")  

        if second in self.states:
            for drone, current_zone in self.states[second].items():
                if second < len(self.states) - 2:
                    next_zone = self.parser.zones[self.states[second + 1][drone]]
                    if next_zone.zone == Zone_Type.restricted:
                        if not drone.first_half:
                            drone.first_half = True
                            # cx, cy = self.center_coordinates(self.parser.zones[next_zone.name].coordinates) 
                        else:
                            drone.first_half = False
                x, y = self.center_coordinates(self.parser.zones[current_zone].coordinates)
                # if drone.first_half:
                #     x, y = ((x + cx) // 2, (y + cy) // 2)
                arcade.draw_circle_filled(x, y, 25 + increment, (0, 0, 0, 120))
                arcade.draw_circle_filled(x, y, 20 + increment, (0, 0, 0, 190))
                arcade.draw_circle_filled(x, y, 15, arcade.color.BLACK)
                arcade.draw_text(drone.id, x, y, arcade.color.WHITE,
                                 15, anchor_x='center', anchor_y='center')
            # exit()
        else:
            arcade.draw_circle_filled(x, y, 25 + increment, (0, 0, 0, 120))
            arcade.draw_circle_filled(x, y, 20 + increment, (0, 0, 0, 190))
            arcade.draw_circle_filled(x, y, 15, arcade.color.BLACK)
            arcade.draw_text(f'D{len(self.states[0])}', x, y, arcade.color.WHITE,
                                15, anchor_x='center', anchor_y='center')

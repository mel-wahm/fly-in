import arcade
from models import Zone_Role, Zone_Type
from math import sin  # , cos, radians
from typing import Any, Tuple


class Renderer(arcade.Window):
    def center_coordinates(self,
                           coords: tuple[int, int]) -> Tuple[float, float]:
        x, y = coords
        x = (self.width / 2) + self.drag_x + (x - self.avg_x) * 160
        y = (self.height / 2) + self.drag_y + (y - self.avg_y) * 160
        return (x, y)

    def __init__(self, parser: Any, states: Any):
        super().__init__(1980, 1080,
                         parser.map_path, fullscreen=True, vsync=True)
        self.parser = parser
        self.connections = parser.connections
        self.states = states
        self.zone_progress: float = 0
        self.wall_progress: float = 0
        self.pause = False
        self.second = 0
        self.sec: float = 0
        self.wallpaper = arcade.rect.XYWH(self.width / 2,
                                          self.height / 2, 1980, 1080)
        cors = [zone.coordinates for zone in self.parser.zones.values()]
        xs = [c[0] for c in cors]
        ys = [c[1] for c in cors]

        self.avg_x = (min(xs) + max(xs)) / 2
        self.avg_y = (min(ys) + max(ys)) / 2
        self.drag_x: float = 0
        self.drag_y: float = 0

        for zone_name, zone in self.parser.zones.items():
            if zone.role == Zone_Role.start_hub:
                self.start_pos = parser.zones[zone_name].coordinates
        self.drone_x, self.drone_y = self.center_coordinates(self.start_pos)

        self.turns = 0

    def draw_drone(self, x: float, y: float, name: Any) -> None:
        arcade.draw_circle_filled(x, y, 18, (255, 0, 40, 50), num_segments=100)
        arcade.draw_circle_filled(x, y, 13,
                                  (255, 0, 40, 120), num_segments=100)

        arcade.draw_circle_filled(x, y, 9, arcade.color.RED, num_segments=100)
        arcade.draw_circle_outline(x, y,
                                   9, arcade.color.WHITE, 2, num_segments=100)

        arcade.draw_rect_filled(arcade.rect.XYWH(x, y - 18, 24, 14),
                                (0, 0, 0, 190))
        arcade.draw_text(
            str(name),
            x,
            y - 18,
            arcade.color.WHITE,
            9,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    def on_mouse_drag(
        self, x: float, y: float, dx: float,
        dy: float, _buttons: int, _modifiers: int
    ) -> None:
        self.drag_x += dx
        self.drag_y += dy

    def on_update(self, delta_time: float) -> None:
        self.zone_progress += delta_time * 3
        self.wall_progress += delta_time * 120
        if not self.pause:
            self.sec += delta_time
            if self.sec >= 1:
                self.sec = 0
                self.second += 1

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.SPACE:
            if self.pause:
                self.pause = False
            else:
                self.pause = True
        if symbol == arcade.key.Q:
            print('Closing Fly-In.')
            exit()

    def on_draw(self) -> None:
        # self.second = int(self.time)
        self.clear()

        r, g, b = arcade.color.RIFLE_GREEN[:3]
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.width / 2,
                             self.height / 2, self.width, self.height),
            (r, g, b, 55),
        )
        arcade.draw_rect_filled(self.wallpaper, (6, 16, 18))
        for g in range(0, self.height, 6):
            arcade.draw_line(0, g, self.width, g, (30, 55, 40, 30), 2)
        for g in range(0, self.width, 6):
            arcade.draw_line(g, 0, g, self.height, (30, 55, 40, 30), 2)
        # cx = self.width / 2
        # cy = self.height / 2
        # for i in range(100):
        #     angle = self.wall_progress - i * 1
        #     nx = cx + 2000 * cos(radians(angle))
        #     ny = cy + 1000 * sin(radians(angle))
        #     arcade.draw_line(cx, cy, nx, ny,
        #                      (60, 200, 120, max(0, 150 - i * 10)), 2)

        for con in self.connections:
            color = arcade.color.LIGHT_BLUE
            first_zone = self.parser.zones[con.connection[0]]
            if first_zone.color:
                if first_zone.color.upper() == "BLACK":
                    color = arcade.color.WHITE
                else:
                    try:
                        color_name = (
                            first_zone.color.upper()
                            .replace("DARK", "DARK_")
                            .replace("LIGHT", "LIGHT_")
                            .replace("__", "_")
                        )
                        color = getattr(arcade.color, color_name)
                    except Exception:
                        pass

            x_cord1, y_cord1 = self.center_coordinates(
                self.parser.zones[con.connection[0]].coordinates
            )
            x_cord2, y_cord2 = self.center_coordinates(
                self.parser.zones[con.connection[1]].coordinates
            )
            arcade.draw_line(x_cord1, y_cord1,
                             x_cord2, y_cord2, arcade.color.WHITE, 3)
            r, g, b = color[:3]
            arcade.draw_line(x_cord1, y_cord1,
                             x_cord2, y_cord2, (r, g, b, 90), 9)
            arcade.draw_line(x_cord1, y_cord1,
                             x_cord2, y_cord2, (r, g, b, 60), 11)
            arcade.draw_line(x_cord1, y_cord1,
                             x_cord2, y_cord2, (r, g, b, 30), 13)

        for name, zone in self.parser.zones.items():
            color = arcade.color.LIGHT_BLUE
            if zone.color:
                if zone.color.upper() == "BLACK":
                    color = arcade.color.WHITE
                else:
                    try:
                        color_name = (
                            zone.color.upper()
                            .replace("DARK", "DARK_")
                            .replace("LIGHT", "LIGHT_")
                            .replace("__", "_")
                        )
                        color = getattr(arcade.color, color_name)
                    except Exception:
                        pass

            x, y = self.center_coordinates(zone.coordinates)
            r, g, b = color[:3]
            increment = sin(self.zone_progress) * 5

            arcade.draw_circle_filled(x, y, 38 + increment, (r, g, b, 30))
            arcade.draw_circle_filled(x, y, 32 + increment, (r, g, b, 60))
            arcade.draw_circle_filled(x, y, 28 + increment, (r, g, b, 90))
            arcade.draw_circle_filled(x, y, 22, color)

            name = "\n".join(name.split("_"))
            for i, line in enumerate(name.split("\n")):
                arcade.draw_text(
                    line, x, y + 65 - i * 15,
                    arcade.color.WHITE, 12, anchor_x="center"
                )

        if self.second in self.states:
            for drone, current_zone in self.states[self.second].items():
                x, y = self.center_coordinates(
                    self.parser.zones[current_zone].coordinates
                )
                prev_zone = self.parser.zones[
                    self.states[max(0, self.second - 1)][drone]
                ]
                px, py = self.center_coordinates(prev_zone.coordinates)
                next_idx = min(len(self.states) - 1, self.second + 1)
                doubled = self.states[next_idx][drone] == current_zone
                current_zone_obj = self.parser.zones[current_zone]
                restricted = (
                    current_zone_obj.zone == Zone_Type.restricted
                )
                if doubled and restricted:
                    self.draw_drone((x + px) / 2, (y + py) / 2, drone.id)
                else:
                    self.draw_drone(x, y, drone.id)

        else:
            x, y = self.center_coordinates(self.parser.end_hub.coordinates)
            self.draw_drone(x, y, f"D{len(self.states[0])}")

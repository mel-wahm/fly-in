import arcade
import math

class Render(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, 'Drone Sketching', fullscreen=True)
        cx, cy = self.width / 2, self.height / 2
        self.label = arcade.Text('DRONE_X', cx, cy - 30,
                                 (60, 180, 60), font_size=10,
                                 anchor_x='center', anchor_y='center',
                                 bold=True, font_name='monospace')

    def on_draw(self):
        self.clear()
        cx, cy = self.width // 2, self.height // 2

        motors = [
            (cx - 140, cy + 140),
            (cx + 140, cy + 140),
            (cx - 140, cy - 140),
            (cx + 140, cy - 140),
        ]

        # arms
        for mx, my in motors:
            arcade.draw_line(cx, cy, mx, my, (60, 60, 60), 12)

        # propeller blades
        prop_colors = [(20, 110, 20), (110, 20, 20), (110, 20, 20), (20, 110, 20)]
        for (mx, my), col in zip(motors, prop_colors):
            for angle_deg in [45, 135]:
                a = math.radians(angle_deg)
                bx, by = math.cos(a) * 44, math.sin(a) * 44
                arcade.draw_line(mx - bx, my - by, mx + bx, my + by, col, 10)

        # motor mounts
        for mx, my in motors:
            arcade.draw_circle_filled(mx, my, 28, (35, 35, 35))
            arcade.draw_circle_outline(mx, my, 28, (70, 70, 70), 2)
            arcade.draw_circle_filled(mx, my, 8, (80, 80, 80))

        # body
        arcade.draw_rect_filled(arcade.rect.XYWH(cx, cy, 250, 240), (25, 25, 25))
        arcade.draw_rect_outline(arcade.rect.XYWH(cx, cy, 250, 240), (60, 60, 60), 2)

        # camera
        arcade.draw_circle_filled(cx, cy + 80, 14, (10, 10, 25))
        arcade.draw_circle_outline(cx, cy + 80, 14, (80, 80, 130), 2)
        arcade.draw_circle_filled(cx, cy + 80, 6, (5, 5, 15))

        # direction arrow
        arcade.draw_triangle_filled(cx, cy + 102, cx - 9, cy + 90, cx + 9, cy + 90,
                                    (0, 200, 60, 200))

        # front LEDs
        arcade.draw_circle_filled(cx - 20, cy + 68, 5, (0, 200, 50))
        arcade.draw_circle_filled(cx + 20, cy + 68, 5, (0, 200, 50))

        # rear LEDs
        arcade.draw_circle_filled(cx - 20, cy - 68, 5, (200, 30, 30))
        arcade.draw_circle_filled(cx + 20, cy - 68, 5, (200, 30, 30))

        # antenna
        arcade.draw_line(cx + 18, cy + 92, cx + 32, cy + 112, (100, 100, 100), 2)
        arcade.draw_circle_filled(cx + 32, cy + 112, 4, (180, 40, 40))

        self.label.draw()


try:
    Render()
    arcade.run()
except KeyboardInterrupt:
    print("\033[35mExiting...")
    exit()

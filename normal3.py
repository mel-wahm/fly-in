import arcade
from math import sin, cos, pi

class Render(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, 'drone', fullscreen=True)
        self.progress = 0

    def on_update(self, delta_time):
        self.progress += delta_time * 3

    def on_draw(self):
        self.clear()
        cx, cy = self.width / 2, self.height / 2
        t = self.progress

        arm_len = 100
        motors = [
            (cx - arm_len, cy + arm_len),  # NW
            (cx + arm_len, cy + arm_len),  # NE
            (cx - arm_len, cy - arm_len),  # SW
            (cx + arm_len, cy - arm_len),  # SE
        ]

        # shadow
        arcade.draw_circle_filled(cx, cy + 5, 185, (0, 0, 0, 30))

        # arms
        for mx, my in motors:
            arcade.draw_line(cx, cy, mx, my, (40, 40, 40), 14)
            arcade.draw_line(cx, cy, mx, my, (55, 55, 55), 8)

        # propellers
        for i, (mx, my) in enumerate(motors):
            spin = t * (1.8 if i % 2 == 0 else -1.8)
            prop_color = (20, 130, 20, 180) if i % 2 == 0 else (130, 20, 20, 180)
            glow_color = (20, 180, 20, 60) if i % 2 == 0 else (180, 20, 20, 60)
            # glow ring
            arcade.draw_circle_filled(mx, my, 58, glow_color)
            # blades
            for b in range(2):
                angle = spin + b * pi / 2
                bx = cos(angle) * 54
                by = sin(angle) * 54
                # blade shape with two lines for thickness
                for off in [-4, 0, 4]:
                    ox = cos(angle + pi/2) * off
                    oy = sin(angle + pi/2) * off
                    arcade.draw_line(mx - bx + ox, my - by + oy,
                                     mx + bx + ox, my + by + oy,
                                     prop_color, 5)

        # motor mounts
        for mx, my in motors:
            arcade.draw_circle_filled(mx, my, 26, (20, 20, 20))
            arcade.draw_circle_outline(mx, my, 26, (70, 70, 70), 2)
            arcade.draw_circle_outline(mx, my, 20, (55, 55, 55), 2)
            arcade.draw_circle_filled(mx, my, 8, (90, 90, 90))
            arcade.draw_circle_filled(mx, my, 4, (50, 50, 50))

        # main body
        arcade.draw_rect_filled(arcade.rect.XYWH(cx, cy, 148, 148), (22, 22, 22))
        arcade.draw_rect_outline(arcade.rect.XYWH(cx, cy, 148, 148), (65, 65, 65), 2)

        # body grid lines
        for dx in [-24, 0, 24]:
            arcade.draw_line(cx + dx, cy - 74, cx + dx, cy + 74, (38, 38, 38), 1)
        for dy in [-24, 0, 24]:
            arcade.draw_line(cx - 74, cy + dy, cx + 74, cy + dy, (38, 38, 38), 1)

        # FC board
        arcade.draw_rect_filled(arcade.rect.XYWH(cx, cy + 10, 68, 58), (12, 30, 12))
        arcade.draw_rect_outline(arcade.rect.XYWH(cx, cy + 10, 68, 58), (35, 90, 35), 1)
        # FC chip
        arcade.draw_rect_filled(arcade.rect.XYWH(cx, cy + 14, 36, 30), (15, 50, 15))
        arcade.draw_rect_outline(arcade.rect.XYWH(cx, cy + 14, 36, 30), (40, 110, 40), 1)
        # FC corner pins
        for px, py in [(-28, 6), (28, 6), (-28, 34), (28, 34)]:
            arcade.draw_circle_filled(cx + px, cy + py, 3, (30, 90, 30))
        # FC label
        arcade.draw_text("FC", cx, cy + 14, (70, 180, 70), 11,
                         anchor_x="center", anchor_y="center",
                         font_name="monospace", bold=True)

        # camera housing
        arcade.draw_rect_filled(arcade.rect.XYWH(cx, cy + 62, 46, 30), (12, 12, 12))
        arcade.draw_rect_outline(arcade.rect.XYWH(cx, cy + 62, 46, 30), (80, 80, 80), 1)
        # gimbal rail
        arcade.draw_line(cx - 20, cy + 56, cx + 20, cy + 56, (55, 55, 55), 1)
        # lens rings
        arcade.draw_circle_filled(cx, cy + 62, 11, (8, 8, 20))
        arcade.draw_circle_outline(cx, cy + 62, 11, (100, 100, 140), 2)
        arcade.draw_circle_filled(cx, cy + 62, 7, (5, 5, 15))
        arcade.draw_circle_outline(cx, cy + 62, 7, (80, 80, 120), 1)
        arcade.draw_circle_filled(cx, cy + 62, 4, (3, 3, 12))
        # lens glint
        arcade.draw_circle_filled(cx - 3, cy + 59, 2, (160, 160, 200, 180))

        # front direction arrow
        arcade.draw_triangle_filled(cx, cy + 84, cx - 9, cy + 71, cx + 9, cy + 71,
                                    (0, 220, 60, 200))

        # front LEDs (green, pulsing)
        pulse = int(180 + sin(t * 4) * 60)
        arcade.draw_circle_filled(cx - 19, cy + 53, 6, (0, pulse, 50))
        arcade.draw_circle_outline(cx - 19, cy + 53, 8, (0, pulse, 50, 80), 2)
        arcade.draw_circle_filled(cx + 19, cy + 53, 6, (0, pulse, 50))
        arcade.draw_circle_outline(cx + 19, cy + 53, 8, (0, pulse, 50, 80), 2)

        # rear LEDs (red)
        rpulse = int(180 + sin(t * 4 + pi) * 60)
        arcade.draw_circle_filled(cx - 19, cy - 53, 6, (rpulse, 30, 30))
        arcade.draw_circle_outline(cx - 19, cy - 53, 8, (rpulse, 30, 30, 80), 2)
        arcade.draw_circle_filled(cx + 19, cy - 53, 6, (rpulse, 30, 30))
        arcade.draw_circle_outline(cx + 19, cy - 53, 8, (rpulse, 30, 30, 80), 2)

        # battery
        arcade.draw_rect_filled(arcade.rect.XYWH(cx, cy - 52, 88, 26), (22, 22, 5))
        arcade.draw_rect_outline(arcade.rect.XYWH(cx, cy - 52, 88, 26), (120, 120, 20), 1)
        # battery cells
        for i, bx in enumerate([-28, -8, 12, 30]):
            w = 16 if i < 3 else 13
            arcade.draw_rect_filled(arcade.rect.XYWH(cx + bx, cy - 52, w, 18), (30, 30, 5))
            arcade.draw_rect_outline(arcade.rect.XYWH(cx + bx, cy - 52, w, 18), (100, 100, 18), 1)
        arcade.draw_text("3S LIPO", cx, cy - 52, (160, 160, 25), 7,
                         anchor_x="center", anchor_y="center",
                         font_name="monospace")

        # antenna
        arcade.draw_line(cx + 16, cy + 65, cx + 30, cy + 86, (110, 110, 110), 2)
        arcade.draw_circle_filled(cx + 30, cy + 86, 5, (190, 50, 50))


if __name__ == "__main__":
    Render()
    try:
        arcade.run()
    except KeyboardInterrupt:
        pass

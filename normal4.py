import arcade
from math import sin, cos, pi

class Drone(arcade.Window):
    def __init__(self):
        super().__init__(1920, 1080, "Drone")
        arcade.set_background_color(arcade.color.WHITE)
        self.progress = 0
        
    def on_update(self, delta_time):
        self.progress += delta_time
    
    def on_draw(self):
        self.clear()
        cx = self.width / 2
        cy = self.height / 2
        
        # Rotating propellers
        prop_angle = self.progress * 600
        
        # 4 arms at 45° angles
        arm_length = 100
        for i in range(4):
            angle = (i * 90 + 45) * pi / 180
            
            # Arm end position
            arm_x = cx + cos(angle) * arm_length
            arm_y = cy + sin(angle) * arm_length
            
            # Draw arm
            arcade.draw_line(cx, cy, arm_x, arm_y, (0, 0, 0), 5)
            
            # Draw propeller (2 rotating blades)
            prop_size = 40
            for blade in range(2):
                blade_angle = (prop_angle + blade * 180) * pi / 180
                bx1 = arm_x + cos(blade_angle) * prop_size
                by1 = arm_y + sin(blade_angle) * prop_size
                bx2 = arm_x - cos(blade_angle) * prop_size
                by2 = arm_y - sin(blade_angle) * prop_size
                arcade.draw_line(bx1, by1, bx2, by2, (100, 100, 100), 4)
            
            # Motor
            arcade.draw_circle_filled(arm_x, arm_y, 8, (50, 50, 50))
        
        # Central body
        arcade.draw_circle_filled(cx, cy, 20, (0, 0, 0))
        arcade.draw_circle_filled(cx, cy, 8, (200, 200, 200))

try:
    app = Drone()
    arcade.run()
except KeyboardInterrupt:
    print("Exiting")
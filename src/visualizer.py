import arcade

COLORS_DICT = {
    # "darkred": arcade.color.DARK_RED,
    "rainbow": arcade.color.DIAMOND,
}
class Renderer(arcade.Window):
    def __init__(self, parser, connections):
        super().__init__(1280, 720, parser.map_path)
        self.parser = parser
        self.connections = connections
        cors = [cor.coordinates for cor in self.parser.zones.values()]
        self.avg_x = sum(cor[0] for cor in cors) / len(cors)
        self.avg_y = sum(cor[1] for cor in cors) / len(cors)
        self.drag_x = 0
        self.drag_y = 0
        self.timer = 0
    
    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        self.drag_x += dx
        self.drag_y += dy

    def on_draw(self):
        self.clear()
        cx = (self.width / 2) + self.drag_x
        cy = (self.height / 2) + self.drag_y
        
        #drawing connection lines
        for con in self.connections:
            x1, y1 = self.parser.zones[con.connection[0]].coordinates 
            x2, y2 = self.parser.zones[con.connection[1]].coordinates
            x1 = cx + (x1 - self.avg_x) * 150
            y1 = cy + (y1 - self.avg_y) * 150
            x2 = cx + (x2 - self.avg_x) * 150
            y2 = cy + (y2 - self.avg_y) * 150
            arcade.draw_line(x1, y1, x2, y2, arcade.color.WHITE, 3)
        
        #drawing zones
        for name, zone in self.parser.zones.items():
            
            if zone.color:
                try:
                    color = getattr(arcade.color, zone.color.upper())
                except Exception:
                    if 'dark' in zone.color.lower():
                        color = "DARK" + "_" + zone.color[4:].upper()
                    try:
                        color = getattr(arcade.color, color.upper())
                    except Exception:
                        try:
                            color = COLORS_DICT[zone.color]
                        except KeyError:
                            raise ValueError(f'The color "{zone.color}" is not in the color list.')
            else:
                color = arcade.color.LIGHT_BLUE
            x, y = zone.coordinates
            arcade.draw_circle_filled(cx + (x - self.avg_x) * 150,
                                      cy + (y - self.avg_y) * 150,
                                      15, color)
            arcade.draw_text(name, cx + (x - self.avg_x) * 150,
                             cy + 30 + (y - self.avg_y) * 150,
                             arcade.color.WHITE, 12, anchor_x="center")
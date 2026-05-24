import arcade


COLORS_DICT = {
    "green": arcade.color.AO,
    "blue": arcade.color.CAPRI,
    "red": arcade.color.CRIMSON,
    "cyan": arcade.color.CYAN,
    "yellow": arcade.color.GOLD,
    "orange": arcade.color.DARK_ORANGE,
    "white": arcade.color.WHITE,
    "black": arcade.color.BLACK,
    "brown": arcade.color.BROWN,
    "darkred": arcade.color.DARK_RED,
    "gold": arcade.color.GOLDENROD,
    "lime": arcade.color.LIME_GREEN,
    "magenta": arcade.color.MAGENTA,
    "maroon": arcade.color.MAROON,
    "purple": arcade.color.ELECTRIC_PURPLE,
    "violet": arcade.color.VIOLET,
    "crimson": arcade.color.CRIMSON,
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

    def on_draw(self):
        self.clear()
        cx = self.width / 2
        cy = self.height / 2
        
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
            x, y = zone.coordinates
            arcade.draw_circle_filled(cx + (x - self.avg_x) * 150,
                                      cy + (y - self.avg_y) * 150,
                                      15,
                                      COLORS_DICT[zone.color])
            arcade.draw_text(name, cx + (x - self.avg_x) * 150,
                             cy + 30 + (y - self.avg_y) * 150,
                             arcade.color.WHITE, 12, anchor_x="center")
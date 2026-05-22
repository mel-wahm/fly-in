import arcade

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
        for con in self.connections:
            
        for name, zone in self.parser.zones.items():
            x, y = zone.coordinates
            color = getattr(arcade.color, zone.color.upper())
            arcade.draw_circle_filled(cx + (x - self.avg_x) * 150,
                                      cy + (y - self.avg_y) * 150,
                                      15,
                                      color)
            arcade.draw_text(name, cx + (x - self.avg_x) * 150,
                             cy + 30 + (y - self.avg_y) * 150,
                             arcade.color.WHITE, 12, anchor_x="center")
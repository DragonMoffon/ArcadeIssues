import arcade

from background import Background, ParallaxBackgroundGroup

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700  # arcade.get_display_size()


class BackgroundWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "background test", resizable=True)
        self.background_color = (5, 44, 70)
        self.far_background = Background.from_file(":resources:images/cybercity_background/far-buildings.png",
                                                   (0.0, 240.0), (SCREEN_WIDTH, 576), scale=3)
        self.mid_background = Background.from_file(":resources:images/cybercity_background/back-buildings.png",
                                                   (0.0, 120.0), (SCREEN_WIDTH, 576), scale=3)
        self.background = Background.from_file(":resources:images/cybercity_background/foreground.png",
                                               (0.0, 0.0), (SCREEN_WIDTH, 576), scale=3)

        self.group = ParallaxBackgroundGroup()
        self.group.extend([self.far_background, self.mid_background, self.background], [3, 2, 1])

        self.x_speed = 0
        self.view_x = 0

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()
        elif symbol == arcade.key.D:
            self.x_speed += 1
        elif symbol == arcade.key.A:
            self.x_speed -= 1

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.D:
            self.x_speed -= 1
        elif symbol == arcade.key.A:
            self.x_speed += 1

    def on_update(self, delta_time: float):
        if self.x_speed:
            self.view_x += self.x_speed * 60 * delta_time
            arcade.set_viewport(self.view_x, self.view_x + self.ctx.viewport[2],
                                0, self.ctx.viewport[3])

            self.group.pos = (self.view_x, 0)
            self.group.offset = (self.group.offset[0]+self.x_speed, self.group.offset[1])

    def on_draw(self):
        self.clear()
        self.group.draw()

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        size = self.far_background.size
        self.far_background.size = width, size[1]

        size = self.mid_background.size
        self.mid_background.size = width, size[1]

        size = self.background.size
        self.background.size = width, size[1]


def main():
    window = BackgroundWindow()
    window.run()


if __name__ == '__main__':
    main()

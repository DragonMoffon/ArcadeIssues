import arcade

import background

SCREEN_WIDTH, SCREEN_HEIGHT = 700, 700


class BackgroundWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "background test", resizable=True)
        self.background = background.Background.from_file(":resources:images/cybercity_background/far-buildings.png",
                                                          depth=4.0, scale=3, offset=(0.0, -960.0))
        self.background.add_from_file(":resources:images/cybercity_background/back-buildings.png",
                                      depth=2.0, scale=3, offset=(0.0, -240.0))
        self.background.add_from_file(":resources:images/cybercity_background/foreground.png", depth=1.0, scale=3)

    def on_draw(self):
        # self.clear()
        self.background.render()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.background._offset = (x - SCREEN_WIDTH // 2, 0.0)

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.background.view_port = (width, height)
        self.use()


def main():
    window = BackgroundWindow()
    window.run()


if __name__ == '__main__':
    main()

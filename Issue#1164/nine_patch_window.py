import arcade


import nine_patch


class TestWindow(arcade.Window):

    def __init__(self):
        super().__init__(1000, 1000)
        self.testy = nine_patch.NinePatch(400, 300, 80, 120, 1)
        self.testy2 = nine_patch.NinePatchShader(arcade.load_texture("grey_panel.png"), 10, 10, 900, 900,
                                                 (30, 30), (70, 70))

    def on_draw(self):
        self.clear()
        self.testy2.draw()

    # def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
    #     self.testy.on_click(x, y)

    # def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
    #     self.testy.on_release()

    # def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
    #     self.testy.drag(dx, dy)


if __name__ == '__main__':
    window = TestWindow()
    window.run()

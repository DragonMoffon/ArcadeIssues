import arcade


import nine_patch


class TestWindow(arcade.Window):

    def __init__(self):
        super().__init__()
        self.testy = nine_patch.NinePatch(400, 300, 80, 120, 1)

    def on_draw(self):
        self.clear()
        self.testy.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.testy.on_click(x, y)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.testy.on_release()

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self.testy.drag(dx, dy)


if __name__ == '__main__':
    window = TestWindow()
    window.run()

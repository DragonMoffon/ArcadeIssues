import arcade


import nine_patch


class TestWindow(arcade.Window):

    def __init__(self):
        super().__init__()
        self.testy = nine_patch.NinePatch(400, 300, 80, 120, 1.0)

    def on_draw(self):
        self.clear()
        self.testy.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print("pressed")

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        print("dragged")
        self.testy.drag(x, y, dx, dy)


if __name__ == '__main__':
    window = TestWindow()
    window.run()

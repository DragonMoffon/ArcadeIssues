import arcade
import solution_one
import solution_two

from arcade.experimental.profiling import Profiler


class TestWindow(arcade.Window):

    def __init__(self):
        super().__init__(title="rotation sprite comparison")
        self.frame_count = 0
        self.profiler = Profiler()

        self.point = (120, 100)

        self.sprite_1 = solution_one.RotatorSprite(center_x=120, center_y=50)
        self.sprite_2 = solution_two.RotatorSprite(30, self.point, center_x=120, center_y=50)

    def on_update(self, delta_time: float):
        with self.profiler.enabled():
            self.sprite_1.rotate_around(self.point, 30*delta_time)
            self.sprite_2.update_rotation(delta_time)

        self.frame_count = (self.frame_count + 1) % 50
        if not self.frame_count:
            self.profiler.print_stats()


if __name__ == '__main__':
    window = TestWindow()
    window.run()

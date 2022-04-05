"""
Solution Two is to implement rotate_sprite as a static method/Separate from the sprite class, but offer a subclass of
sprite which has a rotation_animation method.

I prefer this method as it, one, lets all sprites rotate around a point and, two, still gives people who want an
animated rotating sprite what they want. (spinning fire thing from mario)
"""
import arcade
from arcade import Texture


def rotate_sprite_around_point(sprite, point, degrees, update_sprite_angle):
    """
            Rotate the sprite around a given point by a number of degrees.

            :param point: the point to rotate around
            :param degrees: how many degrees to rotate by
            :param update_sprite_angle: Update the rotation
            """
    if update_sprite_angle:
        sprite.angle += degrees

    sprite.position = arcade.rotate_point(
        sprite.center_x, sprite.center_y,
        point[0], point[1],
        degrees)


class RotatorSprite(arcade.Sprite):

    def __init__(self, angle_speed: float = 360,
                 point: tuple[float, float] = (0.0, 0.0),
                 update_angle: bool = True,
                 filename: str = None,
                 scale: float = 1,
                 image_x: float = 0,
                 image_y: float = 0,
                 image_width: float = 0,
                 image_height: float = 0,
                 center_x: float = 0,
                 center_y: float = 0,
                 repeat_count_x: int = 1,  # Unused
                 repeat_count_y: int = 1,  # Unused
                 flipped_horizontally: bool = False,
                 flipped_vertically: bool = False,
                 flipped_diagonally: bool = False,
                 hit_box_algorithm: str = "Simple",
                 hit_box_detail: float = 4.5,
                 texture: Texture = None,
                 angle: float = 0,):
        super().__init__(
                        filename,
                        scale,
                        image_x,
                        image_y,
                        image_width,
                        image_height,
                        center_x,
                        center_y,
                        repeat_count_x,  # Unused
                        repeat_count_y,  # Unused
                        flipped_horizontally,
                        flipped_vertically,
                        flipped_diagonally,
                        hit_box_algorithm,
                        hit_box_detail,
                        texture,
                        angle)
        self.rotate_point = point
        self.rotation_speed = angle_speed
        self.update_angle = update_angle

    def update_rotation(self, delta_time):
        rotate_sprite_around_point(self, self.rotate_point, self.rotation_speed*delta_time, self.update_angle)
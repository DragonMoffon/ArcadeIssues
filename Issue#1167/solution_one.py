"""
Solution One is to implement this as a subclass of sprite. As referenced in Issue #1167

My problem with this issue is that it, one, adds more to an already crowded sprite class and, two, it means that normal
sprites can't get rotated.
"""
import arcade


class RotatorSprite(arcade.Sprite):

    def rotate_around(self, point: arcade.Point, degrees: float, update_sprite_angle: bool = True):
        """
        Rotate the sprite around a given point by a number of degrees.

        :param point: the point to rotate around
        :param degrees: how many degrees to rotate by
        :param update_sprite_angle: Update the rotation
        """

        if update_sprite_angle:
            self.angle += degrees

        self.position = arcade.rotate_point(
            self.center_x, self.center_y,
            point[0], point[1],
            degrees)

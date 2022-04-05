import arcade
import math


def rotate_sprite_around_point(target_sprite: arcade.Sprite, target_point: tuple[float, float],
                               angle: float, change_sprite_angle: bool = True):
    """
    Rotates a passed in sprite around a point by a set angle.

    :param target_sprite: The sprite to rotate
    :param target_point: The point to rotate around
    :param angle: The angle (in degrees) to rotate by
    :param change_sprite_angle: Whether the sprite should rotate itself.
    """

    if change_sprite_angle:
        target_sprite.angle += angle

    rad = math.radians(angle)
    c, s = math.cos(rad), math.sin(rad)

    rel_x = target_sprite.center_x - target_point[0]
    rel_y = target_sprite.center_y - target_point[1]

    rel_x, rel_y = c * rel_x - s * rel_y, s * rel_x + c * rel_y

    target_sprite.center_x = round(rel_x + target_point[0], 2)
    target_sprite.center_y = round(rel_y + target_point[1], 2)


if __name__ == '__main__':
    example = arcade.SpriteCircle(5, arcade.color.RADICAL_RED)
    example.center_x, example.center_y = 5.0, 0.0
    print(example.center_x, example.center_y)
    rotate_sprite_around_point(example, (0.0, 0.0), 90)
    print(example.center_x, example.center_y)

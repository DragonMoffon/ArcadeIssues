"""
Having outlined two different methods of implementing rotate_sprite. The next step is to figure out which method of
rotating around a point is best.
"""
import math
from arcade.experimental.profiling import Profiler


def current_method(x: float, y: float, cx: float, cy: float,
                   angle_degrees: float) -> list[float]:
    """
    The current method relies on a rotation matrix and shifting the frame of reference.
    """
    # translate frame of reference
    temp_x = x - cx
    temp_y = y - cy

    # now apply rotation
    angle_radians = math.radians(angle_degrees)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    rotated_x = temp_x * cos_angle - temp_y * sin_angle
    rotated_y = temp_x * sin_angle + temp_y * cos_angle

    # translate back
    rounding_precision = 2
    x = round(rotated_x + cx, rounding_precision)
    y = round(rotated_y + cy, rounding_precision)

    return [x, y]


def current_method_cleaned(x: float, y: float, cx: float, cy: float,
                           angle_degrees: float) -> list[float]:
    """
    It's the same it is just shortened. Maybe it'll be faster, but probably not.
    """
    # translate frame of reference
    temp_x = x - cx
    temp_y = y - cy

    # now apply rotation
    angle_radians = math.radians(angle_degrees)
    cos_angle, sin_angle = math.cos(angle_radians), math.sin(angle_radians)
    rotated_x, rotated_y = temp_x * cos_angle - temp_y * sin_angle, temp_x * sin_angle + temp_y * cos_angle

    # translate back
    rounding_precision = 2

    return [round(rotated_x + cx, rounding_precision), round(rotated_y + cy, rounding_precision)]


def atan2_method(x: float, y: float, cx: float, cy: float,
                 angle_degrees: float) -> list[float]:
    """
    Is the equivalent of converting a vector to polar coordinates and rotating.
    """

    rad_angle = math.radians(angle_degrees)
    diff_x, diff_y = x - cx, y - cy
    length, new_angle = math.sqrt(diff_x**2 + diff_y**2), math.atan2(diff_y, diff_x) + rad_angle

    rounding_precision = 2

    return [round(cx + math.cos(new_angle)*length, rounding_precision),
            round(cy + math.sin(new_angle)*length, rounding_precision)]


if __name__ == '__main__':
    profiler = Profiler()
    start_pos = [15, 12]
    rotate_point = [10, 15]

    pos_1 = start_pos.copy()
    pos_2 = start_pos.copy()
    pos_3 = start_pos.copy()
    angle_change = 36

    with profiler.enabled():
        for _ in range(10000):
            pos_1 = current_method(*pos_1, *rotate_point, angle_change)
            pos_2 = current_method_cleaned(*pos_2, *rotate_point, angle_change)
            pos_3 = atan2_method(*pos_3, *rotate_point, angle_change)
        profiler.print_stats()

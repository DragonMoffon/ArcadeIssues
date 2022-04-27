import arcade


class NinePatch:
    """
    Using nine sprites allows for a resizable ui element whose corners do not get distorted
    when changing the width and height.

    The width and height defines the size of the inside area and does not include the border or corners.

    TODO: Add changeable sprites for corners, edges, and center. Add size jump and texture repeat.
    """

    def __init__(self, center_x, center_y, width, height, scale, color=arcade.color.WHITE):
        self._width = 0
        self._height = 0
        self._size = 32 * scale

        h_w, h_h, h_s = width / 2, height / 2, 16 * scale

        self._t_r = arcade.Sprite("Corner.png", angle=270, scale=scale)
        self._b_r = arcade.Sprite("Corner.png", angle=180, scale=scale)
        self._b_l = arcade.Sprite("Corner.png", angle=90, scale=scale)
        self._t_l = arcade.Sprite("Corner.png", scale=scale)

        self._t = arcade.Sprite("Center.png", scale=scale)
        self._l = arcade.Sprite("Center.png", scale=scale)
        self._b = arcade.Sprite("Center.png", scale=scale)
        self._r = arcade.Sprite("Center.png", scale=scale)

        self._body = arcade.Sprite("Center.png", center_x=center_x, center_y=center_y, scale=scale)
        self._body.width = width
        self._body.height = height

        self.size = width, height

        self._renderer = arcade.SpriteList()
        self._renderer.extend([self._t_r, self._t_l, self._b_r, self._b_l,
                              self._t, self._l, self._b, self._r, self._body])
        self._renderer.color = color
        
    def _pos_x(self, center_x, h_w, h_s):
        self._body.center_x = center_x

        self._t_r.center_x = center_x + h_w + h_s
        self._b_r.center_x = center_x + h_w + h_s
        self._b_l.center_x = center_x - h_w - h_s
        self._t_l.center_x = center_x - h_w - h_s

        self._t.center_x = center_x
        self._b.center_x = center_x
        self._l.center_x = center_x - h_w - h_s
        self._r.center_x = center_x + h_w + h_s
        
    def _pos_y(self, center_y, h_h, h_s):
        self._body.center_y = center_y

        self._t_r.center_y = center_y + h_h + h_s
        self._b_r.center_y = center_y + h_h + h_s
        self._b_l.center_y = center_y - h_h - h_s
        self._t_l.center_y = center_y - h_h - h_s

        self._t.center_y = center_y + h_h + h_s
        self._b.center_y = center_y - h_h - h_s
        self._l.center_y = center_y
        self._r.center_y = center_y

    def _pos(self, center_x, center_y, h_w, h_h, h_s):
        self._body.position = center_x, center_y

        self._t_r.position = center_x + h_w + h_s, center_y + h_h + h_s
        self._b_r.position = center_x + h_w + h_s, center_y - h_h - h_s
        self._b_l.position = center_x - h_w - h_s, center_y - h_h - h_s
        self._t_l.position = center_x - h_w - h_s, center_y + h_h + h_s

        self._t.position = center_x, center_y + h_h + h_s
        self._b.position = center_x, center_y - h_h - h_s
        self._l.position = center_x - h_w - h_s, center_y
        self._r.position = center_x + h_w + h_s, center_y

    def _shift(self, d_x, d_y, d_w, d_h):
        pos = self._body.position

        self._body.position = pos[0] + d_x / 2, pos[1] + d_y / 2
        self.size = (self._width + d_h, self._height + d_w)

    def draw(self):
        self._renderer.draw(pixelated=True)

    @property
    def center_x(self):
        return self._body.center_x

    @property
    def center_y(self):
        return self._body.center_y

    @center_x.setter
    def center_x(self, value):
        h_w, h_s = self._width / 2, self._size / 2

        self._pos_x(value, h_w, h_s)

    @center_y.setter
    def center_y(self, value):
        h_h, h_s = self._height / 2, self._size / 2

        self._pos_y(value, h_h, h_s)

    @property
    def pos(self):
        return self.center_x, self.center_y

    @pos.setter
    def pos(self, value: tuple[float, float]):
        self._pos(value[0], value[1], self.width / 2, self.height / 2, self._size / 2)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value < 1:
            raise ValueError("The width was set to a number less than 1! don't do that.")
        self._width = value

        self._pos_x(self.center_x, value / 2, self._size / 2)
        self._body.width = value

        self._t.width = value
        self._b.width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value < 1:
            raise ValueError("The height was set to a number less than 1! don't do that.")
        self._height = value

        self._pos_y(self.center_y, value / 2, self._size / 2)
        self._body.height = value

        self._l.height = value
        self._r.height = value

    @property
    def size(self):
        return self._width, self._height

    @size.setter
    def size(self, value: tuple[int, int]):
        if value[0] < 1:
            raise ValueError("The width was set to a number less than 1! don't do that.")
        elif value[1] < 1:
            raise ValueError("The height was set to a number less than 1! don't do that.")
        elif value != (self._width, self._height):
            self._width = value[0]
            self._height = value[1]

            self._pos(self.center_x, self.center_y, value[0] / 2, value[1] / 2, self._size / 2)

            self._body.width = value[0]
            self._body.height = value[1]

            self._t.width = value[0]
            self._b.width = value[0]

            self._l.height = value[1]
            self._r.height = value[1]

    @property
    def top_right(self):
        return self._t_r.position

    @top_right.setter
    def top_right(self, value: tuple[float, float]):
        d_x = value[0] - self._t_r.center_x
        d_y = value[1] - self._t_r.center_y

        self._shift(d_x, d_y, d_x, d_y)

    @property
    def top_left(self):
        return self._t_l.position

    @top_left.setter
    def top_left(self, value: tuple[float, float]):
        d_x = value[0] - self._t_l.center_x
        d_y = value[1] - self._t_l.center_y

        self._shift(d_x, d_y, -d_x, d_y)

    @property
    def bottom_right(self):
        return self._b_r.position

    @bottom_right.setter
    def bottom_right(self, value: tuple[float, float]):
        d_x = value[0] - self._b_r.center_x
        d_y = value[1] - self._b_r.center_y

        self._shift(d_x, d_y, d_x, -d_y)

    @property
    def bottom_left(self):
        return self._b_l.position

    @bottom_left.setter
    def bottom_left(self, value: tuple[float, float]):
        d_x = value[0] - self._b_l.center_x
        d_y = value[1] - self._b_l.center_y

        self._shift(d_x, d_y, -d_x, -d_y)

    @property
    def top(self):
        return self._t.position

    @top.setter
    def top(self, value: float):
        d_y = value - self._t.center_y

        self._body.center_y += d_y / 2
        self.height = self._height + d_y

    @property
    def bottom(self):
        return self._b.position

    @bottom.setter
    def bottom(self, value: float):
        d_y = value - self._b.center_y

        self._body.center_y += d_y / 2
        self.height -= d_y

    @property
    def left(self):
        return self._l.position

    @left.setter
    def left(self, value: float):
        d_x = value - self._l.center_x

        self._body.center_x += d_x / 2
        self.width -= d_x

    @property
    def right(self):
        return self._r.position

    @right.setter
    def right(self, value: float):
        d_x = value - self._r.center_x

        self._body.center_x += d_x / 2
        self.height += d_x

    def drag(self, x, y, dx, dy):
        p = (x-dx, y-dy)
        h_h, h_w = self.width / 2, self.height / 2
        if (self.center_x - h_w - self._size <= p[0] <= self.center_x + h_w + self._size and
                self.center_y - h_h - self._size <= p[1] <= self.center_y + h_h + self._size):

            if self._t_l.collides_with_point(p):
                self.top_left = self._t_l.center_x + dx, self._t_l.center_y + dy
            elif self._t_r.collides_with_point(p):
                self.top_right = self._t_r.center_x + dx, self._t_r.center_y + dy
            elif self._b_l.collides_with_point(p):
                self.bottom_left = self._b_l.center_x + dx, self._b_l.center_y + dy
            elif self._b_r.collides_with_point(p):
                self.bottom_right = self._b_r.center_x + dx, self._b_r.center_y + dy
            elif self._t.collides_with_point(p):
                self.top = self._t.center_y + dy
            elif self._b.collides_with_point(p):
                self.bottom = self._b.center_y + dy
            elif self._l.collides_with_point(p):
                self.left = self._l.center_x + dx
            elif self._r.collides_with_point(p):
                self.right = self._r.center_x + dx
            else:
                self.pos = self.center_x + dx, self.center_y + dy

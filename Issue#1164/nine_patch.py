import arcade


class NinePatch:
    """
    Using nine sprites allows for a resizable ui element whose corners do not get distorted
    when changing the width and height.

    The width and height defines the size of the inside area and does not include the border or corners.

    TODO: Add changeable sprites for corners, edges, and center. Add size jump and texture repeat.
    """

    def __init__(self, x, y, width, height, scale, color=arcade.color.WHITE):
        self._size = 32 * scale

        self._t_r = arcade.Sprite("Corner.png", angle=270, scale=scale)
        self._b_r = arcade.Sprite("Corner.png", angle=180, scale=scale)
        self._b_l = arcade.Sprite("Corner.png", angle=90, scale=scale)
        self._t_l = arcade.Sprite("Corner.png", scale=scale)

        self._t = arcade.Sprite("Center.png", scale=scale)
        self._l = arcade.Sprite("Center.png", scale=scale)
        self._b = arcade.Sprite("Center.png", scale=scale)
        self._r = arcade.Sprite("Center.png", scale=scale)

        self._body = arcade.Sprite("Center.png", scale=scale)

        self._width = width
        self._height = height
        self._pos = (x, y)
        self._position_sprites(x, y, width, height)
        self._scale_sprites(width, height)

        self._renderer = arcade.SpriteList()
        self._renderer.extend([self._t_r, self._t_l, self._b_r, self._b_l,
                              self._t, self._l, self._b, self._r, self._body])
        self._renderer.color = color

        self.current_piece = None

    def draw(self):
        self._renderer.draw(pixelated=True)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def size(self):
        return self._width, self._height

    @size.setter
    def size(self, _size):
        self._width = _size[0]
        self._height = _size[1]
        self._position_sprites(*self._pos, *_size)
        self._scale_sprites(*_size)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, _pos):
        d_pos = self._pos[0] - _pos[0], self._pos[1] - _pos[1]
        self._pos = _pos
        self._renderer.move(*d_pos)

    def move(self, dx, dy):
        self._pos = self._pos[0] + dx, self._pos[1] + dy
        self._renderer.move(dx, dy)

    def _position_sprites(self, x, y, width, height):
        h_w, h_h, h_s = width / 2, height / 2, self._size / 2

        self._b_l.position = x + h_s, y + h_s
        self._b_r.position = x + width - h_s, y + h_s
        self._t_l.position = x + h_s, y + height - h_s
        self._t_r.position = x + width - h_s, y + height - h_s

        self._l.position = x + h_s, y + h_h
        self._r.position = x + width - h_s, y + h_h
        self._t.position = x + h_w, y + height - h_s
        self._b.position = x + h_w, y + h_s

        self._body.position = x + h_w, y + h_h

    def _scale_sprites(self, width, height):
        d_s = self._size * 2

        self._l.height = height - d_s
        self._r.height = height - d_s
        self._t.width = width - d_s
        self._b.width = width - d_s

        self._body.width = width - d_s
        self._body.height = height - d_s

    def on_click(self, x, y):
        p = (x, y)
        if self._body.collides_with_point(p):
            self.current_piece = self._body
        elif self._t_r.collides_with_point(p):
            self.current_piece = self._t_r
        elif self._t_l.collides_with_point(p):
            self.current_piece = self._t_l
        elif self._b_r.collides_with_point(p):
            self.current_piece = self._b_r
        elif self._b_l.collides_with_point(p):
            self.current_piece = self._b_l
        elif self._t.collides_with_point(p):
            self.current_piece = self._t
        elif self._b.collides_with_point(p):
            self.current_piece = self._b
        elif self._r.collides_with_point(p):
            self.current_piece = self._r
        elif self._l.collides_with_point(p):
            self.current_piece = self._l

    def on_release(self):
        self.current_piece = None

    def drag(self, dx, dy):
        if self.current_piece is self._body:
            self.move(dx, dy)
        elif self.current_piece is self._t_r:
            self.size = self._width + dx, self._height + dy
        elif self.current_piece is self._t_l:
            self.move(dx, 0)
            self.size = self._width - dx, self._height + dy
        elif self.current_piece is self._b_r:
            self.move(0, dy)
            self.size = self._width + dx, self._height - dy
        elif self.current_piece is self._b_l:
            self.move(dx, dy)
            self.size = self._width - dx, self._height - dy
        elif self.current_piece is self._t:
            self.size = self._width, self._height + dy
        elif self.current_piece is self._b:
            self.move(0, dy)
            self.size = self._width, self._height - dy
        elif self.current_piece is self._r:
            self.size = self._width + dx, self._height
        elif self.current_piece is self._l:
            self.move(dx, 0)
            self.size = self._width - dx, self._height



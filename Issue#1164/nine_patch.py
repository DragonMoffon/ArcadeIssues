import arcade
import arcade.gl as gl
from array import array


class NinePatch:
    """
    Using nine sprites allows for a resizable ui element whose corners do not get distorted
    when changing the width and height.

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
        self._width = 1 + self._size*2 if _size[0] < 1 + self._size*2 else _size[0]
        self._height = 1 + self._size*2 if _size[1] < 1 + self._size*2 else _size[1]
        self._position_sprites(*self._pos, self._width, self._height)
        self._scale_sprites(self._width, self._height)

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


class NinePatchShader:

    def __init__(self, texture: arcade.Texture, x, y, width, height, start, end, atlas: arcade.TextureAtlas = None):
        ctx = arcade.get_window().ctx

        # ModernGl components for render.
        self.program = ctx.load_program(vertex_shader="nine_patch_vert.glsl",
                                        fragment_shader="nine_patch_frag.glsl")
        try:
            self.program["uv_texture"] = 0
        except:
            pass

        try:
            self.program['sprite_texture'] = 1
        except:
            pass

        data = array('f', [0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0])
        self.geometry = ctx.geometry([gl.BufferDescription(ctx.buffer(data=data), '2f', ['in_uv'])],
                                     mode=ctx.TRIANGLE_STRIP)

        # Required references for the texture
        self._atlas: arcade.TextureAtlas = ctx.default_atlas if atlas is None else atlas
        self._atlas.texture.filter = ctx.NEAREST, ctx.NEAREST
        if not self._atlas.has_texture(texture):
            self._atlas.add(texture)
        self._texture: arcade.Texture = texture
        try:
            self.program['texture_id'] = self._atlas.get_texture_id(self._texture.name)
        except:
            pass

        # X, Y from bottom left.
        self._x = x
        self._y = y

        # size includes outer edge
        self._width = width
        self._height = height

        self.program['patch_data'] = x, y, width, height

        # pixel coordinate of start, and end
        self._start = start
        self._end = end

        # end pixel UV relative to opposite corner.
        self._end_diff = self._end[0] - texture.width, self._end[1] - texture.height

        # texture UV coordinate of start, and end.
        try:
            self.program["base_uv"] = (start[0] / texture.width, start[1] / texture.height,
                                       end[0] / texture.width, end[1] / texture.height)
        except:
            pass

        # rendered UV coordinate of start, and end.
        try:
            self.program["var_uv"] = (self._start[0] / width, self._start[1] / height,
                                      1 + self._end_diff[0] / width, 1 + self._end_diff[1] / height)
        except:
            pass

        print(self._atlas.get_region_info(texture.name).y, self._atlas.max_width, self._atlas.get_region_info(texture.name).texture_coordinates)

    def draw(self):
        self._atlas.use_uv_texture(0)
        self._atlas.texture.use(1)
        self.geometry.render(self.program)


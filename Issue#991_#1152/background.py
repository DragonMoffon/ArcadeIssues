from PIL import Image

import arcade
from arcade.resources import resolve_resource_path
import arcade.gl as gl
from pyglet.math import Mat3


class BackgroundTexture:

    def __init__(self, texture: gl.Texture,
                 offset: tuple[float, float] = (0.0, 0.0),
                 scale: float = 1.0, angle: float = 0.0):
        self.texture = texture

        self._scale = scale
        self._scale_transform = Mat3().scale(scale, scale)

        self._angle = angle
        self._angle_transform = Mat3().rotate(angle)

        self._offset = offset
        self._offset_transform = Mat3().translate(offset[0], offset[1])

    @property
    def pixel_transform(self):
        return self._offset_transform @ self._angle_transform @ self._scale_transform

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value
        self._scale_transform = Mat3().scale(value, value)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value: float):
        self._angle = value
        self._angle_transform = Mat3().rotate(value)

    @property
    def offset(self):
        return self._scale

    @offset.setter
    def offset(self, value: tuple[float, float]):
        self._offset = value
        self._offset_transform = Mat3().translate(-value[0], value[1])

    @property
    def wrap_x(self) -> int:
        """
        Get or set the horizontal wrapping of the texture. This decides how textures
        are read when texture coordinates are outside the ``[0.0, 1.0]`` area.
        Default value is ``REPEAT``.

        Valid options are::

            # Note: Enums can also be accessed in arcade.gl
            # Repeat pixels on the y axis
            texture.wrap_x = ctx.REPEAT
            # Repeat pixels on the y axis mirrored
            texture.wrap_x = ctx.MIRRORED_REPEAT
            # Repeat the edge pixels when reading outside the texture
            texture.wrap_x = ctx.CLAMP_TO_EDGE
            # Use the border color (black by default) when reading outside the texture
            texture.wrap_x = ctx.CLAMP_TO_BORDER

        :type: int
        """
        return self.texture.wrap_x

    @wrap_x.setter
    def wrap_x(self, value: int):
        self.texture.wrap_x = value

    @property
    def wrap_y(self) -> int:
        """
        Get or set the horizontal wrapping of the texture. This decides how textures
        are read when texture coordinates are outside the ``[0.0, 1.0]`` area.
        Default value is ``REPEAT``.

        Valid options are::

            # Note: Enums can also be accessed in arcade.gl
            # Repeat pixels on the x axis
            texture.wrap_x = ctx.REPEAT
            # Repeat pixels on the x axis mirrored
            texture.wrap_x = ctx.MIRRORED_REPEAT
            # Repeat the edge pixels when reading outside the texture
            texture.wrap_x = ctx.CLAMP_TO_EDGE
            # Use the border color (black by default) when reading outside the texture
            texture.wrap_x = ctx.CLAMP_TO_BORDER

        :type: int
        """
        return self.texture.wrap_y

    @wrap_y.setter
    def wrap_y(self, value: int):
        self.texture.wrap_y = value

    def use(self, unit: int = 0) -> None:
        """Bind the texture to a channel,

        :param int unit: The texture unit to bind the texture.
        """
        self.texture.use(unit)


class Background:

    def __init__(self,
                 texture: BackgroundTexture,
                 pos: tuple[float, float],
                 size: tuple[float, float],
                 shader: gl.Program = None,
                 geometry: gl.Geometry = None):

        if shader is None:
            shader = arcade.get_window().ctx.load_program(vertex_shader="vertex_geometry.glsl",
                                                          fragment_shader="background_frag.glsl")
        self.shader = shader

        if geometry is None:
            geometry = gl.geometry.quad_2d(pos=(0.5, 0.5))
        self.geometry = geometry

        self.texture = texture

        self._pos = pos
        try:
            self.shader['pos'] = pos
        except KeyError:
            pass

        self._size = size
        try:
            self.shader['size'] = size
        except KeyError:
            pass

    @staticmethod
    def from_file(tex_src: str,
                  pos: tuple[float, float] = (0.0, 0.0),
                  size: tuple[int, int] = None,
                  offset: tuple[float, float] = (0.0, 0.0),
                  scale: float = 1.0,
                  angle: float = 0.0,
                  *,
                  filters=(gl.NEAREST, gl.NEAREST),
                  shader: gl.Program = None,
                  geometry: gl.Geometry = None):
        _context = arcade.get_window().ctx

        with Image.open(resolve_resource_path(tex_src)).convert("RGBA") as img:
            texture = _context.texture(img.size, data=img.transpose(Image.FLIP_TOP_BOTTOM).tobytes(),
                                       filter=filters)
            if size is None:
                size = texture.size

        background_texture = BackgroundTexture(texture, offset, scale, angle)
        return Background(background_texture, pos, size, shader, geometry)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: tuple[float, float]):
        self._pos = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value
        self.shader['size'] = value

    def draw(self, shift=(0, 0)):
        self.shader['pixelTransform'] = self.texture.pixel_transform
        self.shader['pos'] = self.pos[0]+shift[0], self.pos[1]+shift[1]
        self.texture.use(0)

        self.geometry.render(self.shader)

    @property
    def blend(self):
        try:
            return self.shader['blend']
        except KeyError:
            return 1

    @blend.setter
    def blend(self, value):
        try:
            self.shader['blend'] = value
        except KeyError:
            pass

    def blend_layer(self, other, percent):
        self.shader['blend'] = 1 - percent
        other.shader['blend'] = percent


class BackgroundGroup:

    def __init__(self):
        self.backgrounds: list[Background] = []

        self._pos = [0, 0]
        self._offset = [0, 0]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        for background in self.backgrounds:
            background.texture.offset = value

    def add(self, item: Background):
        if item not in self.backgrounds:
            self.backgrounds.append(item)
        else:
            print("WARNING: Background already in group")

    def extend(self, items: list[Background]):
        for item in items:
            self.add(item)

    def draw(self):
        for background in self.backgrounds:
            background.draw(self.pos)


class ParallaxBackgroundGroup:

    def __init__(self, backgrounds: list[Background] = None, depths: list[float] = None):
        self.backgrounds: list[Background] = [] if backgrounds is None else backgrounds
        self.depths: list[float] = [] if depths is None else backgrounds

        if len(self.backgrounds) != len(self.depths):
            raise ValueError("The number of backgrounds does not equal the number of depth values")

        self._pos = [0, 0]
        self._offset = [0, 0]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        for index, background in enumerate(self.backgrounds):
            depth = self.depths[index]
            background.texture.offset = value[0] / depth, value[1] / depth

    def add(self, item: Background, depth: float = 1.0):
        if item not in self.backgrounds:
            self.backgrounds.append(item)
            self.depths.append(depth)
        else:
            print("WARNING: Background already in group")

    def remove(self, item: Background):
        index = self.backgrounds.index(item)
        self.backgrounds.remove(item)
        self.depths.pop(index)

    def change_depth(self, item: Background, new_depth: float):
        self.depths[self.backgrounds.index(item)] = new_depth

    def extend(self, items: list[Background], depths: list[float]):
        for index, item in enumerate(items):
            self.add(item, depths[index])

    def draw(self):
        for background in self.backgrounds:
            background.draw(self.pos)







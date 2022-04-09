from PIL import Image
from math import radians, sin, cos

import arcade
from arcade.resources import resolve_resource_path
import arcade.gl as gl


class BackgroundLayer:
    DefaultGeo: gl.Geometry = None

    def __init__(self,
                 texture: gl.Texture,
                 shader: gl.Program,
                 size: tuple[float, float],
                 depth: float = 1.0,  scale: float = 1.0,
                 offset: tuple[float, float] = (0.0, 0.0)):
        if BackgroundLayer.DefaultGeo is None:
            _context = arcade.get_window().ctx
            BackgroundLayer.DefaultGeo = gl.geometry.quad_2d_fs()

        self.texture: gl.Texture = texture
        self.shader: gl.Program = shader

        self._size = size
        self.shader['size'] = size

        self._depth = depth
        self.shader['depth'] = depth

        self._offset = offset
        self.shader['offset'] = offset

        self._scale = scale
        self.shader['scale'] = scale

        self._angle = 0.0
        self.shader['rot'] = 1.0, 0.0

    @staticmethod
    def from_file(tex_src: str,
                  depth: float = 1.0,
                  scale: float = 1.0,
                  offset: tuple[float, float] = (0.0, 0.0),
                  size: tuple[float, float] = None,
                  *,
                  shader_src: tuple[str, str] = ("vertex.glsl", "background_frag.glsl"),
                  filters: tuple[int, int] = (gl.NEAREST, gl.NEAREST)):

        _context = arcade.get_window().ctx

        with Image.open(resolve_resource_path(tex_src)).convert("RGBA") as img:
            texture = _context.texture(img.size, data=img.transpose(Image.FLIP_TOP_BOTTOM).tobytes(),
                                       filter=filters)
            if size is None:
                size = (0, texture.height)

        shader = _context.load_program(vertex_shader=shader_src[0], fragment_shader=shader_src[1])
        return BackgroundLayer(texture, shader, size, depth, scale, offset)

    def draw(self, offset: tuple[int, int] = (0.0, 0.0), transparency: float = 1.0, geometry: gl.geometry = None):
        self.shader['blend'] = transparency
        self.shader['offset'] = offset[0] - self.offset[0], offset[1] - self.offset[1]
        self.texture.use(0)

        if geometry is None:
            BackgroundLayer.DefaultGeo.render(self.shader)
        else:
            geometry.render(self.shader)

    @property
    def depth(self):
        return self._depth

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value: tuple[int, int]):
        self._offset = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value
        self.shader['scale'] = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value: float):
        self._angle = value
        self.shader['rot'] = cos(radians(value)), sin(radians(value))


class Background:

    def __init__(self, context: arcade.ArcadeContext, view_port_size: tuple[int, int]):
        self.context = context

        self._view_port = view_port_size

        self._offset = 0, 0

        self.layers: list[BackgroundLayer] = []

    def add(self, layer: BackgroundLayer):
        layer.shader['screenResolution'] = self._view_port
        if not len(self.layers) or layer.depth <= self.layers[-1].depth:
            self.layers.append(layer)
        elif layer.depth > self.layers[0].depth:
            self.layers.insert(0, layer)
        else:
            for i in range(len(self.layers[1:])):
                if layer.depth > self.layers[i+1].depth:
                    self.layers.insert(i+1, layer)
                    break

    @property
    def view_port(self):
        return self._view_port

    @view_port.setter
    def view_port(self, value: tuple[int, int]):
        self._view_port = value
        for layer in self.layers:
            layer.shader['screenResolution'] = value

    @staticmethod
    def from_file(tex_src: str,
                  depth: float = 1.0,
                  scale: float = 1.0,
                  offset: tuple[float, float] = (0.0, 0.0),
                  size: tuple[float, float] = None,
                  *,
                  filters: tuple[int, int] = (gl.NEAREST, gl.NEAREST)):

        layer = BackgroundLayer.from_file(tex_src, depth, scale, offset, size, filters=filters)
        _context = arcade.get_window().ctx
        background = Background(_context, _context.viewport[2:])
        background.add(layer)
        return background

    def add_from_file(self,
                      tex_src: str,
                      depth: float = 1.0,
                      scale: float = 1.0,
                      offset: tuple[float, float] = (0.0, 0.0),
                      size: tuple[float, float] = None,
                      *,
                      shader_src: tuple[str, str] = ("vertex.glsl", "background_frag.glsl"),
                      filters: tuple[int, int] = (gl.NEAREST, gl.NEAREST)):
        layer = BackgroundLayer.from_file(tex_src, depth, scale, offset, size,
                                          shader_src=shader_src, filters=filters)
        self.add(layer)
        return layer

    def render(self):
        for layer in self.layers:
            layer.draw(self._offset)





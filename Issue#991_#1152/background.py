from PIL import Image

import arcade
from arcade.resources import resolve_resource_path
import arcade.gl as gl
import pyglet.gl as py_gl


class BackgroundLayer:

    def __init__(self, texture: gl.Texture, shader: gl.Program, depth: float = 1.0,  scale: float = 1.0,
                 offset: tuple[float, float] = (0.0, 0.0)):
        self.texture: gl.Texture = texture
        self.shader: gl.Program = shader

        self.depth = depth
        self.shader['depth'] = depth

        self.offset = offset
        self.shader['offset'] = offset

        self.scale = scale
        self.shader['scale'] = scale

    @staticmethod
    def from_file(tex_src: str, depth: float = 1.0, scale: float = 1.0, offset: tuple[float, float] = (0.0, 0.0), *,
                  shader_src: tuple[str, str] = ("vertex.glsl", "background_frag.glsl"),
                  repeat_y: bool = False, filters: tuple[int, int] = (gl.NEAREST, gl.NEAREST)):
        _context = arcade.get_window().ctx
        with Image.open(resolve_resource_path(tex_src)).convert("RGBA") as img:
            wrap_y = gl.CLAMP_TO_EDGE if not repeat_y else gl.REPEAT
            texture = _context.texture(img.size, data=img.transpose(Image.FLIP_TOP_BOTTOM).tobytes(),
                                       filter=filters, wrap_x=gl.REPEAT, wrap_y=wrap_y)
        shader = _context.load_program(vertex_shader=shader_src[0], fragment_shader=shader_src[1])
        return BackgroundLayer(texture, shader, depth, scale, offset)


class Background:
    geometry: gl.Geometry = None
    shader: gl.Program = None

    def __init__(self, context: arcade.ArcadeContext, view_port_size: tuple[int, int],
                 color=arcade.color.BLACK, target: gl.framebuffer = None):
        if Background.geometry is None:
            Background.geometry = gl.geometry.quad_2d_fs()
            Background.shader = context.load_program(vertex_shader="vertex.glsl", fragment_shader="fragment.glsl")

        self.color = color
        self.context = context

        if target is None:
            target = context.screen
        self.target = target

        self._view_port = view_port_size

        self._fbo = context.framebuffer(color_attachments=[context.texture(view_port_size)])

        self._offset = [0, 0]
        self._blend = 0.0

        self.layers: list[BackgroundLayer] = []

    def add(self, layer: BackgroundLayer):
        layer.shader['screenResolution'] = self._view_port
        if not len(self.layers) or layer.depth < self.layers[-1].depth:
            self.layers.append(layer)
        elif layer.depth > self.layers[0].depth:
            self.layers.insert(0, layer)
        else:
            for i in range(len(self.layers[1:])):
                if layer.depth > self.layers[i+1].depth:
                    self.layers.insert(i+1, layer)
                    break
        print("")

    @property
    def view_port(self):
        return self._view_port

    @view_port.setter
    def view_port(self, value: tuple[int, int]):
        self._view_port = value
        self._fbo.color_attachments[0].resize(value)
        self._fbo.resize()
        for layer in self.layers:
            layer.shader['screenResolution'] = value

    @staticmethod
    def from_file(tex_src: str, depth: float = 1.0, scale: float = 1.0, offset: tuple[float, float] = (0.0, 0.0),
                  color=arcade.color.BLACK, *, target=None, repeat_y: bool = False,
                  filters: tuple[int, int] = (gl.NEAREST, gl.NEAREST)):

        layer = BackgroundLayer.from_file(tex_src, depth, scale, offset, repeat_y=repeat_y, filters=filters)
        _context = arcade.get_window().ctx
        background = Background(_context, _context.viewport[2:], color, target)
        background.add(layer)
        return background

    def add_from_file(self, tex_src: str, depth: float = 1.0,  scale: float = 1.0,
                      offset: tuple[float, float] = (0.0, 0.0), *,
                      shader_src: tuple[str, str] = ("vertex.glsl", "background_frag.glsl"), repeat_y: bool = False,
                      filters: tuple[int, int] = (gl.NEAREST, gl.NEAREST)):
        layer = BackgroundLayer.from_file(tex_src, depth, scale, offset,
                                          shader_src=shader_src, repeat_y=repeat_y, filters=filters)
        self.add(layer)
        return layer

    def render(self):
        with self.target.activate() as fbo:
            fbo.clear(self.color)
            for layer in self.layers:
                layer.shader['offset'] = self._offset[0] + layer.offset[0], self._offset[1] + layer.offset[1]
                layer.shader['blend'] = self._blend
                layer.texture.use(0)

                Background.geometry.render(layer.shader)





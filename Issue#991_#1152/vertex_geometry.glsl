#version 330

// This version uses the position and size to position the geometry before using the projection matrix.
// The geometry is expected in object space.
// Generally this is what someone would use if using their own geometry.

// This is the program compiled when calling Background.from_file()

in vec2 in_vert;
in vec2 in_uv;

uniform Projection {
    mat4 matrix;
} proj;

uniform vec2 size;
uniform vec2 pos;

out vec2 frag_uv;

void main() {
    frag_uv = in_uv;

    vec4 position = vec4(in_vert * size + pos, 0.0, 1.0);
    gl_Position = proj.matrix * position;
}

#version 330

in vec2 frag_uv;

uniform sampler2D tex;

out vec4 fragColor;

void main() {
    fragColor = texture(tex, frag_uv, 0);
}

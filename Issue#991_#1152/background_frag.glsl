#version 330

in vec2 frag_uv;

uniform sampler2D backgroundTexture;

uniform float depth;
uniform float blend;
uniform float scale;

uniform vec2 screenResolution;
uniform vec2 offset;
uniform vec2 size;
uniform vec2 rot;

out vec4 fragColor;

void main() {
    vec2 texSize = vec2(textureSize(backgroundTexture, 0));
    vec2 adjustedUV = frag_uv * screenResolution;
    vec2 adjustedOffset = offset / depth;

    vec2 adjusted = (adjustedUV + adjustedOffset);

    fragColor = vec4(0.0);
    if ((size.x == 0 || (0 <= adjusted.x && adjusted.x <= size.x*scale)) &&
            (size.y == 0 || (0 <= adjusted.y && adjusted.y <= size.y*scale))) {
        adjusted = vec2(rot.x*adjusted.x - rot.y*adjusted.y, rot.y*adjusted.x + rot.x*adjusted.y) / (scale * texSize);
        fragColor = texture(backgroundTexture, adjusted, 0);
        fragColor.a *= blend;
    }
}

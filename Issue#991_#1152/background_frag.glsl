#version 330

in vec2 frag_uv;

uniform sampler2D backgroundTexture;

uniform float depth;
uniform float blend;
uniform float scale;

uniform vec2 screenResolution;
uniform vec2 offset;

out vec4 fragColor;

void main() {
    vec2 texSize = vec2(textureSize(backgroundTexture, 0));
    vec2 adjustedUV = frag_uv * (screenResolution / texSize);
    vec2 adjustedOffset = offset / (depth * texSize);

    fragColor = texture(backgroundTexture, (adjustedUV + adjustedOffset)/scale, 0);
    fragColor.a *= (1-blend);
}

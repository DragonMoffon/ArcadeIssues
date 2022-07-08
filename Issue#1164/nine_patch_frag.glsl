#version 330

uniform vec4 base_uv;
uniform vec4 var_uv;

uniform float texture_id;

uniform sampler2D uv_texture;
uniform sampler2D sprite_texture;

in vec2 pos_uv;

out vec4 f_color;

void main() {
    vec2 tex_uv;
    if (pos_uv.x <= var_uv.x){
        tex_uv.x = pos_uv.x / var_uv.x * base_uv.x;
    }
    else if (pos_uv.x >= var_uv.z){
        tex_uv.x = base_uv.z + (pos_uv.x - var_uv.z) / (1 - var_uv.z) * (1 - base_uv.z);
    }
    else{
        tex_uv.x = base_uv.x + (pos_uv.x - var_uv.x) / (var_uv.z - var_uv.x) * (base_uv.z - base_uv.x);
    }

    if (pos_uv.y <= var_uv.y){
        tex_uv.y = pos_uv.y / var_uv.y * base_uv.y;
    }
    else if (pos_uv.y >= var_uv.w){
        tex_uv.y = base_uv.w + ((pos_uv.y - var_uv.w) / (1 - var_uv.w)) * (1 - base_uv.w);
    }
    else{
        tex_uv.y = base_uv.y + (pos_uv.y - var_uv.y) / (var_uv.w - var_uv.y) * (base_uv.w - base_uv.y);
    }

    vec4 uv_data = texelFetch(uv_texture, ivec2(texture_id, 0), 0);
    f_color += texture(sprite_texture, vec2(uv_data.x, 0.0) + pos_uv*uv_data.zw);
    //f_color = vec4(vec2(uv_data.x, uv_data.y) + pos_uv*uv_data.zw*vec2(1.0, -1.0), 0.0, 1.0);
}

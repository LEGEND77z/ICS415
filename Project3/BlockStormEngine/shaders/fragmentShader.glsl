#version 330 core
in  vec2 vTex;
out vec4 FragColor;

uniform sampler2D atlas;   // bound to texture unit 0

void main()
{
    FragColor = texture(atlas, vTex);
}

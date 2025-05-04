#version 330 core
layout(location = 0) in vec3 aPos;       // position
layout(location = 1) in vec2 aTexCoord;  // UV

uniform mat4 transform;

out vec2 vTex;        // pass UV to fragment shader

void main()
{
    gl_Position = transform * vec4(aPos, 1.0);
    vTex = aTexCoord;
}

from ursina import *

app = Ursina()

water_shader = Shader(
    language=Shader.GLSL,
    vertex="""
#version 430
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 uv;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  uv = p3d_MultiTexCoord0;
}
    """,
    fragment="""
#version 430
uniform float time;
uniform sampler2D p3d_Texture0;  // channel1
uniform sampler2D channel0;
in vec2 uv;
out vec4 color;

float avg(vec4 color) {
    return (color.r + color.g + color.b)/3.0;
}

void main() {
    float speed = 1.0;
    float scale = 0.5;
    float opacity = 0.5;
    
    vec2 scaledUv = uv * scale;

    vec4 water1 = texture(channel0, scaledUv + time*0.02*speed - 0.1);
    vec4 water2 = texture(channel0, scaledUv + time*speed*vec2(-0.02, -0.02) + 0.1);
           
    vec4 background = texture(p3d_Texture0, vec2(uv) + avg(water1) * 0.04);
    
    water1.rgb = vec3(avg(water1));
    water2.rgb = vec3(avg(water2));
       
    float alpha = 0.2;
    
    color = (water1 + water2) * alpha + background;
}
""")

water = Entity(
    model="plane",
    position=(0, -1, 0),
    scale=(10, 1, 10),
    rotation_x=-90,
    texture="water_bottom",
    shader=water_shader
)


water.set_shader_input("time", 0)
water.set_shader_input("channel0", load_texture("gray_noise"))

timer = 0


def update():
    global timer
    water.set_shader_input("time", timer)
    timer += 0.01


app.run()

#version 330

in vec3 point;
out vec3 xyz_coords;

void main() {
    xyz_coords = point;
    gl_Position = vec4(point, 1.);
}

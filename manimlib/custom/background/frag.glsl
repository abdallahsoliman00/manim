#version 330

in vec3 xyz_coords;
out vec4 frag_color;

uniform float iTime;
uniform float alpha;

// void main() {
//     vec2 uv = xyz_coords.xy;
//     uv.x *= 16./9.;

//     float d = length(uv);
//     d = smoothstep(0.1,0.8,d);

//     d = 0.1 / abs(sin(2. * d + iTime + uv.x * uv.y));
//     vec3 color = vec3(0.09, 0.09, 0.44);
//     frag_color = vec4(d*color, 1.);
// }

void main() {
    vec2 uv = xyz_coords.xy;
    uv.x *= 16./9.;
    
    // Create multiple wave patterns
    float wave1 = sin(uv.x * 3.0 + iTime * 2.0);
    float wave2 = sin(uv.y * 4.0 + iTime * 1.5);
    float wave3 = sin((uv.x + uv.y) * 2.0 + iTime * 3.0);
    float wave4 = sin(length(uv) * 6.0 - iTime * 2.5);
    
    // Combine waves
    float combined = (wave1 + wave2 + wave3 + wave4) * 0.25;
    
    // Create color cycling effect
    vec3 color1 = vec3(0.15, 0.15, 0.52);
    vec3 color2 = vec3(0.62, 0.1, 0.1);
    vec3 color3 = vec3(0.42, 0.5, 0.15);
    
    // Interpolate between colors based on wave values
    vec3 finalColor = mix(color1, color2, sin(combined + iTime) * 0.5 + 0.5);
    finalColor = mix(finalColor, color3, sin(combined * 2.0 + iTime * 0.7) * 0.3 + 0.3);
    
    // Add some intensity variation
    float intensity = 0.5 + 0.5 * sin(combined * 3.0 + iTime);

    // Navy blue background
    vec3 background_color = vec3(0.11, 0.22, 0.71);

    // Blend the effect with the navy background
    vec3 result = mix(background_color, finalColor * intensity, 0.85);

    frag_color = vec4(result, alpha);
}


#version 330 core

layout (location = 0) out vec4 fragColor;

/*
	all actions with textures should be carried out
	in linear color space

	below is gamma correction
*/
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;
uniform vec3 bg_color;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int voxel_id;
flat in int face_id;

void main(){
	vec2 face_uv = uv;
	face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

	vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;
	tex_col = pow(tex_col, gamma);

	tex_col *= shading;

	// fog
	float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
	tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00002 * fog_dist * fog_dist)));

	tex_col = pow(tex_col, inv_gamma);
	fragColor = vec4(tex_col, 1.0);
}
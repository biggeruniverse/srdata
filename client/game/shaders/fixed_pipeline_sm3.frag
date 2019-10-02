// (c) 2012 savagerebirth.com
#version 130
#extension GL_EXT_texture_array : enable

in float	fog;
in vec4		ambient;
in vec3		diffuse;
in vec3		lightAccumColor;
in float	rimFactor;

in vec4		ecPosition;

out vec4	gl_FragColor;

#include "shaders/fragShadow.glsl"

uniform sampler2D	texture0; 	// base texture

void main()
{
	vec4 color		= vec4(0.0);
        float diffuseMod	= 1.0;
	vec4 baseColor 		= texture2D(texture0, gl_TexCoord[0].st);

	if(baseColor.a*gl_Color.a < 0.05)
		discard;

	//Big: shadows
        diffuseMod = shadowCoef(gl_FragCoord.xyz);
	
	color = vec4(baseColor.rgb * (ambient.rgb + (diffuse*diffuseMod) + lightAccumColor)*gl_Color.rgb, baseColor.a*gl_Color.a);

	color.rgb = mix(gl_Fog.color.rgb, color.rgb, fog);
	
	gl_FragColor 	= color;
}

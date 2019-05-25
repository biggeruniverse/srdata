// (c) 2011 savagerebirth.com
#version 120

varying vec3 	normal;			// normal
varying vec4 	ecPosition;
varying float	fog;
varying vec4	ambient;
varying vec3 	alphas;
varying vec4	texlayer;
varying vec3	lightAccumColor;
varying vec4	color;
varying vec3	secondary_color;

#include "shaders/fragShadow.glsl"

uniform sampler2DArray	texture0; 	// base texture
uniform sampler2D	fow;	//fog of war
uniform sampler2D	slope;	//steepness

uniform float   showSlope;

void main()
{
	vec4 frag_color	= vec4(0.0);
	float diffuseMod= 1.0;

	vec4 baseColor 	= texture2DArray(texture0, vec3(gl_TexCoord[0].st, texlayer.x));
	vec4 layer1	= texture2DArray(texture0, vec3(gl_TexCoord[0].st, texlayer.y));
	vec4 layer2	= texture2DArray(texture0, vec3(gl_TexCoord[0].st, texlayer.z));
	//vec4 baseColor	= texture2D(texture0, glTexCoord[0].st);
	vec4 dynamap	= texture2D(fow, gl_TexCoord[2].st);
	vec4 steepness	= texture2D(slope, gl_TexCoord[2].st);

	frag_color.rgb = mix(baseColor.rgb, layer1.rgb, alphas.y);
	frag_color.rgb = mix(frag_color.rgb, layer2.rgb, alphas.z);
	frag_color.a = 1.0;

	//Big: shadows
#ifdef GLSL_SM3
        diffuseMod = shadowCoef(gl_FragCoord.xyz);
#endif

	frag_color.rgb *= (ambient.rgb + (color.rgb*diffuseMod*color.a)+lightAccumColor);
	frag_color.rgb = mix(frag_color.rgb, steepness.rgb, steepness.a*showSlope);
	frag_color.rgb = mix(frag_color.rgb, vec3(0.0,0.0,0.0), dynamap.a);
	frag_color.rgb = mix(gl_Fog.color.rgb, frag_color.rgb, fog);
	
	gl_FragColor 	= frag_color;
	//gl_FragColor = vec4(showSlope, showSlope, showSlope, 1.0);
	//gl_FragColor = vec4(gl_TexCoord[2].s,gl_TexCoord[2].t,diffuseMod,1.0);
}

//(c) 2012 savagerebirth.com
#version 130

in float	fog;
in vec4		ambient;
in vec3		diffuse;
in vec3		lightAccumColor;

in vec4		ecPosition;

out vec4	gl_FragColor;

#include "shaders/fragShadow.glsl"

uniform sampler2D	texture0; 	// base texture
uniform sampler2D	normalMap; 	// dissolve texture

void main()
{
	vec4 color		= vec4(0.0);
        float diffuseMod	= 1.0;
	vec4 baseColor 		= texture2D(texture0, gl_TexCoord[0].st);
	float alpha 		= texture2D(normalMap, gl_TexCoord[0].st).r;

	alpha = clamp(baseColor.a*gl_Color.a*alpha,0.0,1.0);

	//if(alpha < 0.05)
	//	discard;

        diffuseMod = shadowCoef(gl_FragCoord.xyz);
	
	color = vec4(baseColor.rgb * (ambient.rgb + (diffuse*diffuseMod)+lightAccumColor)*gl_Color.rgb, alpha);

	color.rgb = mix(gl_Fog.color.rgb, color.rgb, fog);
	
	//gl_FragColor 	= color;
	gl_FragColor    = vec4(1.0);
	//gl_FragColor 	= vec4(alpha,alpha,alpha,1.0);
}

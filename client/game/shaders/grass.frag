//(c) 2012 savagerebirth.com
#version 130
#extension GL_EXT_texture_array : enable

in float	fog;
in vec4		ambient;
in vec3		diffuse;
in vec3		lightAccumColor;
in vec4		outColor;
in vec2		outTexCoord;
in vec4		ecPosition;

#include "shaders/fragShadow.glsl"

uniform sampler2D	texture0; 	// base texture
uniform sampler2D	normalMap; 	// dissolve texture

out vec4 FragColor;

void main()
{
	vec4 baseColor 		= texture2D(texture0, outTexCoord.st);
	float alpha 		= texture2D(normalMap, outTexCoord.st).r;
	alpha = clamp(baseColor.a*outColor.a*alpha,0.0,1.0);
	float diffuseMod	= 1.0;

	diffuseMod = shadowCoef(gl_FragCoord.xyz);

	FragColor = vec4(baseColor.rgb * (ambient.rgb + diffuse*diffuseMod + lightAccumColor.rgb)*outColor.rgb, alpha);

	FragColor.rgb = mix(gl_Fog.color.rgb, FragColor.rgb, fog);

	//FragColor.rgb = vec3(outTexCoord.st,1.0);
	//FragColor.rgb = baseColor.rgb;
	//FragColor = outColor;
}

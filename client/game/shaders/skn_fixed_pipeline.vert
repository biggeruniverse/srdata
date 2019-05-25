// (c) 2011 savagerebirth.com
#version 120

#include "shaders/dqSkin.glsl"

varying float fog;
varying vec4 ambient;
varying vec3 diffuse;
varying vec3 lightAccumColor;
varying float rimFactor;

varying vec4 ecPosition;

uniform vec4 eyeWorld;

void main()
{
	float NdotL;
	vec3 lightDir;
	vec4 pos;
	vec3 normal;
	vec3 tangent = vec3(0.0);
	vec4 ecPos;

	// pass texture coords
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;
	gl_TexCoord[2] = gl_MultiTexCoord2;
	gl_TexCoord[3] = gl_MultiTexCoord3;

	skinVertex(pos, normal, tangent);

	normal = normalize(normal);

	ecPos = gl_ModelViewMatrix * pos;	
	ecPosition = gl_ModelViewProjectionMatrix * pos;

	ambient = gl_LightModel.ambient;

	/***** LINEAR FOG *********/
	gl_FogFragCoord = abs(ecPosition.z);
	fog = (gl_Fog.end - gl_FogFragCoord) * gl_Fog.scale;
	fog = clamp(fog, 0.0, 1.0);

	/***** FIXED-FUNCTION VERTEX LIGHTING *****/
	lightDir = (gl_ModelViewMatrixInverse * gl_LightSource[0].position).xyz; //LIGHT0 is assumed to be the sun, and directional(normalized)
	NdotL = max(dot(normal, lightDir), 0.0);

	diffuse = gl_FrontMaterial.diffuse.rgb * gl_LightSource[0].diffuse.rgb * NdotL;

	lightDir = (gl_ModelViewMatrixInverse * gl_LightSource[1].position).xyz; 
	NdotL = max(dot(normal, lightDir), 0.0);
	lightAccumColor = gl_FrontMaterial.diffuse.rgb * gl_LightSource[1].diffuse.rgb * NdotL;

	rimFactor = smoothstep(0.5, 1.0, 1.0-max(0.0, dot(normalize(gl_NormalMatrix * normal), normalize(-ecPos.xyz))));
	rimFactor *= rimFactor;

#ifdef SR_VERTEX_ONLY
	gl_FrontColor = vec4((ambient.rgb + diffuse + lightAccumColor)*gl_Color.rgb, gl_Color.a);
#else
	//gl_FrontColor = vec4(diffuse*gl_Color.rgb, gl_Color.a);
	gl_FrontColor = gl_Color;
#endif

	gl_Position = ecPosition;
}

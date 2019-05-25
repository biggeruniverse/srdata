// (c) 2011 savagerebirth.com
#version 120

#include "shaders/dqSkin.glsl"

varying vec4 lightPos;
varying vec4 lightPos1;
varying vec3 viewV;
varying float fog;
varying float rimFactor;
varying vec3 halfVector;
varying vec4 ambient;
varying vec3 normal;

varying vec4 ecPosition;

uniform vec4 eyeWorld;

void main()
{
	vec4 pos;
	vec3 tangent = vec3(0.0);

	// pass texture coords
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;
	gl_TexCoord[2] = gl_MultiTexCoord2;
	gl_TexCoord[3] = gl_MultiTexCoord3;
	tangent = normalize(gl_MultiTexCoord2.xyz); //everyone loves it

	skinVertex(pos, normal, tangent);

	vec4 ecPos = gl_ModelViewMatrix * pos;
	vec4 vPos = gl_ProjectionMatrix * ecPos;

	normal = normalize(normal);
	tangent = normalize(tangent);

	//// EYE CAM POSITITION ////
	ecPosition = gl_ModelViewMatrix * pos;
	
	//float aI = 0.75 + max(0.0, 0.25 * (dot(vec3(0.0, 0.0, 1.0), normal)));
	float aI = 1.0;

	ambient = gl_LightModel.ambient * aI;
	
	//// LINEAR FOG ////
	gl_FogFragCoord = abs(vPos.z);
	fog = (gl_Fog.end - gl_FogFragCoord) * gl_Fog.scale;
	fog = clamp(fog, 0.0, 1.0);


	//// RIM LIGHT ////

	rimFactor = smoothstep(0.5, 1.0, 1.0-max(0.0, dot(normalize(gl_NormalMatrix * normal), normalize(-ecPos.xyz))));
	rimFactor *= rimFactor;

	//// TBN AND DYNAMIC LIGHTS ////
	
	vec3 binormal = cross(normal, tangent); 
	binormal = normalize(binormal) * gl_MultiTexCoord2.w;
	
	mat3 tbn_mat = mat3(tangent, binormal, normal);

	//// Transform Light and Eye into Tangent Space ////
	//lightPos 	= gl_LightSource[0].position * gl_ModelViewMatrix;
	lightPos = gl_ModelViewMatrixInverse * gl_LightSource[0].position;	
	lightPos.w   = gl_LightSource[0].position.w;
	lightPos.xyz	*= tbn_mat;
	lightPos.xyz	= normalize(lightPos.xyz);

	lightPos1 		= gl_ModelViewMatrixInverse * gl_LightSource[1].position;
	lightPos1.w   = gl_LightSource[1].position.w;
	lightPos1.xyz	*= tbn_mat;	
	lightPos1.xyz	= normalize(lightPos1.xyz);
	
	viewV		= -gl_Vertex.xyz + eyeWorld.xyz;
	viewV 		*= tbn_mat;
	viewV		= normalize(viewV);
	
	// normalized in fragment shader!
	halfVector 	= lightPos.xyz + viewV.xyz;	
	
	//gl_FrontColor = vec4(tangent.xyz * 0.5 + 1.0, 1.0);

	gl_FrontColor = gl_Color;
	gl_Position = vPos;
}

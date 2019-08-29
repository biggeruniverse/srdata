// (c) 2011 savagerebirth.com
#version 120

attribute vec4 blendWeights;
attribute vec4 blendIndices;
attribute float numBones;

varying vec3 normal;

uniform mat2x4 boneMatrices[100];
uniform int  useBones;
uniform vec4 eyeWorld;

void main()
{
	vec4 pos = vec4(0.0);
	vec3 tangent = vec3(0.0);

	vec4 curindex = blendIndices;
	vec4 curweight = blendWeights;

	// pass texture coords
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;
	gl_TexCoord[2] = gl_MultiTexCoord2;
	gl_TexCoord[3] = gl_MultiTexCoord3;
	vec3 tang = normalize(gl_MultiTexCoord2.xyz); //everyone loves it

	normal = vec3(0.0);
	
	//// SKINNING ////
	if(useBones == 1) {
		for(int i = 0; i< int(numBones); i++) {
			mat4 m44 = mat4(boneMatrices[int(curindex.x)]);
	
			mat3 m33 = mat3(m44[0].xyz,
					m44[1].xyz,
					m44[2].xyz);
	
			pos += m44 * gl_Vertex * curweight.x;
			normal += m33 * gl_Normal * curweight.x;
			tangent += m33 * tang * curweight.x;
	
			//shift
			curindex = curindex.yzwx;
			curweight = curweight.yzwx;
		}
	} else {
		pos = gl_Vertex;
		normal = gl_Normal;
	}

	gl_Position = gl_ModelViewProjectionMatrix * pos;
	normal = normalize(normal);
	tangent = normalize(tangent);

	//// EYE CAM POSITITION ////
	vec4 ecPosition = gl_ModelViewMatrix * gl_Vertex;
	
	vec3 ecPosition3 = ecPosition.xyz / ecPosition.w;

	normal = normalize(gl_NormalMatrix * normal);
	//gl_FrontColor = vec4(tangent.xyz * 0.5 + 1.0, 1.0);
	gl_FrontColor = gl_Color;
}

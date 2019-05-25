attribute vec4 blendWeights;
attribute vec4 blendIndices;
attribute float numBones;

uniform mat4 boneMatrices[50];
uniform int useBones;

void skinVertex(out vec4 pos, out vec3 normal, inout vec3 tangent)
{
	vec4 curindex = blendIndices;
	vec4 curweight = blendWeights;
	vec3 t = tangent;

	tangent = vec3(0.0);

	if(useBones == 1) {
		pos = vec4(0.0);
		normal = vec3(0.0);

		//// SKINNING ////
        	for(int i = 0; i< int(numBones); i++) {
			mat4 m44 = boneMatrices[int(curindex.x)];

			mat3 m33 = mat3(m44[0].xyz,
					m44[1].xyz,
					m44[2].xyz);

			pos += m44 * gl_Vertex * curweight.x;
			normal += m33 * gl_Normal * curweight.x;
			tangent += m33 * t * curweight.x;

			//shift
			curindex = curindex.yzwx;
			curweight = curweight.yzwx;
		}
	} else {
		pos = gl_Vertex;
		normal = gl_Normal;
	}
}

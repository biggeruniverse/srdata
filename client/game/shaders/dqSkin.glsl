attribute vec4 blendWeights;
attribute vec4 blendIndices;
attribute float numBones;

uniform mat2x4 boneMatrices[100];
uniform int useBones;

void skinVertex(out vec4 pos, out vec3 normal, inout vec3 tangent)
{
	vec4 curindex = blendIndices;
	vec4 curweight = blendWeights;
	vec3 t = tangent;

	if(useBones == 1) {
		mat2x4 blendedDQ = mat2x4(0.0);

		//// SKINNING ////
        	for(int i = 0; i< int(numBones); i++) {
			blendedDQ += boneMatrices[int(curindex.x)]*curweight.x;

			//shift
			curindex = curindex.yzwx;
			curweight = curweight.yzwx;
		}
		float len = length(blendedDQ[0]);
		blendedDQ /= len;

		pos = vec4(gl_Vertex.xyz + 2.0*cross(blendedDQ[0].yzw, cross(blendedDQ[0].yzw, gl_Vertex.xyz) + blendedDQ[0].x*gl_Vertex.xyz), 1.0);
		pos.xyz += 2.0*(blendedDQ[0].x*blendedDQ[1].yzw - blendedDQ[1].x*blendedDQ[0].yzw + cross(blendedDQ[0].yzw, blendedDQ[1].yzw));

		normal = gl_Normal + 2.0*cross(blendedDQ[0].yzw, cross(blendedDQ[0].yzw, gl_Normal) + blendedDQ[0].x*gl_Normal);

		tangent = t + 2.0*cross(blendedDQ[0].yzw, cross(blendedDQ[0].yzw, t) + blendedDQ[0].x*t);
	} else {
		pos = gl_Vertex;
		normal = gl_Normal;
	}
}

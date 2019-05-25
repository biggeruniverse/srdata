#extension GL_EXT_texture_array : enable

#ifdef GLSL_SM3
uniform sampler2DArrayShadow    shadowMap;
uniform vec2                    camClip;
uniform vec4                    csmSplitDist;
uniform int			shadowsEnabled;

float shadowCoef(vec3 frag)
{
	float near = camClip.x;
	float far = camClip.y;
	float index = 3.0;
	float depth = (near * near) / (far + near - frag.z* (far-near));
	depth *= far;

	if(shadowsEnabled==0)
		return 1.0;

        if(depth < csmSplitDist.x)
                index=0.0;
        else if (depth < csmSplitDist.y)
                index=1.0;
        else if (depth < csmSplitDist.z)
                index=2.0;

        vec4 shadow_coord = gl_TextureMatrix[int(index)+4]*ecPosition;

        shadow_coord.xyz /= shadow_coord.w;

        shadow_coord.w = shadow_coord.z;

        shadow_coord.z = index;

        return shadow2DArray(shadowMap, shadow_coord).x;
}
#endif

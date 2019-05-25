//(c) 2012 savagerebirth.com
#version 130
#extension GL_EXT_texture_array : enable

//#define RAYEFFECT

uniform float		bloomMix;
uniform vec2		camClip;
uniform vec4		eyeWorld;
uniform vec4		csmSplitDist;
#ifdef RAYEFFECT
uniform mat4		mvpInverse;
#endif

uniform sampler2D       texture0;       // base texture
uniform sampler2D       texture1;       // SSAO
uniform sampler2D       bloomTex;       // bloom

#include "shaders/blurs.glsl"

#ifdef RAYEFFECT

const int SAMPLES = 50;
const float EXPOSURE = 0.2;
const float DECAY = 0.5;

vec3 addRays(vec2 tx) {
	float depth = texture2D(depthTex, tx).x;
	vec3 pos, forward;
	vec4 far, near;
	vec4 preWorld = vec4((gl_FragCoord.xy * screenScale.xy), depth, 1.0);
	vec3 color = vec3(0.0);
	mat4 remap = mat4(2.0, 0.0, 0.0, -1.0, 0.0, 2.0, 0.0, -1.0, 0.0, 0.0, 2.0, -1.0, 0.0, 0.0, 0.0, 1.0);
	mat4 invMat = mvpInverse * remap;

	far = preWorld * invMat;
	far.xyz /= far.w;

	preWorld.z = 0.0;
	near = preWorld * invMat;
	near.xyz /= near.w;

	forward = normalize(far.xyz - near.xyz);
	float delta = distance(far, near) / float(SAMPLES*3);

	pos = far.xyz;
	for(int i=0;i<SAMPLES;i++) {
		pos -= forward * delta;	
		color += vec3(0.1, 0.1, 0.1) * shadowCoef(pos) * 0.1;
	}

	return color * EXPOSURE;
}

#endif

out vec4 gl_FragColor;

void main()
{
	vec3 lum        = vec3(0.299, 0.587, 0.114);

        vec4 baseColor          = texture2D(texture0, gl_TexCoord[0].st);
        vec4 aomix              = texture2D(texture1, gl_TexCoord[0].st);
        vec3 bloom              = texture2DBilinear(bloomTex, gl_TexCoord[0].st, screenScale).rgb;

	//float bloomlum = step(.5, dot(lum,bloom.rgb));
	float bloomlum = 1.0;

	gl_FragColor 	 = vec4(baseColor.rgb*aomix.rgb + gl_Color.rgb, 1.0);
	gl_FragColor.rgb += (bloomlum * bloom.rgb)*bloomMix;
#ifdef RAYEFFECT
	gl_FragColor.rgb += addRays(gl_TexCoord[0].st);
#endif
	//gl_FragColor.rgb = baseColor.rgb + gl_Color.rgb;
	//gl_FragColor.rgb = aomix.rgb;
	//gl_FragColor.rgb = bloomlum * bloom.rgb;
}

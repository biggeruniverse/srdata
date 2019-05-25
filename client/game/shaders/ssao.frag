// (c) 2012 savagerebirth.com
#version 130
const float strength = 0.014;
const float offset = 36.0;
const float radius = 0.00012;
const float falloff = 0.000002;
const float invSamples = -1.38/10.0;

uniform sampler2D texture0;
uniform sampler2D normalMap;

void main(void)
{
	vec3 pSphere[10] = vec3[](vec3(-0.010735935, 0.01647018, 0.0062425877),vec3(-0.06533369, 0.3647007, -0.13746321),vec3(-0.6539235, -0.016726388, -0.53000957),vec3(0.40958285, 0.0052428036, -0.5591124),vec3(-0.1465366, 0.09899267, 0.15571679),vec3(-0.44122112, -0.5458797, 0.04912532),vec3(0.03755566, -0.10961345, -0.33040273),vec3(0.019100213, 0.29652783, 0.066237666),vec3(0.8765323, 0.011236004, 0.28265962),vec3(0.29264435, -0.40794238, 0.15964167));
	float bl = 0.0;

	vec3 fresnel = normalize((texture(normalMap, gl_TexCoord[0].st*offset).rgb*2.0)-vec3(1.0));
	//vec3 fresnel = texture(normalMap, gl_TexCoord[0].st*offset).rgb;
	vec4 pixel = texture(texture0, gl_TexCoord[0].st);
	float depth = (camClip.x * camClip.x) / (camClip.y + camClip.x - pixel.a * (camClip.y - camClip.x));
	vec3 pos = vec3(gl_TexCoord[0].st, depth);
	vec3 normal = pixel.xyz;

	float radD = radius / depth;
	
	float occluderDepth, diff;
	vec4 occluderFrag;
	vec3 ray;

	for(int i=0; i<10;i++)
	{
		vec3 ray = radD*reflect(pSphere[i], fresnel);
	
		occluderFrag = texture(texture0, pos.xy + sign(dot(ray, normal))*ray.xy);
		diff = depth - (camClip.x * camClip.x) / (camClip.y + camClip.x - occluderFrag.a * (camClip.y - camClip.x));

		bl += step(falloff, diff)*(1.0-dot(occluderFrag.xyz,normal))*(1.0-smoothstep(falloff, strength, diff));
	}

	gl_FragColor.rgb = vec3(1.0+bl*invSamples);
	//gl_FragColor.rgb = fresnel;
	//gl_FragColor.rgb = pixel.rgb;
	//gl_FragColor.rgb = vec3(depth);
}

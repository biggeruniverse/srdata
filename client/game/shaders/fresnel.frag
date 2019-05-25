//(c) 2012 savagerebirth.com
#version 120

varying vec3 		normal;			// normal
varying vec3 		ecPosition3;
varying float		fog;
varying vec4		ambient;

varying vec3		lightDir;

//Big: shadows
varying vec4		shadowCoord;

uniform sampler2D	texture0; 	// base texture
uniform sampler2D	texture1; 	// shadows texture
uniform sampler2D	normalMap;	// normal map
uniform sampler2D	texture3;	// framebuffer
uniform sampler2D	texture4;	// depthbuffer

uniform vec4            ps_pb_cs_hs;
uniform vec2		screenScale;
uniform vec2		camClip;

void main()
{
	vec4 color		= vec4(0.0);
        float diffuseMod	= 1.0;
	float fresnel		= 1.0;
	vec4 baseColor 		= vec4(0.17, 0.27, 0.44, 1.0);
	vec3 ecPos		= normalize(-ecPosition3);

	//// REFRACTION ////
	vec3 normalMap	= normalize(2.0* texture2D(normalMap, gl_TexCoord[0].st*10.0).rgb - 1.0);
	vec3 projCoord = gl_TexCoord[1].xyz;
	projCoord.xy += 1.03 * normalMap.rg;

	//// SHADOWS ////
        vec4 shadowCoordCorrect = shadowCoord / shadowCoord.w;
        float distFromLight = texture2D(texture1, shadowCoordCorrect.st).r;
        diffuseMod = step(shadowCoordCorrect.z, distFromLight);

	//// FRESNEL ////
	fresnel = dot(ecPos, normalize(normal));

	//// SPECULAR ////
	vec3 refVec = reflect(lightDir, normalMap);
	float specular = max(dot(normalize(refVec), ecPos), 0.0);
	specular = pow(specular, 256.0);

	//// FRAMEBUFFER ////
	projCoord.xy *= screenScale;
	vec4 tex0 = texture2DProj(texture3, projCoord);

	//// DEPTH ////
	float screenDepth = texture2D(texture4, (ecPosition3.xy/ecPosition3.z)*screenScale).r*camClip.y;
	//float screenDepth = texture2D(texture4, gl_TexCoord[1].st).r;
	baseColor.a = clamp((screenDepth-ecPosition3.z)/camClip.y, 0.1, 1.0);


	//gl_FragColor = vec4(baseColor.a);
	gl_FragColor = mix(baseColor, tex0, fresnel) + specular;
	//gl_FragColor = vec4(normalMap.rgb, 1.0);
	//gl_FragColor = tex0 + specular;
}

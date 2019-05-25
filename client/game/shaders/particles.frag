//(c) 2012 savagerebirth.com

//varying vec3 		normal;			// normal
varying vec3 		ecPosition3;

uniform vec2		screenScale;
uniform sampler2D	texture0; 	// base texture
//uniform sampler2D	texture1; 	// shadows texture
//uniform sampler2D	texture2;
//uniform sampler2D	texture3;	// framebuffer
//uniform sampler2D	texture4;	// depthbuffer

void main()
{
	vec4 baseColor 	= texture2D(texture0, gl_TexCoord[0].st)*gl_Color;

	vec2 coord = ecPosition3.xy*screenScale;
	coord.y = 1.0-coord.y;

	//soft-particles! mix in from depth
	//float screenDepth = (zFar * 2.0) / (zFar - texture2D(texture4, coord).r*zFar);
	//float screenMod = (screenDepth - ecPosition3.z)/zFar;
	//screenMod = clamp(screenMod, 0.0, 1.0);

	//float alpha = screenMod*baseColor.a;

	gl_FragColor = baseColor*gl_FrontMaterial.diffuse;
	//gl_FragColor 	= vec4(baseColor.rgb*screenMod, alpha);
}

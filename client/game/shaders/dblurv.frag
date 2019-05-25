//(c) 2012 savagerebirth.com
#version 130

//#inc#

uniform vec2		screenScale;
uniform vec2		camClip;

uniform sampler2D	texture0; 	// base texture
uniform sampler2D	texture1; 	// depth texture

out vec4 fragColor;

float gauss(in float x)
{
	float mu = 2.0;

	return (2.507*mu)*(1.0/(2.507*mu) * pow(2.7183, -(x*x)/(2.0*mu*mu)));
}

float passDepth(in float comp, in vec2 coord)
{
	return 1.0-step(.5,abs((camClip.x * camClip.x) / (camClip.y + camClip.x - texture(texture1, coord ).x * (camClip.y-camClip.x))-comp));
}

void main()
{
	vec4 baseColor = texture(texture0, gl_TexCoord[0].st);
	float depth = (camClip.x * camClip.x) / (camClip.y + camClip.x - texture(texture1, gl_TexCoord[0].st ).x * (camClip.y-camClip.x));
	
    baseColor *= smoothstep(.1, .5, dot(vec3(0.299, 0.587, 0.114), baseColor.rgb));
	
	//above
	for(int i=1; i<5;i++)
	{
		vec2 tc = gl_TexCoord[0].st+vec2(0.0,-i)* screenScale;
		vec4 color = texture(texture0, tc);
		baseColor += color*dot(vec3(0.299, 0.587, 0.114), color.rgb)*gauss(float(i))*passDepth(depth, tc);
	}

	//below
	for(int i=1; i<5;i++)
	{
		vec2 tc = gl_TexCoord[0].st+vec2(0.0,i)*screenScale;
		vec4 color = texture(texture0, tc);
		baseColor += color*dot(vec3(0.299, 0.587, 0.114), color.rgb)*gauss(float(i))*passDepth(depth, tc);
	}
	
	fragColor = vec4(baseColor.rgb, gl_Color.a);
}

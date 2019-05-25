//(c) 2012 savagerebirth.com

uniform vec2		screenScale;

//const vec3 lum = vec3(0.299, 0.587, 0.114);
const vec3 lum = vec3(1.0, 1.0, 1.0);
const int kernelSize = 5;

float gauss(float x)
{
	const float mu = 2.0;
	
	return (2.507*mu)*(1.0/(2.507*mu) * pow(2.7183, -(x*x)/(2.0*mu*mu)));
}

vec4 cubic(float x)
{
	float x2 = x * x;
	float x3 = x2 * x;
	vec4 w;
	w.x =   -x3 + 3*x2 - 3*x + 1;
	w.y =  3*x3 - 6*x2       + 4;
	w.z = -3*x3 + 3*x2 + 3*x + 1;
	w.w =  x3;
	return w / 6.f;
}

vec3 hblur(in sampler2D tex, in vec2 coord)
{
	vec3 color = vec3(0.0);

	for(int i=0;i<kernelSize;i++)
	{	
		int off = i-2;
		vec3 tc = texture2D(tex, coord+vec2(off, 0)*screenScale).rgb;
		color += tc * dot(lum, tc)*gauss(float(abs(off)));
	}

	return color;
} 

vec3 vblur(in sampler2D tex, in vec2 coord)
{
	vec3 color = vec3(0.0);

	for(int i=0;i<kernelSize;i++)
	{	
		int off = i-2;
		vec3 tc = texture2D(tex, coord+vec2(0, off)*screenScale).rgb;
		color += tc * dot(lum, tc)*gauss(float(abs(off)));
	}

	return color;
} 

//specialized blurs
vec3 hblurlum(in sampler2D tex, in vec2 coord, in float cutoff)
{
	vec3 color = vec3(0.0);

	for(int i=0;i<kernelSize;i++)
	{	
		int off = i-2;
		vec3 tc = texture2D(tex, coord+vec2(off, 0)*screenScale).rgb;
		color += tc * smoothstep(cutoff, 1.0, dot(lum, tc))*gauss(float(abs(off)));
	}

	return color;
}

vec4 texture2DBilinear(in sampler2D tex, in vec2 coord, in vec2 blurTexSize) {
	float scale = 3;

	vec4 tl = texture2D(tex, coord + vec2(0.0, 0.0));
	vec4 tr = texture2D(tex, coord + vec2(blurTexSize.x, 0.0)*scale);
	vec4 bl = texture2D(tex, coord + vec2(0.0, blurTexSize.y)*scale);
	vec4 br = texture2D(tex, coord + vec2(blurTexSize.x, blurTexSize.y)*scale);

	vec2 f = fract(vec2(coord.x * (1/blurTexSize.x), coord.y * (1/blurTexSize.y)));
	vec4 tA = mix(tl, tr, f.x);
	vec4 tB = mix(bl, br, f.x);

	return mix(tA, tB, f.y);
}

vec4 texture2DBicubic(in sampler2D tex, in vec2 coord, in vec2 blurTexSize) {
	float fx = fract(coord.x);
	float fy = fract(coord.y);
	coord.x -= fx;
	coord.y -= fy;

	vec4 xcubic = cubic(fx);
	vec4 ycubic = cubic(fy);

	vec4 c = vec4(coord.x - 0.5, coord.x + 1.5, coord.y - 0.5, coord.y + 1.5);
	vec4 s = vec4(xcubic.x + xcubic.y, xcubic.z + xcubic.w, ycubic.x + ycubic.y, ycubic.z + ycubic.w);
	vec4 offset = c + vec4(xcubic.y, xcubic.w, ycubic.y, ycubic.w) / s;

	vec4 sample0 = texture2D(tex, vec2(offset.x, offset.z) );
	vec4 sample1 = texture2D(tex, vec2(offset.y, offset.z) );
	vec4 sample2 = texture2D(tex, vec2(offset.x, offset.w) );
	vec4 sample3 = texture2D(tex, vec2(offset.y, offset.w) );

	float sx = s.x / (s.x + s.y);
	float sy = s.z / (s.z + s.w);

	return mix( mix(sample3, sample2, sx), mix(sample1, sample0, sx), sy);
}

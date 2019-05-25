// another SSAO impl that doesn't need normals
#version 130

#define PI    3.14159265

//#inc#

const int samples = 8; //samples on the first ring (4-8)
const int rings = 6; //ring count (3-6)

uniform vec2 screenScale;
uniform vec2 camClip;

uniform sampler2D texture0;

out vec4 gl_FragColor;

vec2 rand(in vec2 coord) //generating random noise
{
	float noiseX = (fract(sin(dot(coord ,vec2(12.9898,78.233))) * 43758.5453));
	float noiseY = (fract(sin(dot(coord ,vec2(12.9898,78.233)*2.0)) * 43758.5453));
	return vec2(noiseX,noiseY)*0.004;
}

float readDepth(in vec2 coord) 
{
	return (camClip.x * camClip.x) / (camClip.y + camClip.x - texture(texture0, coord ).x * (camClip.y-camClip.x)); 	
}

float compareDepths( in float depth1, in float depth2 )
{
	float aoCap = 1.0;
	float aoMultiplier = 150.0;
	float depthTolerance = 0.0001;
	float aorange = 0.010533;
	float diff = sqrt(clamp(1.0-(depth1-depth2) / aorange,0.0,1.0));
	float ao = min(aoCap,max(0.0,depth1-depth2-depthTolerance) * aoMultiplier) * diff;
	return ao;
}

void main()
{	
	float depth = readDepth(gl_TexCoord[0].st);
	float d;
	
	float aspect = pow(screenScale.x,-1)*screenScale.y;
	vec2 noise = rand(gl_TexCoord[0].st);
	
	float w = screenScale.x/clamp(depth,0.05,1.0)+(noise.x*(1.0-noise.x));
	float h = screenScale.y/clamp(depth,0.05,1.0)+(noise.y*(1.0-noise.y));
	
	float pw;
	float ph;

	float ao;	
	float s;
	float fade = 1.0;
	
	for (int i = 0 ; i < rings; i += 1)
	{
		fade *= 0.5;
		for (int j = 0 ; j < samples*i; j += 1)
		{
			float step = PI*2.0 / (samples*float(i));
			pw = (cos(float(j)*step)*float(i));
			ph = (sin(float(j)*step)*float(i))*aspect;
			d = readDepth( vec2(gl_TexCoord[0].st.s+pw*w,gl_TexCoord[0].st.t+ph*h));
			ao += compareDepths(depth,d)*fade;
			s += 1.0*fade;
		}
	}
	
	ao /= s;
	ao = 1.0-ao;	
    
	gl_FragColor = vec4(ao,ao,ao, 1.0)+depth;
}


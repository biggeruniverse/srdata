// (c) 2012 savagerebirth.com
#version 130

const float PI=3.1415926535;
const int waveCount=4;

out float fog;
out vec4 ambient;
out vec3 diffuse;
out vec3 lightAccumColor;
out vec4 ecPosition;
out vec2 outTexCoord;
out vec4 outColor;

in vec4 inVertex;
in vec4 inColor;
in vec2 inTexCoord;
in vec2 inKernelOffset;
in vec2 patchOffset;

uniform vec4 camUp;
uniform vec4 camRight;
uniform vec2 windVec;
uniform vec4 eyeWorld;
uniform float zGrass;
uniform float time;
uniform vec4 amplitude;
uniform vec4 wavelength;
uniform vec4 speed;
uniform vec2 wavedir[4];

uniform vec2 worldOffset;
uniform vec2 texScale;
uniform vec2 patchScale;
uniform vec2 mapSize;
uniform sampler2D coverageTex;

float waveInfluence()
{
	float H = 0.0;
	float freq;
	vec4 amp=amplitude, wl=wavelength, spd=speed;
	vec2 pos = inVertex.xy + worldOffset*mapSize;


	//calculate wave influence for the vertex (sum of sines)
	int i;
	for(i=0;i<waveCount;i++)
	{
		freq = 2.0*PI/wl.x;
		H += amp.x * sin(dot(wavedir[i],pos)*freq+time*spd.x*freq);
		amp = amp.yzwx;
		wl = wl.yzwx;
		spd = spd.yzwx;
	}

	return H*1.5;
}

vec3 calcNormal(in vec2 coord)
{
	vec3 normal;
	vec2 c1 = vec2(0.0, 2.0)*texScale;
	vec2 c2 = vec2(2.0, 0.0)*texScale;

	vec3 b = vec3(c1, textureLod(coverageTex, coord+c1, 0.0).z);
	vec3 c = vec3(c2, textureLod(coverageTex, coord+c2, 0.0).z);

	return cross(b, c);
}

void main()
{
	float NdotL, H;
	vec3 lightDir, windInf;
	float dist = length(inVertex.xyz+vec3(worldOffset.xy*mapSize,0.0)-eyeWorld.xyz)/zGrass;
	vec4 coverage = textureLod(coverageTex, patchOffset*patchScale + worldOffset, 0.0);
	vec3 normal = calcNormal(patchOffset*patchScale + worldOffset);

	// pass texture coords
	outTexCoord = inTexCoord;
	outTexCoord.t = round(coverage.r*4.0)/4.0+0.25*(1.0-inKernelOffset.y);

	H = waveInfluence()*inKernelOffset.y*coverage.a*inTexCoord.t;

	windInf = vec3(windVec.x*H*2.0, windVec.y*H*2.0, 0);

	//vec4 vPos = vec4(inVertex.xyz+camUp.xyz*20.0*inKernelOffset.y*coverage.a+camRight.xyz*15.0*inKernelOffset.x+windInf*coverage.a, inVertex.w);
	vec4 vPos = vec4(inVertex.xyz+camUp.xyz*20.0*inKernelOffset.y*coverage.a+windInf*coverage.a, inVertex.w);

	vPos.z += coverage.z;

	ecPosition = gl_ModelViewMatrix * vPos;

	ambient = gl_LightModel.ambient;

	/***** LINEAR FOG *********/
        gl_FogFragCoord = abs(ecPosition.z/ecPosition.w);
        fog = (gl_Fog.end - gl_FogFragCoord) * gl_Fog.scale;
        fog = clamp(fog, 0.0, 1.0);

	/***** FIXED-FUNCTION VERTEX LIGHTING *****/
	lightDir = (gl_ModelViewMatrixInverse * gl_LightSource[0].position).xyz; //LIGHT0 is assumed to be the sun, and directional(normalized)
	NdotL = clamp(dot(normal, lightDir)+0.5, 0.0, 1.0);

	windInf = vec3(1.0,1.0,1.0)*clamp(H,0.4,1.0);

	diffuse = (gl_FrontMaterial.diffuse.rgb * gl_LightSource[0].diffuse.rgb * NdotL)*windInf;

	lightDir = (gl_ModelViewMatrixInverse * gl_LightSource[1].position).xyz;
	NdotL = max(dot(normal, lightDir), 0.0);

	lightAccumColor = gl_LightSource[1].diffuse.rgb * NdotL;

	outColor = vec4(inColor.rgb, inColor.a*clamp(1.0-dist, 0.0, 1.0));
	gl_Position = gl_ProjectionMatrix * ecPosition;
}

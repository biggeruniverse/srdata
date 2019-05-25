// (c) 2011 savagerebirth.com
#version 120

attribute vec3 mixlayer;
attribute vec3 tangent;
attribute vec4 materials;

varying vec3 normal;
varying vec4 ecPosition;
varying float fog;
varying vec4 ambient;
varying vec3 alphas;
varying vec4 texlayer;
varying vec3 lightAccumColor;
varying vec4 color;
varying vec3 secondary_color;

void main()
{
	float NdotL;
	vec3 lightDir;
	vec4 vPos;

	color = gl_Color;

	// transform normal
	normal = normalize(gl_NormalMatrix * gl_Normal);
	
	// pass texture coords
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;
	gl_TexCoord[2] = gl_MultiTexCoord2;
	//gl_TexCoord[3] = gl_MultiTexCoord3;

	vPos = gl_ModelViewMatrix * gl_Vertex;
	ecPosition = vPos;

	ambient = gl_LightModel.ambient;

	/***** LINEAR FOG *********/
        gl_FogFragCoord = abs(vPos.z/vPos.w);
        fog = (gl_Fog.end - gl_FogFragCoord) * gl_Fog.scale;
        fog = clamp(fog, 0.0, 1.0);

	/***** FIXED-FUNCTION VERTEX LIGHTING *****/
	lightDir = normalize((gl_ModelViewMatrixInverse * gl_LightSource[0].position).xyz); //LIGHT0 is assumed to be the sun, and directional(normalized)
	NdotL = max(dot(gl_Normal, lightDir), 0.0);

	color.rgb *= gl_LightSource[0].diffuse.rgb * NdotL;

	lightDir = normalize((gl_ModelViewMatrixInverse * gl_LightSource[1].position).xyz);
	NdotL = max(dot(gl_Normal, lightDir), 0.0);

	lightAccumColor = gl_LightSource[1].diffuse.rgb * NdotL;

	secondary_color = gl_SecondaryColor.rgb;
	
	gl_Position = gl_ProjectionMatrix * ecPosition;

	texlayer = materials;
	alphas = mixlayer;
}

// (c) 2011 savagerebirth.com

varying vec3 normal;
varying float fog;
varying vec4 ambient;
varying vec3 diffuse;
varying vec3 lightAccumColor;

//Big: shadows
varying vec4 ecPosition;

void main()
{
	float NdotL;
	vec3 lightDir;
	
	// transform normal
	normal = normalize(gl_NormalMatrix * gl_Normal);
	
	// pass texture coords
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;
	gl_TexCoord[2] = gl_MultiTexCoord2;
	gl_TexCoord[3] = gl_MultiTexCoord3;

	ecPosition = gl_ModelViewMatrix * gl_Vertex;

	ambient = gl_LightModel.ambient;

	/***** LINEAR FOG *********/
	gl_FogFragCoord = abs(ecPosition.z/ecPosition.w);
	fog = (gl_Fog.end - gl_FogFragCoord) * gl_Fog.scale;
	fog = clamp(fog, 0.0, 1.0);

	/***** FIXED-FUNCTION VERTEX LIGHTING *****/
	lightDir = (gl_ModelViewMatrixInverse * gl_LightSource[0].position).xyz; //LIGHT0 is assumed to be the sun, and directional(normalized)
	NdotL = max(dot(gl_Normal, lightDir), 0.0);

	diffuse = gl_FrontMaterial.diffuse.rgb * gl_LightSource[0].diffuse.rgb * NdotL;

	lightDir = (gl_ModelViewMatrixInverse * gl_LightSource[1].position).xyz;
	NdotL = max(dot(gl_Normal, lightDir), 0.0);
	lightAccumColor = gl_FrontMaterial.diffuse.rgb * gl_LightSource[1].diffuse.rgb*NdotL;

	gl_FrontColor = gl_Color;
	
	gl_Position = gl_ProjectionMatrix * ecPosition;
}

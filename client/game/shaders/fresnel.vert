varying vec3 normal;
varying vec3 ecPosition3;
varying float fog;
varying vec4 ambient;

varying vec3 lightDir;

//Big: shadows
varying vec4 shadowCoord;

void main()
{
	float NdotL;
	vec4 color = vec4(0.0);
	
	// transform normal
	normal = normalize(gl_NormalMatrix * gl_Normal);
	
	// pass texture coords
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord2;
	gl_TexCoord[2] = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
	gl_TexCoord[3] = gl_MultiTexCoord3;

	gl_TexCoord[2] = mat4(0.5, 0.0, 0.0, 0.0,
                                0.0, 0.5, 0.0, 0.0,
                                0.0, 0.0, 0.5, 0.0,
                                0.5, 0.5, 0.5, 1.0) * gl_TexCoord[2];

	vec4 ecPosition = gl_ModelViewMatrix * gl_Vertex;
	ecPosition3 = ecPosition.xyz;	

	ambient = gl_LightModel.ambient;

	//calc shadow coord
	shadowCoord = gl_TextureMatrix[1] * ecPosition;
	
	/***** LINEAR FOG *********/
        gl_FogFragCoord = abs(ecPosition3.z);
        fog = (gl_Fog.end - gl_FogFragCoord) * gl_Fog.scale;
        fog = clamp(fog, 0.0, 1.0);

	/***** FIXED-FUNCTION VERTEX LIGHTING *****/
	lightDir = (vec4(gl_LightSource[0].position.xyz,1) * gl_ModelViewMatrixInverse).xyz; //LIGHT0 is assumed to be the sun, and directional(normalized)
	NdotL = max(dot(normal, lightDir), 0.0);

	color.rgb += gl_Color.rgb * gl_LightSource[0].diffuse.rgb * NdotL;

        gl_FrontColor = vec4(color.rgb, gl_Color.a);

	gl_Position = ftransform();
}

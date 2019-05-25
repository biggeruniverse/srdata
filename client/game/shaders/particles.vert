//varying vec3 normal;
varying vec3 ecPosition3;

void main()
{
	vec4 color = vec4(0.0);
	
	// transform normal
	//normal = normalize(gl_NormalMatrix * gl_Normal);
	
	// pass texture coords
	gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	gl_TexCoord[1] = gl_MultiTexCoord1;
	gl_TexCoord[2] = gl_MultiTexCoord2;
	gl_TexCoord[3] = gl_MultiTexCoord3;

	vec4 ecPosition = gl_ModelViewMatrix * gl_Vertex;
	ecPosition3 = ecPosition.xyz;

	color.rgb = gl_Color.rgb;

        gl_FrontColor = vec4(color.rgb, gl_Color.a);
	
	gl_Position = ftransform();
}

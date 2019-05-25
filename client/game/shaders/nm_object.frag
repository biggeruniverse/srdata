//(c) 2012 savagerebirth.com

varying vec4 		lightPos;	// light position 0 in tangent space
varying vec4 		lightPos1;	// light position 1 in tangent space
varying float		fog;
varying vec3 		viewV;
varying vec3		halfVector;
varying vec4		ambient;

uniform sampler2D	texture0; 	// base texture
uniform sampler2D	normalMap; 	// normalmap texture

uniform vec4		ps_pb_cs_hs;	// parallax scale, parallax bias, rgb scale (tex modulate), height scale (for normalmap)

void main()
{
	vec4 color;
	vec4 diffuse = vec4(0.0);
	vec4 specular = vec4(0.0);
	vec3 normal2;
	vec3 lightVector;
	vec4 baseColor;
	vec2 newTexcoord;

	// read height value
	float h = texture2D(normalMap, gl_TexCoord[0].st).a;

	newTexcoord = gl_TexCoord[0].st + (viewV.xy * (h * ps_pb_cs_hs.x + ps_pb_cs_hs.y));		// calculate texcoord based on parallax settings
	
	vec4 normalColor = texture2D(normalMap, newTexcoord);	// read normal fragment
	normalColor = normalColor * 2.0 - 1.0;	// bring the normal in [-1, 1]
	
	normal2 = normalColor.rgb;
	normal2.z *= h * ps_pb_cs_hs.w;		// modulate normal by uniform hscale and heightmap
	normal2 = normalize(normal2);		// normalize
	
	baseColor = texture2D(texture0, newTexcoord) * gl_Color;
	
	float nDotVP=0.0; 	// normal . light direction
	float nDotHV=0.0; 	// normal . light half vector
		
	/********* light 0 ***************/			
	lightVector = lightPos.xyz;
			
	nDotVP = max(0.0, dot(normal2, lightVector));
	
	diffuse += gl_LightSource[0].diffuse * nDotVP;


	/********* light 1 ***************/
	// no ambient for the rim light
	
	nDotVP = max(0.0, dot(normal2, lightPos1.xyz));
	
	diffuse += gl_LightSource[1].diffuse * nDotVP;

	//if (nDotHV > 0.0)
	//	color.rgb += specular.rgb * gl_FrontMaterial.specular.rgb;
	
	color = vec4(baseColor.rgb * (ambient.rgb + diffuse.rgb), baseColor.a);	

	color.rgb *= ps_pb_cs_hs.z;

	// apply linear fog
	color.rgb = mix(gl_Fog.color.rgb, color.rgb, fog);

	gl_FragColor = color;
}

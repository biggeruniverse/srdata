//(c) 2012 savagerebirth.com

varying vec4 		lightPos;	// light position 0 in tangent space
varying vec4 		lightPos1;	// light position 1 in tangent space
varying float		fog;
varying float		rimFactor;
varying vec3 		viewV;
varying vec3		halfVector;
varying vec4		ambient;

uniform sampler2D	texture0; 	// base texture
uniform sampler2D	texture1; 	// clouds texture
uniform sampler2D	normalMap; 	// normalmap texture
uniform sampler2D	glossMap; 	// glossmap texture

uniform vec3		rimColor;
uniform vec4		ps_pb_cs_hs;	// parallax scale, parallax bias, rgb scale (tex modulate), height scale (for normalmap)

void main()
{
	vec4 color;
	vec4 diffuse = vec4(0.0);
	vec4 specular;
	vec3 normal2;
	vec3 lightVector;
	vec4 baseColor;
	vec2 newTexcoord;
		
	float h = texture2D(normalMap, gl_TexCoord[0].st).a;
	newTexcoord = gl_TexCoord[0].st + (viewV.xy * (h * ps_pb_cs_hs.x + ps_pb_cs_hs.y));
	
	vec4 normalColor 	= texture2D(normalMap, newTexcoord);
	normalColor = normalColor * 2.0 - 1.0;

	normal2    = normalColor.xyz;
	normal2.z *= h * ps_pb_cs_hs.w;
	normal2 = normalize(normal2);
	
	baseColor = texture2D(texture0, newTexcoord);
	baseColor *= gl_Color;
	
	float nDotVP=0.0; 	// normal . light direction
	float nDotHV=0.0; 	// normal . light half vector
		
	/********* light 0 ***************/			
	lightVector = lightPos.xyz;

	nDotVP = max(0.0, dot(normal2, lightVector));
		
	diffuse += gl_LightSource[0].diffuse * nDotVP;
				
	nDotHV 	= max(0.0, dot(normal2, normalize(halfVector)));	
	specular = gl_LightSource[0].diffuse * pow(nDotHV, gl_FrontMaterial.shininess);
			
		
	/********* light 1 ***************/
	lightVector = lightPos1.xyz;
			
	nDotVP 	 = max(0.0, dot(normal2, lightVector));
				
	diffuse += gl_LightSource[1].diffuse * nDotVP;
		
	///// END LIGHTS /////		
	color = vec4(baseColor.rgb * (ambient.rgb + diffuse.rgb), baseColor.a);
	color.rgb += texture2D(glossMap, newTexcoord).rgb * specular.rgb * gl_FrontMaterial.specular.rgb;
	color.rgb *= ps_pb_cs_hs.z;

	//color.rgb += ambient.rgb*rimColor*rimFactor*0.4;

	color.rgb = mix(gl_Fog.color.rgb, color.rgb, fog);

	gl_FragColor 	= color;
}

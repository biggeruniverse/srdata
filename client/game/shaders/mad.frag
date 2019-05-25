uniform sampler2D	texture0; 	// base texture

void main()
{
	vec3 lum	= vec3(0.299, 0.587, 0.114);
	vec4 baseColor 	= texture2D(texture0, gl_TexCoord[0].st);

	vec3 color = step(0.2, vec3(dot(lum, baseColor.rgb)));
	
	gl_FragColor 	= vec4(color, 1.0);
}

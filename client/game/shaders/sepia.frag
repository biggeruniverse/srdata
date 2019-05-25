//(c) 2012 savagerebirth.com

uniform sampler2D	texture0; 	// base texture

void main()
{
	vec3 lum	= vec3(0.299, 0.587, 0.114);
	vec4 baseColor 	= texture2D(texture0, gl_TexCoord[0].st);

	vec3 color = clamp(vec3(dot(lum, baseColor.rgb)) * vec3(1.2, 1.0, 0.8), 0.0, 1.0);

	//blacken the edges with an exponetial falloff
	float s = abs(gl_TexCoord[0].s-0.5);
	float sb = 1.0-(s*s);
	float t = abs(gl_TexCoord[0].t-0.5);
	float tb = 1.0-(t*t);
	
	color *= sb*tb;	

	gl_FragColor 	= vec4(color, 1.0);
}

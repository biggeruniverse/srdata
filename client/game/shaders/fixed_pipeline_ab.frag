// (c) 2011 savagerebirth.com

uniform sampler2D	texture0; 	// base texture

void main()
{
	vec4 baseColor 	= texture2D(texture0, gl_TexCoord[0].st);

	gl_FragColor = vec4(baseColor.rgb*gl_Color.rgb*gl_Color.a, baseColor.a*gl_Color.a);
	//gl_FragColor = gl_Color;
}

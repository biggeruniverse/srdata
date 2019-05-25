// (c) 2011 savagerebirth.com

varying float	fog;
varying vec4	ambient;
varying vec3	diffuse;
varying vec3	lightAccumColor;
varying vec3	normal;

uniform sampler2D	texture0; 	// base texture

void main()
{
	vec4 baseColor 	= texture2D(texture0, gl_TexCoord[0].st);

	vec4 color = vec4(baseColor.rgb * (ambient.rgb + diffuse + lightAccumColor) * gl_Color.rgb, baseColor.a*gl_Color.a);

	color.rgb = mix(gl_Fog.color.rgb, color.rgb, fog);

	gl_FragColor    = color;
}

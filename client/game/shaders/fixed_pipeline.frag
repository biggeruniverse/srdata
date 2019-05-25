// (c) 2012 savagerebirth.com

varying float		fog;
varying vec4		ambient;
varying vec3		diffuse;
varying vec3		lightAccumColor;

varying vec4		ecPosition;

uniform sampler2D	texture0; 	// base texture

void main()
{
	vec4 color		= vec4(0.0);
        float diffuseMod	= 1.0;
	vec4 baseColor 		= texture2D(texture0, gl_TexCoord[0].st);

	if(baseColor.a*gl_Color.a < 0.05)
		discard;

	color = vec4(baseColor.rgb * (ambient.rgb + (diffuse*diffuseMod) + lightAccumColor)*gl_Color.rgb, baseColor.a*gl_Color.a);

	color.rgb = mix(gl_Fog.color.rgb, color.rgb, fog);
	
	gl_FragColor 	= color;
}

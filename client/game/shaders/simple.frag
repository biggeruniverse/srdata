//(c) 2012 savagerebirth.com

uniform sampler2D       texture0;       // base texture
uniform vec3		rimColor;

varying float		fog;
varying float        	rimFactor;
varying vec3		lightAccumColor;
varying vec3		diffuse;
varying vec4		ambient;

void main()
{
	vec4 baseColor	= texture2D(texture0, gl_TexCoord[0].st);

	gl_FragColor	  = gl_Color * baseColor;
	gl_FragColor.rgb *= (diffuse+ambient.rgb+lightAccumColor);
	gl_FragColor.rgb += ambient.rgb*rimColor*rimFactor*.4;

	gl_FragColor.rgb = mix(gl_Fog.color.rgb, gl_FragColor.rgb, fog);
}

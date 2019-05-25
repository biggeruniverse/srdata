//(c) 2012 savagerebirth.com

uniform float		bloomMix;
uniform sampler2D       texture0;       // base texture
uniform sampler2D       texture1;       // SSAO
uniform sampler2D       texture2;       // bloom

vec4 toSRGB(in vec4 c) {
        float y=1.0/2.2;
        return vec4(pow(c.rgb, vec3(y)), c.a);
}

void main()
{

        vec4 baseColor          = texture2D(texture0, gl_TexCoord[0].st);
        vec4 aomix              = texture2D(texture1, gl_TexCoord[0].st);
        vec4 bloom              = texture2D(texture2, gl_TexCoord[0].st);

	//gl_FragColor 	 = toSRGB(vec4(baseColor.rgb*aomix.rgb + gl_Color.rgb, 1.0));
	gl_FragColor 	 = vec4(baseColor.rgb*aomix.rgb + gl_Color.rgb, 1.0);
	gl_FragColor.rgb += bloom.rgb*bloomMix;
	//gl_FragColor.rgb = baseColor.rgb + gl_Color.rgb;
	//gl_FragColor.rgb *= aomix.rgb;
}

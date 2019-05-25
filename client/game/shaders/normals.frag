//(c) 2012 savagerebirth.com

varying vec3 normal;

uniform sampler2D       texture0;       // base texture

void main()
{
        vec4 baseColor          = texture2D(texture0, gl_TexCoord[0].st);

	if(baseColor.a*gl_Color.a < 0.5)
		discard;

        gl_FragColor = vec4(normal, gl_FragCoord.z);
	//gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}

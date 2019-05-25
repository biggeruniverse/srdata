#version 120
uniform sampler2D texture0; // base texture

// Invert Color filter?

void main()
{
        vec4 baseColor = texture2D(texture0, gl_TexCoord[0].st);
        vec3 white = vec3(1.0, 1.0, 1.0 );

        vec3 color = white - baseColor.rgb;
        gl_FragColor = vec4(color, 1.0);
}


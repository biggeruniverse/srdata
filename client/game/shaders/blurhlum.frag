//(c) 2012 savagerebirth.com
#version 130

#include "shaders/blurs.glsl"

uniform sampler2D	texture0; 	// base texture

out vec4 fragColor;

void main()
{

	fragColor = vec4(hblurlum(texture0, gl_TexCoord[0].st, .55), gl_Color.a);
}

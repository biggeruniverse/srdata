// (c) 2012 savagerebirth.com
#version 130

uniform sampler2DArray texture0;

void main(void)
{
	float zFar = 4500;
	float zNear = 2.0;
	float depth = (zNear * zNear) / (zFar + zNear - texture(texture0, vec3(gl_TexCoord[0].st,2.0) ).r * (zFar-zNear));
	//float depth = texture(texture0, vec3(gl_TexCoord[0].st, 0.0)).r;

	gl_FragColor = vec4(depth,depth,depth, 1.0);
}

void main()
{
	// pass texture coords
        gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	//pass color
	gl_FrontColor = vec4(1,0,0,1);
	// just transform vertex	
	gl_Position = ftransform();
}

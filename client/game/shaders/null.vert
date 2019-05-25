// (c) 2011 savagerebirth.com

void main()
{
	// pass texture coords
        gl_TexCoord[0] = gl_TextureMatrix[0] * gl_MultiTexCoord0;
	//pass color
	gl_FrontColor = gl_FrontMaterial.diffuse*gl_Color;
	// just transform vertex	
	gl_Position = ftransform();
}

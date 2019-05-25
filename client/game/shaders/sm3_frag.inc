// (c) 2012 savagerebirth.com
//For shaders declaring GLSL 130+

struct gl_MaterialParameters {
    vec4 emission;
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    float shininess;
};

struct gl_FogParameters {
    vec4 color;
    float density;
    float start;
    float end;
    float scale;
};

struct gl_LightSourceParameters {
    vec4 ambient;
    vec4 diffuse;
    vec4 specular;
    vec4 position;
    vec4 halfVector;
    vec3 spotDirection;
    float spotExponent;
    float spotCutoff;
    float spotCosCutoff;
    float constantAttenuation;
    float linearAttenuation;
    float quadraticAttenuation;
};

uniform		gl_MaterialParameters gl_FrontMaterial;
uniform		gl_MaterialParameters gl_BackMaterial;
uniform		gl_FogParameters gl_Fog;
uniform		gl_LightSourceParameters gl_LightSource[gl_MaxLights];
uniform mat3	gl_NormalMatrix;
uniform mat4	gl_TextureMatrix[gl_MaxTextureCoords];
uniform vec4	gl_Color;
uniform vec4	gl_SecondaryColor;
uniform vec4	gl_TexCoord[gl_MaxTextureCoords];

out vec4	gl_FragColor;


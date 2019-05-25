#(c) 2011 savagerebirth.com

import glass

class DefaultImage(DefaultWidget, glass.GlassLabel):
    def __init__(self):
        glass.GlassLabel.__init__(self);
        DefaultWidget.__init__(self);
        self.setFocusable(0);
        
    # type: 
    #    None = imagePath + src
    #    'default' = defaultImagePath + src
    #    else = src
    def setImage(self, src, type=None, lazy=0):

        if type is None: 
            src = self.imagePath + src;
        elif type == "default":
            src = self.defaultImagePath + src;
        elif type == "gui":
            src = "/gui/" + src;

        glass.GlassLabel.setImage(self, src, lazy);

    def scale(self, s):
        self.setSize(int(self.getWidth()*s), int(self.getHeight()*s));


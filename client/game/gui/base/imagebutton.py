#(c) 2011 savagerebirth.com

import glass

class DefaultImageButton(DefaultWidget, glass.ImageButton):
    def __init__(self):
        glass.ImageButton.__init__(self);
        DefaultWidget.__init__(self);
        
    # type: 
    #    None = imagePath + src
    #    'default' = defaultImagePath + src
    #    else = src
    def setImage(self, src, type=None):

        if type is None: 
            src = self.imagePath + src;
        elif type == "default":
            src = self.defaultImagePath + src;

        glass.ImageButton.setImage(self, src);
#(c) 2011 savagerebirth.com

# This is a simple wrapper to make adding icons less repetetive
# DefaultIcon("options"); instead of DefaultImageButton("/gui/path/icons/options.png"); setSize() 

import glass

class MainIcon(DefaultImageButton):
    def __init__(self, icon, width=21, height=21, ext="png"):
        DefaultImageButton.__init__(self);
        
        self.extension = ext;
        
        self.setImage("icons/" + icon + "." + ext);
        self.setSize(width, height);
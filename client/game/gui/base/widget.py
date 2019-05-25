#(c) 2011 savagerebirth.com

import glass

# TODO: put this in defines, here while I dev as repo updates will overwrite everything but the gui folder
#ApiUrl = "projects/SR-Website/api/index.php";#"test.savagerebirth.com/api";
ApiUrl = "savagerebirth.com/api";

class DefaultWidget(glass.GlassWidget):
    
    def __init__(self):
        
        glass.GlassWidget.__init__(self);
        
        self.defaultImagePath = "/gui/default/images/";
        # designed to be overwritten by other themes
        self.imagePath = "/gui/main/images/";

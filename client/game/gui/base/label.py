#(c) 2011 savagerebirth.com

import glass

class DefaultLabel(glass.GlassLabel):
    
    def __init__(self, string=""):
        glass.GlassLabel.__init__(self, string);
        self.adjustSize();

    def setCaption(self, string):
        glass.GlassLabel.setCaption(self, string);
        self.adjustSize();
        
    def setFont(self, font):
        glass.GlassLabel.setFont(self, font);
        self.adjustSize();
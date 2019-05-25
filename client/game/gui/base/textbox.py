#(c) 2011 savagerebirth.com

import glass

class DefaultTextBox(glass.GlassTextBox):
    
    def __init__(self, label=""):
        glass.GlassTextBox.__init__(self, label);
        self.setLineWrap(1);
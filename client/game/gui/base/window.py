#(c) 2011 savagerebirth.com

import glass

class DefaultWindow(glass.GlassWindow, DefaultContainer):
    
    def __init__(self, label=""):
        glass.GlassWindow.__init__(self, label);
        DefaultContainer.__init__(self);
        self.setTitleVisible(0);
        self.setFrameStyle("Eight");
        
    def add(self, obj, x=None, y=None, alignX="left", alignY="top"):
       
        if x is None:
            x = obj.getX();
 
        if y is None:
            y = obj.getY();
 
        if isinstance(x, str):
            alignX = x;
            x = 0;
            
        if isinstance(y, str):
            alignY = y;
            y = 0;            
        
        if alignX == "right":
            x = self.getWidth() - obj.getWidth() - x;
        elif alignX == "center":
            x += (self.getWidth() // 2 - obj.getWidth() // 2);
        
        if alignY == "bottom":
            y = self.getHeight() - obj.getHeight() - y;
        elif alignY == "center":
            y += (self.getHeight() // 2 - obj.getHeight() // 2);
        
        return glass.GlassWindow.add(self, obj, x, y);

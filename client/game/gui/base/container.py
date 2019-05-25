#(c) 2011 savagerebirth.com

import glass

class DefaultContainer(glass.GlassContainer):
    def __init__(self):
        glass.GlassContainer.__init__(self);
        self.widgets = []
        
    def add(self, obj, x=0, y=0, alignX="left", alignY="top"):
        
        try: x, y, alignX, alignY = obj.beforeAdd(self, x, y, alignX, alignY)
        except: pass
        
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
        
        glass.GlassContainer.add(self, obj, x, y);
        self.widgets.append(obj)
    
        try: obj.afterAdd(self)
        except: pass

    def fit(self):
        width = 0
        height = 0

        for w in self.widgets:
            width = max(width, w.getX() + w.getWidth())
            height = max(height, w.getY() + w.getHeight())


        self.setSize(width, height)

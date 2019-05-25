# (c) 2012 savagerebirth.com

# this is called a widget but as reference to a big container working as a single unit, 
# so we inherit from a container
"""
DoF: Only use them for widgets that are added directly to the screen, not onto other windows.
     Also, initialize + add them in commhud.py and not inside the widget file, we'd like
     to keep some kind of overiew!
"""

class CommAbstractWidget(DefaultContainer):
    def __init__(self):
        DefaultContainer.__init__(self);
        self.initialized = False;
        self.alwaysUpdate = False;
        
    def create(self):
        raise NotImplementedError("create needs to be defined");

    def frame(self):
        pass;
    
    def rebuild(self):
        pass;



class AbstractSection(DefaultWindow):
    
    def __init__(self):
        DefaultWindow.__init__(self);
        self.initialized = False;
        self.setFrameStyle("TrimmedEight");
        
    def create(self):
        raise NotImplementedError("create needs to be defined"); 
            
    def setVisible(self, visible):
        if visible:
            self._create();
            
        DefaultWindow.setVisible(self, visible);
        
    def _create(self):
        if self.initialized == False:
            self.create();
            self.initialized = True;
        
    def onShow(self):
        pass;
    
    def onHide(self):
        pass;
    
    def frame(self):
        pass;

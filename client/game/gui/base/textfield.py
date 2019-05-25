#(c) 2011 savagerebirth.com

import glass

# TODO: font and size place holders

class DefaultTextField(glass.GlassTextField):
    
    def __init__(self, label=""):
        
        glass.GlassTextField.__init__(self, label);
        
        self.placeHolder = None;
        self.oldText = None;
        
        # TODO:
        #self.placeHolderColor = None;
        #self.placeHolderFont = None;
        #self.placeHolderSize = None;
        #self.oldColor = None;
        #self.oldFont = None;
        #self.oldSize = None;
        
        self.addFocusListener(self);
        
    def setPlaceHolder(self, string):
        self.placeHolder = string;
        #self.enablePlaceHolder();
        
    def getPlaceHolder(self):
        return self.placeHolder;
    
    def focusLost(self, e):
        con_println("ZING2!\n");
        if e.widget.getText() == "" and self.placeHolder is not None:
            self.enabledPlaceHolder();
            
    def focusGained(self, e):
        con_println("ZING!\n");
        if e.widget.getText() == self.placeHolder:
            self.disablePlaceHolder();
        
            
    def enablePlaceHolder(self):
        #self.oldColor = self.getForegroundColor();
        #self.oldFont = self.getFont();
        #self.oldSize = self
        
        #if self.placeHolderColor is not None:
        #    self.setColor(self.placeHolderColor);
        
        self.oldText = self.getText();
        
        self.setText(self.placeHolder);
        
    def disablePlaceHolder(self):
        #self.setColor = self.oldColor;
        self.setText = self.oldText;
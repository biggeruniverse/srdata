# (c) 2010 savagerebirth.com

import glass;

class DefaultAlert(DefaultWindow):

    def __init__(self, alertMessage, okAction=None, okLabel="Ok"):

        DefaultWindow.__init__(self, "Alert");
        
        self.setBackgroundColor(glass.Color(0, 0, 0, 191));
        
        width = 350;
        # add padding and border manually
        self.padding = 10;
        self.border = 5;
        self.setPadding(0);
        self.setWidth(width + self.padding * 2 + self.border * 2);
        self.centerWindow();
        self.setY(self.getY() - 190);
        self.setBackgroundColor(glass.Color(0, 0, 0, 191));
        self.setVisible(0);
    
        self.msg = DefaultTextBox();
        self.msg.setForegroundColor(glass.Color(238, 238, 238));
        self.msg.setOpaque(0);
        self.msg.setFocusable(0);
        self.msg.setSize(width, self.msg.getHeight());
        self.msg.setText(alertMessage);
        #self.msg.setAlignment(glass.Graphics.CENTER);
        self.add(self.msg);
        
        self.ok = DefaultButton(okLabel);
        self.ok.setSize(80, 30);
        if okAction is not None:
            self.ok.setClickAction(okAction);
        self.ok.addActionListener(self);
        self.add(self.ok, "center", self.msg.getHeight() + 15);
        
        self.hr = DefaultLabel("");
        self.hr.setBackgroundColor(glass.Color(255, 255, 255, 100));
        self.hr.setSize(width, 1);
        self.hr.setOpaque(1);
        self.add(self.hr, 0, self.msg.getHeight() + 5);
        
        self.setHeight(self.msg.getHeight() + self.ok.getHeight() + 15 + self.padding * 2 + self.border * 2);
        
        self.addTempHackyBorder();
        
    def resize(self):
        self.hr.setY(self.msg.getHeight() + 5 + self.padding + self.border);
        self.ok.setY(self.msg.getHeight() + 15 + self.padding + self.border);
        self.setHeight(self.msg.getHeight() + self.ok.getHeight() + 15 + self.padding * 2 + self.border * 2);
        self.borderObjs[2].setY(self.getHeight() - self.border);
        
    def addTempHackyBorder(self):
        
        color = glass.Color(0, 0, 0, 100);
        
        top = DefaultLabel();
        top.setSize(self.getWidth(), self.border);
        top.setOpaque(1);
        top.setBackgroundColor(color);
        self.add(top, 0, 0, "left", "top", True);
        
        right = DefaultLabel();
        right.setSize(self.border, self.getHeight() - self.border * 2);
        right.setOpaque(1);
        right.setBackgroundColor(color);
        self.add(right, 0, self.border, "right", "top", True);
        
        bottom = DefaultLabel();
        bottom.setSize(self.getWidth(), self.border);
        bottom.setOpaque(1);
        bottom.setBackgroundColor(color);
        self.add(bottom, 0, 0, "left", "bottom", True);
        
        left = DefaultLabel();
        left.setSize(self.border, self.getHeight() - self.border * 2);
        left.setOpaque(1);
        left.setBackgroundColor(color);
        self.add(left, 0, self.border, "left", "top", True);
        
        self.borderObjs = [top, right, bottom, left];
        
    def add(self, obj, x=0, y=0, alignX="left", alignY="top", ignore=False):
        if isinstance(x, str):
            alignX = x;
            x = 0;
            
        if isinstance(y, str):
            alignY = y;
            y = 0;
        
        if ignore != True:
            x += self.padding + self.border;
            y += self.padding + self.border;
        DefaultWindow.add(self, obj, x, y, alignX, alignY);
        
    def onAction(self, e):
        if e.widget.getCaption() == self.ok.getCaption():
            import mainmenu;
            self.setVisible(0);
            
    def setVisible(self, visible):        
        if self.getParent() is not None and visible == 1:
            self.getParent().moveToTop(self);
            self.resize();
        DefaultWindow.setVisible(self, visible);
        #import mainmenu;
        #mainmenu.fade(visible);
        
        if visible == 1:
            self.requestModalFocus();
        else:
            self.releaseModalFocus();
# (c) 2011 savagerebirth.com

import glass

# NOTE: using ImageButton for now since Nine is broken
class DefaultButton(glass.GlassButton):#glass.GlassNinePatchButton):
    def __init__(self, label):
        glass.GlassButton.__init__(self, label);#GlassNinePatchButton.__init__(self, label);
        self.setForegroundColor(themeGold);
        self.setAlignment(glass.Graphics.CENTER);
        self.setSpacing(0);
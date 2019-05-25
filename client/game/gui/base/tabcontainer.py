#(c) 2011 savagerebirth.com

import glass

class DefaultTabContainer(glass.GlassTabbedContainer):
    
    def __init__(self):
        glass.GlassTabbedContainer.__init__(self);
        
    def addTab(self, tab, widget):
        #if isinstance(tab, (str,unicode)):
         #   tab = DefaultButton(tab);
            
        glass.GlassTabbedContainer.addTab(self, tab, widget);

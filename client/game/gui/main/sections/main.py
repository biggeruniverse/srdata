# (c) 2011 savagerebirth.com

import mainmenu

class MainSection(AbstractSection):
    
    def __init__(self):
        AbstractSection.__init__(self);
        
    def create(self):
        pass;

#TODO
mainmenu.modules["menu"].addSection("main", MainSection());

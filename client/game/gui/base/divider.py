#(c) 2012 savagerebirth.com

import glass

class DefaultDivider(DefaultImage):
	def __init__(self):
		DefaultImage.__init__(self);
		self.setFocusable(0);
		self.setImage("divider.png");
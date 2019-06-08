# (c) 2011 savagerebirth.com
#scales a widget at a given rate to a given size

class ScaleAction(GuiAction):
	def __init__(self, widget, destw, desth, rate=.05):
		GuiAction.__init__(self, widget);
		self.initw = widget.getWidth();
		self.inith = widget.getHeight();
		self.destw = destw;
		self.desth = desth;
		self.widget = widget;
		self.lerp = 0;
		self.rate = rate;
	
	def run(self):
		self.lerp += self.rate*self.rateMult();
		if self.lerp > 1:
			self.lerp=1;
		w = self.initw + (self.destw - self.initw)*self.lerp;
		h = self.inith + (self.desth - self.inith)*self.lerp;
		self.widget.setSize(int(w), int(h));
	
	def is_done(self):
		return self.lerp >= 1;


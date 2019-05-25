# (c) 2011 savagerebirth.com

class SlideAction(GuiAction):
	def __init__(self, widget, destx, desty, rate=.05):
		self.initx = widget.getX();
		self.inity = widget.getY();
		self.destx = destx;
		self.desty = desty;
		self.widget = widget;
		self.lerp = 0;
		self.rate = rate;
		return GuiAction.__init__(self, widget);

	def run(self):
		self.lerp += self.rate*self.rateMult();
		if self.lerp > 1:
			self.lerp=1;
		x = self.lerp*self.destx + (1-self.lerp)*self.initx;
		y = self.lerp*self.desty + (1-self.lerp)*self.inity;
		self.widget.setX(int(x));
		self.widget.setY(int(y));

	def isDone(self):
		return self.lerp >= 1;

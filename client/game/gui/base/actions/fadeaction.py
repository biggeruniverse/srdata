# (c) 2011 savagerebirth.com

class FadeInAction(Action):
	def __init__(self, widget,step = 12, target=255):
		if step <= 0:
			raise ValueError("argument step must be a positive integer");
		if not 0 <= target <= 255:
			raise ValueError("argument target must lie in [0,255]");
		self.widget = widget;
		self.step = int(step);
		#never trust the user input
		self.target = target;
		return Action.__init__(self);

	def run(self):
		self.widget.setVisible(1);
		self.widget.setAlpha( int(min( self.widget.getAlpha() + self.step , self.target)) );

	def isDone(self):
		return self.widget.getAlpha() >= self.target;

class FadeOutAction(Action):
	def __init__(self, widget,step = 12, target=0):
		if step <= 0:
			raise ValueError("argument step must be a positive integer");
		if not 0 <= target <= 255:
			raise ValueError("argument target must lie in [0,255]")
		self.widget = widget;
		self.step = int(step);
		#never trust the user input
		self.target = target;
		return Action.__init__(self);

	def run(self):
		self.widget.setVisible(1);
		self.widget.setAlpha( int(max( self.widget.getAlpha() - self.step , self.target)) );

	def isDone(self):
		if self.widget.getAlpha() <= self.target:
			self.widget.setVisible(0);
			return True;
		return False;


# (c) 2011 savagerebirth.com
import silverback

class FadeInAction(silverback.Action):
	def __init__(self, widget,step = 12, target=255):
		if step <= 0:
			raise ValueError("argument step must be a positive integer");
		if not 0 <= target <= 255:
			raise ValueError("argument target must lie in [0,255]");
		self.widget = widget;
		self.step = int(step);
		#never trust the user input
		self.target = target;
		return silverback.Action.__init__(self);

	def run(self):
		self.widget.setVisible(True);
		self.widget.setAlpha( int(min( self.widget.getAlpha() + self.step , self.target)) );

	def is_done(self):
		return self.widget.getAlpha() >= self.target;

class FadeOutAction(silverback.Action):
	def __init__(self, widget,step = 12, target=0):
		if step <= 0:
			raise ValueError("argument step must be a positive integer");
		if not 0 <= target <= 255:
			raise ValueError("argument target must lie in [0,255]")
		self.widget = widget;
		self.step = int(step);
		#never trust the user input
		self.target = target;
		return silverback.Action.__init__(self);

	def run(self):
		self.widget.setVisible(True);
		self.widget.setAlpha( int(max( self.widget.getAlpha() - self.step , self.target)) );

	def is_done(self):
		if self.widget.getAlpha() <= self.target:
			self.widget.setVisible(False);
			return True;
		return False;


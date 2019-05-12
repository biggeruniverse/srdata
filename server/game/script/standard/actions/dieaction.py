# (c) 2011 savagerebirth.com

class DieAction(Action):
	def __init__(self, obj):
		self.obj = obj;
		return Action.__init__(self);

	def run(self):
		self.obj.die();


# (c) 2011 savagerebirth.com

class CallAction(Action):
	def __init__(self, funcobj, args):
		Action.__init__(self);
		self.func = funcobj;
		self.args = args;

	def run(self):
		self.func(args);

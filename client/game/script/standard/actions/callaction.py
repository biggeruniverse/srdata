# (c) 2011 savagerebirth.com

#is_done by default returns True, which is what we want here

class CallAction(Action):
	def __init__(self, funcobj, args):
		Action.__init__(self);
		self.func = funcobj;
		self.args = args;

	def run(self):
		self.func(*self.args)

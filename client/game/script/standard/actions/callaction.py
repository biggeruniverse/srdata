# (c) 2011 savagerebirth.com

#is_done by default returns True, which is what we want here

class CallAction(Action):
	def __init__(self, funcobj, args=tuple([])):
		self.func = funcobj;
		self.args = args;
		super().__init__()

	def run(self):
		self.func(*self.args)

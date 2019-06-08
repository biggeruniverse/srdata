# (c) 2011 savagerebirth.com

from silverback import *

class WaitAction(Action):
	def __init__(self, time):
		self.duration = time
		self.until = 0
		super().__init__()

	def reset(self):
		self.until = self.duration + Host_Milliseconds()

	def run(self):
		#stacklesslib.main._sleep(0.005)
		pass

	def is_done(self):
		if self.until >= Host_Milliseconds():
			return False
		return True


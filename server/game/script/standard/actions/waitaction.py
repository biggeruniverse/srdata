# (c) 2011 savagerebirth.com

from silverback import *
import stacklesslib

class WaitAction(Action):
	def __init__(self, time):
		self.until = time + Host_Milliseconds()
		return Action.__init__(self)

	def run(self):
		stacklesslib.main.sleep(0.005)

	def isDone(self):
		if self.until >= Host_Milliseconds():
			return False
		return True


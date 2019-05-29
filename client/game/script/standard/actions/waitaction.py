# (c) 2011 savagerebirth.com

from silverback import *
import stacklesslib

class WaitAction(Action):
	def __init__(self, time):
		con_println("setting time\n")
		self.until = time + Host_Milliseconds()
		return Action.__init__(self)

	def run(self):
		con_println("run!\n")
		stacklesslib.main._sleep(0.005)

	def isDone(self):
		con_println("checking if done...\n")
		if self.until >= Host_Milliseconds():
			return False
		con_println("yes!")
		return True


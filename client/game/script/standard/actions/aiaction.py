# (c) 2011 savagerebirth.com

from silverback import *;

class AIAction(Action):
	def __init__(self, m):
		self.mind = m;
		return Action.__init__(self);

	def run(self):
		self.mind.update();

	def isDone(self):
		return False;


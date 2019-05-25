#(c) 2011 savagerebirth.com
# this is a basic action outline, actions extend from this

from silverback import con_dprintln;

class Action:
	def __init__(self):
		self.parent = None;
		

	def setParent(self, seq):
		self.parent = seq;

	def run(self):
		con_dprintln("Action.run()\n");

	def isDone(self):
		return True;

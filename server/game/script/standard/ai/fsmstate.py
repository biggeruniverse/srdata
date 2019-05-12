# (c) 2011 savagerebirth.com

#interface class for FSM states

class FSMState:
	def __init__(self):
		self.machine = None;
		self.targetObject = None;

	def run(self):
		pass;

	def isComplete(self):
		return True;

	def canTransition(self, s):
		return False;


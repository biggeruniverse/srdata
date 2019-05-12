#(c) 2011 savagerebirth.com

class FiniteStateMachine:
	import logging
	logger = logging.getLogger("savage.ai.fsm")
	def __init__(self, ghost):
		self.states = [];
		self.mind = ghost;
		self.insertState(savage.IdleState());

	def getState(self):
		if len(self.states) == 0:
			return AISTATE_NONE;
		return self.states[0].getType();

	def insertState(self, st):
		st.machine = self;
		self.states.insert(0, st);

	def addState(self, st):
		st.machine = self;
		self.states.append(st);

	def reset(self):
		self.states = [];
		self.insertState(savage.IdleState());
		
	def clear(self):
		self.states = [];

	def evaluate(self):
		if len(self.states) == 0:
			return;

		if not self.states[0].isComplete():
			self.states[0].run();
		else:
			if not self.states[0].canTransition(self.states[1]):
				#raise RuntimeException();
				self.logger.error("Invalid state transition! ("+str(self.states[0])+"->"+str(self.states[1])+")\n");
				self.reset();
			else:
				self.states.pop(0);
				# one state left means we're idling (goal completed)
				if len(self.states) == 1:
                                        self.mind.goalReached()


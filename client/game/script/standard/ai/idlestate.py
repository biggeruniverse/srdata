# (c) 2011 savagerebirth.com

class IdleState(savage.FSMState):
	def __init__(self):
		savage.FSMState.__init__(self);

	def run(self):
		go = self.machine.mind;
		go.stopMoving();
		if go.getPrimaryAnimState() != AnimStates.AS_IDLE:
			go.setPrimaryAnimState(AnimStates.AS_IDLE);

	def isComplete(self):
		return False;

	def canTransition(self, s):
		return True;


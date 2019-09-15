# (c) 2011 savagerebirth.com

from silverback import *;
from vectors import Vec3;

class GoState(savage.FSMState):
	def __init__(self, pos):
		savage.FSMState.__init__(self);
		self.destination = Vec3(pos);
		self.nav = savage.StateNavigation()

	def run(self):
		go = self.machine.mind;

		if self.nav.run(go):
			self.machine.mind.gotoPosition(self.destination);

	def isComplete(self):
		go = self.machine.mind
		if self.nav.blocked:
                        return False;
		if not self.nav.firstRun and go.isArrived():
			return True;
		return False;

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True;
		if isinstance(s, savage.ChaseState):
			return True;

		if isinstance(s, savage.GoState):
			return True;
		return False;

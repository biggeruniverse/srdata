# (c) 2011 savagerebirth.com
#
# Evade is not the same as follow, chase implies that afterwards we will attack!
# Thus, we only need to get within the range specified and then we quit. When 
# following, we are basically always going to try to get close to the target 
# until someone stops us.

from vectors import Vec3;

class EvadeState(savage.FSMState):
	def __init__(self, o, d):
		savage.FSMState.__init__(self);
		self.targetObject = o;
		self.evadeDist = d
		self.nav = savage.StateNavigation()

	def run(self):
		go = self.machine.mind;

		if self.nav.run(go):
			o = savage.Vec3(self.targetObject.getPosition())
			p = savage.Vec3(go.getPosition())
			t = p - o
			t.data[2] = 0.0
			t = t.normalise() * self.evadeDist
			t = o + t
			if t.distanceSqTo(o) < p.distanceSqTo(o):
				t = p
			go.gotoPosition(t);

	def isComplete(self):
		go = self.machine.mind
		if self.nav.blocked:
			return False;
		if self.targetObject == None or self.targetObject.getHealth() <= 0 or not self.targetObject.isActive():
			return True;
		if not self.nav.firstRun and go.isArrived():
			return True;
		return False;

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True;
		if isinstance(s, savage.AttackState):
			return True;
		if isinstance(s, savage.ConstructState):
			return True;

		if isinstance(s, savage.ReturnState):
			return True;
		#if isinstance(s, RoamState):
		#	return True;
		return False;


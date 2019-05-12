# (c) 2011 savagerebirth.com
#
# Quick and dirty follow

from vectors import Vec3;

class FollowState(savage.FSMState):
	def __init__(self, o):
		savage.FSMState.__init__(self);
		self.targetObject = o;
		self.nav = savage.StateNavigation()
		self.arrived = False

	def run(self):                
		go = self.machine.mind;
		
		if self.nav.run(go):
			self.arrived = go.gotoObject(self.targetObject);

	def isComplete(self):
		go = self.machine.mind;

		if self.targetObject == None or self.targetObject.getHealth() <= 0 or not self.targetObject.isActive():
			go.stopMoving();
			return True;
		
		return self.arrived;

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True;
		if isinstance(s, savage.AttackState):
			return True;
		if isinstance(s, savage.ConstructState):
			return True;
		if isinstance(s, savage.MineState):
			return True;
		if isinstance(s, savage.ReturnState):
			return True;
		if isinstance(s, savage.DropoffState):
                        return True;
		#if isinstance(s, RoamState):
		#	return True;
		return False;


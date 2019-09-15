# (c) 2011 savagerebirth.com
#
# Chase is not the same as follow, chase implies that afterwards we will attack!
# Thus, we only need to get within the range specified and then we quit. When 
# following, we are basically always going to try to get close to the target 
# until someone stops us.

from vectors import Vec3;

class ChaseState(savage.FSMState):
	def __init__(self, o, d):
		savage.FSMState.__init__(self);
		self.targetObject = o;
		self.chaseDist = d
		self.nav = savage.StateNavigation()
		self.arrived = False

	def run(self):		
		go = self.machine.mind;
		
		if self.nav.run(go):
			self.arrived = go.gotoObject(self.targetObject);

	def isComplete(self):
		go = self.machine.mind;

		if self.nav.blocked:
			return False;
		
		if self.targetObject == None or self.targetObject.getHealth() <= 0 or not self.targetObject.isActive():
			go.stopMoving();
			return True;

		if not self.nav.firstRun and go.isArrived():
			go.stopMoving();
			return True
		
		p = Vec3(self.targetObject.getPosition());
		o = Vec3(go.getPosition());
		dist = self.chaseDist;
		if dist < 0:
			dist = go.getType().getAttackTypeValue("melee_1", "range");
		dist = dist ** 2;

		if o.distanceSqTo(p) <= dist:
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


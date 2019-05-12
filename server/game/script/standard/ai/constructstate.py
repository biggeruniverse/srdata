# (c) 2011 savagerebirth.com
from vectors import Vec3;

class ConstructState(savage.FSMState):
	def __init__(self, o):
		savage.FSMState.__init__(self);
		self.attackTime = 0;
		self.targetObject = o;

	def run(self):
		go = self.machine.mind;
		gotype = go.getType();

		#check if target is out of range, if so
		#insert a chase state into the mind and exit
		r = gotype.getAttackTypeValue("melee_1", "range") ** 2;
		p = Vec3(go.getPosition());
		o = Vec3(self.targetObject.getPosition());
		
		if go.getPrimaryAnimState() != AnimStates.AS_CONSTRUCT:
			self.attackTime = savage.getGameTime()+gotype.getAttackTypeValue("melee_1", "impact");
			#go.setPrimaryAnimState(AnimStates.AS_IDLE);
			go.setPrimaryAnimState(AnimStates.AS_CONSTRUCT);

		if go.getPrimaryAnimState() == AnimStates.AS_CONSTRUCT:
			go.setForwardVector( o - p );
			#make the attack
			if self.attackTime <= savage.getGameTime():
				go.damage(self.targetObject, gotype.getAttackTypeValue("melee_1", "damage"));
				self.attackTime = savage.getGameTime() + gotype.getAttackTypeValue("melee_1", "time");
				#go.setPrimaryAnimState(AnimStates.AS_MELEE_1);

	def isComplete(self):
		go = self.machine.mind;
		if self.targetObject == None or not self.targetObject.isBeingBuilt():
			go.setPrimaryAnimState(AnimStates.AS_IDLE);
			return True;
		return False;

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True;
		if isinstance(s, savage.ChaseState):
			return True;
		if isinstance(s, savage.MineState):
			return True;
		if isinstance(s, savage.GoState):
			return True;
		if isinstance(s, savage.ConstructState):
			return True;

		if isinstance(s, savage.ReturnState):
			return True;
		#if isinstance(s, RoamState):
		#	return True;
		return False;


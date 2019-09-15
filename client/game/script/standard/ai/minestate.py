# (c) 2011 savagerebirth.com
from vectors import Vec3;

class MineState(savage.FSMState):
	def __init__(self, o):
		savage.FSMState.__init__(self)
		self.attackTime = 0;
		self.targetObject = o;
		self.maxCapacity = False

	def run(self):
		go = self.machine.mind;
		gotype = go.getType();

		#check if target is out of range, if so
		#insert a chase state into the mind and exit
		#r = gotype.getAttackTypeValue("melee_1", "range") ** 2;
		p = Vec3(go.getPosition());
		o = Vec3(self.targetObject.getPosition());

		#are we ready to mine, or should we return?
		mineType = self.targetObject.getType().getValue("mineType");
		if go.getCarryResource(mineType) >= go.getMaxCarryResource(mineType):
			#go.setCurrentGoalPriority(9001); #reset mining priority so we never randomly forget we were mining...
			go.fsm.insertState(savage.MineState(self.targetObject))
			go.fsm.insertState(savage.ChaseState(self.targetObject, self.targetObject.getType().getValue("proximity")))
			dropoff = go.findClosestDropPoint()
			go.fsm.insertState(savage.DropoffState(dropoff))
			go.fsm.insertState(savage.ChaseState(dropoff, dropoff.getType().getValue("proximity")));
			self.maxCapacity = True
			return;

		#are we close enough to the mine?
		#if o.distanceSqTo(p)-self.targetObject.getRadiusSq() > r:
		#	self.attackTime = 0;
		#	go.fsm.insertState(savage.ChaseState(self.targetObject, 100));
		#	return;

		if go.getPrimaryAnimState() != AnimStates.AS_MINE:
			self.attackTime = savage.getGameTime()+gotype.getAttackTypeValue("melee_1", "impact");
			#go.setPrimaryAnimState(AnimStates.AS_IDLE);
			go.setPrimaryAnimState(AnimStates.AS_MINE);

		if go.getPrimaryAnimState() == AnimStates.AS_MINE:
			go.setForwardVector( o - p );
			#make the attack
			if self.attackTime <= savage.getGameTime():
				go.mineResources(self.targetObject)
				self.attackTime = savage.getGameTime() + gotype.getAttackTypeValue("melee_1", "time");
				#go.setPrimaryAnimState(AnimStates.AS_MELEE_1);

	def isComplete(self):
		go = self.machine.mind;
		if self.targetObject == None or self.targetObject.getHealth() <= 0:
			go.setPrimaryAnimState(AnimStates.AS_IDLE);
			return True;
		return self.maxCapacity

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True;
		if isinstance(s, savage.ChaseState):
			return True;

		if isinstance(s, savage.ReturnState):
			return True;
		if isinstance(s, savage.ConstructState):
			return True;
		if isinstance(s, savage.MineState):
			return True;
		return False;


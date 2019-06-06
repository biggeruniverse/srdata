# (c) 2011 savagerebirth.com

from silverback import *
from vectors import Vec3
import logging
import threading
import time

class Mind(GameObject):
	import logging;
	logger = logging.getLogger("savage.ai.mind")
	def __init__(self, oid):
		import threading
		savage.GameObject.__init__(self, oid)
		self.goalStack = []
		self.goal = None
		self.lastGoal = None
		self.fsm = savage.FiniteStateMachine(self)
		self.death = threading.Event()
		self.thread = threading.Thread(name="Mind of %d" % oid, target=self.update)
		self.homePos = savage.Vec3(0.0, 0.0, 0.0)
		self.givingWay = False
		self.lastCollisions = []

		self.death.clear()
		self.thread.start()

	def setIdle(self, val):
		return savage.ai_setidle(self.objectId, val)

	def gotoPosition(self, pos):
		return savage.ai_gotoposition(self.objectId, pos[0], pos[1]);

	def gotoObject(self, obj):
		return savage.ai_gotoobject(self.objectId, obj.objectId);

	def stopMoving(self):
		return savage.ai_stop(self.objectId);

	def isMoving(self):
		return savage.ai_ismoving(self.objectId);

	def isArrived(self):
		return savage.ai_isarrived(self.objectId)

	def isIdle(self):
		return savage.ai_isidle(self.objectId)

	def fireWeapon(self, targetPos):
		weaponType = savage.getObjectType(self.getType().getValue("forceInventory0"));
		return savage.ai_fireweapon(self.objectId, targetPos[0], targetPos[1], targetPos[2], weaponType.typeId);

	def mineResources(self, mine):
		savage.ai_mineresources(self.objectId, mine.objectId)

	def addGoal(self, goal):
		self.goalStack.append(goal);

	def insertGoal(self, goal):
		if self.goal is not None:
			self.goalStack.insert(0, self.goal)
		self.goalStack.insert(0, goal)
		self.goal = None

	def clearGoals(self):
		self.goalStack = [];
		self.goal = None;
		self.lastGoal = None;
		self.givingWay = False;

	def goalReached(self):
		#if self.goal is not None and self.goal.state == goaltype:
		self.goal = None;
		self.givingWay = False;

	def setCurrentGoalPriority(self, p):
		self.goal.priority = p;

	def reassessPriorities(self):                
		self.lastGoal = self.goal;

		if self.goal is not None:
			self.goalStack.append(self.goal)

		self.goalStack = sorted(self.goalStack, key=lambda goal: goal.priority)
		if len(self.goalStack) > 0:
			self.goal = self.goalStack.pop(0);

		if self.goal is None:
			self.setIdle(True)
			return;
		else:
			self.setIdle(False)

		self.handleGoal();

	def update(self):
		while not self.death.is_set():
			self.reassessPriorities();

			#we're done here
			#if self.getHealth() <= 0:
			#	self.death.set();

			#NOTE: "thinking" is done here
			self.fsm.evaluate();

			self.lastCollisions = []
			time.sleep(.1) #we don't need them to be thinking all the time

	def handleGoal(self):                
		if self.goal == self.lastGoal:
			return;
		self.logger.debug("Handling goal "+str(self.goal));
		self.fsm.reset();

		if self.goal is None:
			return
		elif self.goal.state == savage.Goal.AIGOAL_ATTACK:
			self.fsm.insertState(savage.ReturnState(self.homePos));
			self.fsm.insertState(savage.AttackState(self.goal.targetObject));

		elif self.goal.state == savage.Goal.AIGOAL_CHASE:
			self.fsm.insertState(savage.ChaseState(self.goal.targetObject, -1));
			
		elif self.goal.state == savage.Goal.AIGOAL_EVADE:
			evadeDist = 200.0;
			o = savage.Vec3(self.getPosition())
			p = savage.Vec3(self.goal.targetObject.getPosition())
			if o.distanceSqTo(p) < (evadeDist ** 2):
				self.fsm.insertState(savage.EvadeState(self.goal.targetObject, evadeDist));
			else:
				self.fsm.insertState(savage.HeadlessChickenState(7000))
			self.goalStack[:] = (g for g in self.goalStack if g.state != savage.Goal.AIGOAL_EVADE)
			
		elif self.goal.state == savage.Goal.AIGOAL_GOTO:
			self.fsm.insertState(savage.GoState(self.goal.targetPosition));
			
		elif self.goal.state == savage.Goal.AIGOAL_IDLE:
			self.setIdle(True);
		elif self.goal.state == savage.Goal.AIGOAL_FOLLOW:
			self.fsm.insertState(savage.FollowState(self.goal.targetObject));
		else:
			self.logger.warn("unhandled goal "+str(self.goal));
			self.goalReached()

	def commandPosition(self, whofrom, goal, x, y):
		g = savage.Goal(goal, 25000);
		g.targetPosition = Vec3(x, y, 0);
		self.addGoal(g);

	def commandTarget(self, whofrom, goal, obj):
		g = savage.Goal(goal, 25000);
		g.targetObject = savage.getGameObject(obj); #getGameObject returns the correct instance
		self.addGoal(g);

	def findClosestObject(self, objtype):
		#really just a wrapper...
		objs = savage.getTypeObjects(objtype);
		closest = objs[0];
		o = Vec3(self.getPosition());
		for obj in objs:
			p = Vec3(obj.getPosition());
			if p.distanceSqTo(o) < Vec3(closest.getPosition()).distanceSqTo(o):
				closest = p;

		return closest;

	def findClosestDropPoint(self):
		buildings = savage.team_getbuildings(self.getTeam());
		closest = None;
		o = Vec3(self.getPosition());
		for obj in buildings:
			if obj.getType().getValue("dropoff") and not obj.isBeingBuilt():
				p = Vec3(obj.getPosition());
				if closest is None or p.distanceSqTo(o) < Vec3(closest.getPosition()).distanceSqTo(o):
					closest = obj;
		return closest;

	#override this to create species-specific behaviour
	def onSpawn(self, target):
		self.homePos = savage.Vec3(self.getPosition())
	
	def onDamaged(self, target, amt):
		# let's not attack ourselves!
		if target.objectId == self.objectId:
			return;
		#perhaps we're already mad at the person attacking us...
		if target == self.fsm.states[0].targetObject:
			if self.goal.state == savage.Goal.AIGOAL_ATTACK:
				self.goal.priority+=1000;
			return;
		g = savage.Goal(savage.Goal.AIGOAL_ATTACK, 3000);
		g.targetObject = target;
		#if self.goal.state == savage.Goal.AIGOAL_IDLE:
                #        self.clearGoals()
		self.insertGoal(g);

	def onDeath(self, killer):
		self.setPrimaryAnimState(AnimStates.AS_DEATH_GENERIC);
		self.death.set();

	def onDestroy(self):
		self.death.set();
		self.thread = None;
		self.fsm.clear();

	def onCollide(self, obj):                
		self.lastCollisions.append(obj)

	def onPushed(self, obj):
		if isinstance(obj, savage.Player) and obj.getTeam() == self.getTeam() and not self.givingWay:
			o = savage.Vec3(obj.getPosition())
			p = savage.Vec3(self.getPosition())
			t = p - o
			t.data[2] = 0.0
			t = t.normalise() * 30.0
			t = p + t
			g = savage.Goal(savage.Goal.AIGOAL_GOTO, 10000)
			g.targetPosition = t
			self.insertGoal(g)
			self.givingWay = True

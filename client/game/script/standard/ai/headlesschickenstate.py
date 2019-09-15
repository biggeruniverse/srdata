# (c) 2011 savagerebirth.com
#
# Make the AI run around like a headless chicken in an effort to dodge missiles

from vectors import Vec3;

class HeadlessChickenState(savage.FSMState):
	def __init__(self, time):
		savage.FSMState.__init__(self)
		self.endTime = savage.getGameTime() + time
		self.targetPos = None
		self.nav = savage.StateNavigation()

	def getRandomPoint(self):
		go = self.machine.mind
		p = savage.Vec3(go.getPosition())
		dist = float(M_Randnum(25, 50))
		dirX = M_Randnum(0, 200) - 100
		dirY = M_Randnum(0, 200) - 100
		direction = savage.Vec3(dirX, dirY)
		return ((direction.normalise() * dist) + p)
	
	def run(self):
		go = self.machine.mind

		if self.targetPos is None:
                        self.targetPos = self.getRandomPoint()

		if not self.nav.firstRun and go.isArrived():
			self.targetPos = self.getRandomPoint()
			go.gotoPosition(self.targetPos)
			self.nav.repath()

		if self.nav.run(go):
			go.gotoPosition(self.targetPos)

	def isComplete(self):
		go = self.machine.mind
		if self.endTime <= savage.getGameTime():
			go.stopMoving()
			go.setPrimaryAnimState(AnimStates.AS_IDLE)
			return True
		return False

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True
		return False

			

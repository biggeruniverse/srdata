# (c) 2011 savagerebirth.com
#
# Generic class used by states that require navigation

class StateNavigation:
	def __init__(self):
		self.timeMin = 500
		self.timeMax = 1500
		self.blockMin = 250
		self.blockMax = 750
		self.repathTime = savage.getGameTime()
		self.blockTime = 0
		self.firstRun = True
		self.blocked = False

        # call if you need to repath the AI
	def repath(self):
                self.repathTime = savage.getGameTime() + M_Randnum(self.timeMin, self.timeMax)

	# keep track of navigation, return True when repath is required
	def run(self, go):
		for c in go.lastCollisions:
			if isinstance(c, savage.Mind):
				if c.isMoving():
					# block ourselves and wait for the other guy to get out of the way
					go.setPrimaryAnimState(AnimStates.AS_IDLE)
					go.stopMoving()
					self.blockTime = savage.getGameTime() + M_Randnum(self.blockMin, self.blockMax)
					self.blocked = True
					return False
				else:
					# if we ran into an NPC that isn't moving we need to recalculate our path
					self.repathTime = savage.getGameTime()

		if self.blocked:
			if self.blockTime <= savage.getGameTime():
				self.blocked = False
				self.repathTime = savage.getGameTime()
			else:
				return False

		go.setPrimaryAnimState(AnimStates.AS_WALK_FWD)
		go.setSecondaryAnimState(AnimStates.AS_IDLE)

		if self.repathTime <= savage.getGameTime():
			self.repath()
			self.firstRun = False
			return True

		return False

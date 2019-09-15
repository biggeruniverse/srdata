# (c) 2011 savagerebirth.com
class DropoffState(savage.FSMState):
	def __init__(self, dropoff):
		savage.FSMState.__init__(self);
		self.dropoff = dropoff
		self.done = False
		
	def run(self):
		go = self.machine.mind;

		if self.dropoff is None or self.dropoff.getHealth() <= 0 or not self.dropoff.isActive():
                        self.dropoff = go.findClosestDropPoint()
                        go.fsm.insertState(savage.ChaseState(dropoff, dropoff.getType().getValue("proximity")))
                        return
		
		savage.ai_dropoffresources(go.objectId, self.dropoff.objectId);
		
		self.done = True;

	def isComplete(self):
		return self.done;

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True;
		if isinstance(s, savage.ChaseState):
			return True;
		
		return False

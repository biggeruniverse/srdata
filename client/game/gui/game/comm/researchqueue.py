#copyright (c) savagerebirth.com 2011
#this file defines the ResearchQueue, an important ActionSequence subclass

#The Queue is an ActionSequence
#Each researchable item in the queue is an action (ResearchAction)

class ResearchQueue(ActionSequence):
	def __init__(self):
		ActionSequence.__init__(self);
		self.listeners = [];
	
	def is_done(self):
		if len(self.actions) > 0:
			item = self.actions[0]
			if not item.areReqsMet():
				self.swap(0, len(self.actions)-1)
		#gimp the is_done so the sequence never disappears on us
		return False;

	#pause inherited from ActionSequence
	
	def swap(self, a, b):
		if a == b or len(self.actions) == 1:
			return;
		self.actions.rotate(-a);
		itemA = self.actions.popleft();
		self.actions.rotate(a-b+1);
		itemB = self.actions.popleft();
		self.actions.appendleft(itemA);
		self.actions.rotate(b-1-a);
		self.actions.appendleft(itemB);
		self.actions.rotate(a); 
		
		#phew!

	def cancel(self, index=0):
		self.actions.rotate(-index);
		#so the element we want to remove is at the LHS of the deque
		action = self.actions.popleft();
		self.actions.rotate(index);
		for l in self.listeners:
			l.onResearchCancelled(action);

	def cancelAction(self, action):
		for i,a in enumerate(self.actions):
			if a == action:
				self.cancel(i);
				break;

	def contains(self, item):
		for a in self.actions:
			if a.item.objtype.typeId == item:
				return True;
		return False;

	def getQueue(self):
		return self.actions;

	def areReqsMet(self, index=0):
		return self.action[index].areReqsMet();

	def addResearch(self, item):
		#check that we actually CAN research another one
		if item.objtype.isWorkerType() or item.objtype.isBuildingType() or not item.objtype.isResearched():
			con_dprintln("adding research for "+item.objtype.getName()+"\n");
			action = ResearchAction( item );
			action.set_sequence(self);
			self.add_action(action)
			for l in self.listeners:
				l.onResearchQueued(action);

	def addListener(self, l):
		self.listeners.append(l);

gblQueue = ResearchQueue();


#copyright (c) savagerebirth.com 2011
#this file defines the ResearchQueue, an important ActionSequence subclass

#The Queue is an ActionSequence
#Each researchable item in the queue is an action (ResearchAction)

class ResearchQueue(ActionSequence):
	def __init__(self):
		ActionSequence.__init__(self);
		self.listeners = [];
	
	def is_done(self):
		return False;
		#gimp the is_done so the sequence never disappears on us

	#pause inherited from ActionSequence
	
	def swap(self, a, b):
		self.rotate(-a);
		itemA = self.popleft();
		self.rotate(a-b+1);
		itemB = self.popleft();
		self.appendleft(itemA);
		self.rotate(b-1-a);
		self.appendLeft(itemB);
		self.rotate(a); 
		
		#phew!

	def cancel(self, index=0):
		self.rotate(-index);
		#so the element we want to remove is at the LHS of the deque
		action = self.popleft();
		self.rotate(index);
		for l in self.listeners:
			l.onResearchCancelled(action);


	def getQueue(self):
		return self.actions;

	def areReqsMet(self, index=0):
		return self.action[index].areReqsMet();

	def addResearch(self, item):
		con_dprintln("adding research for "+item.objtype.getName()+"\n");
		action = ResearchAction( item );
		action.setParent(self);
		self.actions.append(action);
		for l in self.listeners:
			l.onResearchQueued(action);

	def addListener(self, l):
		self.listeners.append(l);

gblQueue = ResearchQueue();


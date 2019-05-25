# (c) 2011 savagerebirth.com

from silverback import *;

class ResearchAction(Action):
	def __init__(self, item):
		Action.__init__(self);
		self.item = item;
		self.requested = False;

	def run(self):
		if self.areReqsMet():
			CL_RequestPurchase(self.item.getType().getName(), self.item.builder);
			self.requested = True;
	
	def areReqsMet(self):
		return self.item.areRequirementsMet();

	def __eq__(self, b):
		if not isinstance(b, ResearchAction):
			return False;
		return self.item == b.item;
		
	def isDone(self):
		return self.requested;


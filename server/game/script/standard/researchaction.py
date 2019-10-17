# (c) 2011 savagerebirth.com

from silverback import *;

class ResearchAction(Action):
	def __init__(self, item):
		Action.__init__(self);
		self.item = item;
		self.requested = False;

	def run(self):
		if self.areReqsMet() and not self.requested:
			CL_RequestPurchase(self.item.getType().getName(), self.item.builder);
			self.requested = True;

	def is_done(self):
		return self.requested
	
	def areReqsMet(self):
		return self.item.areRequirementsMet();

	def __eq__(self, b):
		if not isinstance(b, ResearchAction):
			return False;
		return self.item == b.item;
		
	def is_done(self):
		return self.requested;


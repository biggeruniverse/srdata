# (c) 2011 savagerebirth.com

from silverback import *;

class WaitForStateSlotAction(Action):
	def __init__(self, obj, slot):
		self.slot = slot;
		self.obj = obj;
		return Action.__init__(self);

	def run(self):
		#con_dprintln("BOING! BOING! The time remaining is: "+str(self.until-Host_Milliseconds())+"\n");
		pass;

	def is_done(self):
		if self.obj.getState(self.slot) is not None:
			return False;
		return True;


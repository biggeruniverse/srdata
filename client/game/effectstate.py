# (c) 2010 savagerebirth.com
# this represents buffs, debuffs, and so on
import savage;

class EffectState:
	def __init__(self, stateid, i, r, dur):
		self.stateId = stateid;
		self._timeRemaining = r;
		self.inflictor = i;
		self.duration = dur;
	
	def __str__(self):
		return "State Object for " +self.getName()+" (ID "+str(self.stateID)+")";

	def getValue(self, name):
		return savage.state_getpropertyvalue(self.stateId, name);
		
	def getName(self):
		return self.getValue("name");
		
	def getIcon(self):
		iconPath = self.getValue("icon"); #.replace(".tga",".s2g");
		if iconPath == "":
			iconPath = "/gui/standard/black.s2g";
		return iconPath;

	# a state could be inflicted by an item or object, not just a player
	def getInflictor(self):
		if self.inflictor == -1:
			return None;
		return savage.getGameObject(self.inflictor);
		
	def getTimeRemaining(self, seconds = True):
		if self.getValue("neverDisplayTime") == 1 or self._timeRemaining == -1:
			if seconds:
				return "";
			return 0.0;				
		if seconds: return str(round(self._timeRemaining,1)) + "s";
		else: return self._timeRemaining;
	
	def getDuration(self):
		return self.duration;


# (c) 2011 savagerebirth.com
#
# This class is used by the game code to mask the fact that items in inventory are not actual game objects in the world. This is used when calling on* hooks for inventory items.
#

import savage;

class GameItem(savage.GameObject):
	def __init__(self, itype, team=-1):
		self.team = team;
		self.itemtype = None;
		if team >= 0:
			self.itemtype = savage.ObjectType(itype);
			savage.GameObject.__init__(self, -1);
		else:
			savage.GameObject.__init__(self, itype);

	def getTeam(self):
		if self.team == -1:
			return savage.GameObject.getTeam(self);
		else:
			return self.team;

	def getName(self):
		if self.itemtype is None:
			return savage.GameObject.getName(self);
		else:
			return self.itemtype.getName();


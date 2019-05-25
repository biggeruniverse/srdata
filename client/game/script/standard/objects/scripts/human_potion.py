class human_potion(GameItem):
	def onImpact( self, target ):
		objs = savage.getRadiusObjects(self.objectId, 70);
		for obj in objs:
			if obj.getTeam() == self.getTeam():
				obj.addState(self.getOwner(), "human_potion", 11000);


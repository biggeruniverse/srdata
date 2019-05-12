class human_revive(GameItem):
	def onUse(self, user, target):
		objs = savage.getRadiusObjects(user.objectId, 35.0);
		for obj in objs:
			self.onImpact(obj);

	def onImpact( self, target ):
		if target.getTeam() == self.getTeam():
			target.revive( 0.5 );

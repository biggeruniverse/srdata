class beast_poison(GameItem):
	def onImpact( self, target ):
		if target is not None and target.getTeam() != self.getTeam():
			target.addState(self.getOwner(), "poisoned", 5000);

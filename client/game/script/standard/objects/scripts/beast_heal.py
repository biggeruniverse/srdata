class beast_heal(GameItem):
	def onImpact( self, target ):
		if target != None and target.getTeam() == self.getTeam():
			target.heal(93);

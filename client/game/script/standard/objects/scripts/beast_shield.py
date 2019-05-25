class beast_shield( GameItem):
	def onImpact( self, target ):
		if target is not None and self.getOwner().getTeam() == target.getTeam():
			target.addState(target, "beast_shield" , 400);

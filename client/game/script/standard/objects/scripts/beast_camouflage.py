class beast_camouflage(GameItem):
	def onUse( self, user, target ):
		target.addState(user, "beast_camouflage", 15000);

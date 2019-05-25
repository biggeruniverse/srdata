class beast_protect(GameItem):
	def onUse( self, user, target ):
		target.addState(user, "beast_protect", 5000);

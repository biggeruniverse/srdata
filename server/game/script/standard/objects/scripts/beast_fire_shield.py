class beast_fire_shield( GameItem):
	def onUse( self, user, target ):
		target.addState(user, "fire_shield" , 10000);

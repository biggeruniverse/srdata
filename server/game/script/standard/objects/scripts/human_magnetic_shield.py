class human_magnetic_shield(GameItem):
	def onUse( self, user, target ):
		target.addState(user, "magshield", 11000);

class human_adrenaline(GameItem):
	def onUse( self, user, target ):
		target.addState(user, "adrenaline", 12500);

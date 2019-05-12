class beast_rabid(GameItem):
	def onSpawn( self, target ):
		target.addState(None, "rabid", -1);

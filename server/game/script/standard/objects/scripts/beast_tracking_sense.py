class beast_tracking_sense(GameItem):
	def onSpawn( self, target ):
		target.addState(None, "beast_tracking" , -1);

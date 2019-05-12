class beast_tracking_sense( GameItem):
	def onSpawn( self, target ):
		target.addState(target, "beast_tracking" , -1);

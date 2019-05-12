class human_electrify(GameItem):
	def onUse( self, user, target ):
		target.addState(user, "electrify", 10000);

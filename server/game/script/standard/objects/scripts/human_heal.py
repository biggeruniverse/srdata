class human_heal(GameItem):
	def onImpact( self, target ):
		if target != None and target.getTeam() == self.getTeam():
			#TODO: give experience to the owner of self (if there was an owner)
			target.heal(11);

class human_incinerator( GameItem):
	def onImpact( self, target ):
		if target is not None and self.getTeam() != target.getTeam():
			if target.getTeam() == 0:
				target.addState(self.getOwner(), "barbequed",5000);
			else:
				target.addStateTime("beast_immolate", -0.3);

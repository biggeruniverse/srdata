class beast_snare( GameItem):
	def onFuseEnd( self ):
		objs = savage.getRadiusObjects(self.objectId, 30);
		for obj in objs:
			if obj.getTeam() != self.getTeam():
				obj.addState(self.getOwner(), "snare", 3000);
		self.die();

"""
@fuse
!givestateradius self 30 snare 3000
!die self
"""


class human_disruptor(GameItem):
	def onFuseEnd(self):
		objs = savage.getRadiusObjects(self.objectId, 100);
		for obj in objs:
			if obj.getTeam() != self.getTeam():
				obj.addState(self, "pulsed", 12000);

		self.die();

	def onBackfire(self, owner):
		owner.damage(owner, 1000);

"""
@fuse
!givestateradius self 100 pulsed 12000
!destabilize self 120 enemy neutral item ally
!die self

@backfire
!damage self 1000
"""


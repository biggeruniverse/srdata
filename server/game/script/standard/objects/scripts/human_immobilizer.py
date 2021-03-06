from savage import WaitAction, CallAction

class human_immobilizer( GameItem):
	def onUse(self, user, target):
		ActionSequence(savage.WaitAction(3000), savage.CallAction(GameItem.givestate, (user, "immobilize", 3333)));

	def onFuseEnd( self ):
		objs = savage.getRadiusObjects(self.objectId, 30);
		for obj in objs:
			if obj.getTeam() != self.getTeam():
				obj.addState(self.getOwner(), "immobilize", 3333);
		self.die();

	def onBackFire(self):
		self.getOwner().addState(self.getOwner(), "immobilize", 3250);

"""
@fuse
!givestateradius self 35 imobilize 3250
!die self

@backfire
!givestate self imobilize 3333
"""


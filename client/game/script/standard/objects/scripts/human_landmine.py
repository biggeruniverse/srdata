# (c) 2011 savagerebirth.com

class human_landmine(GameItem):
	def onUse( self, user, target):
		target.drop(savage.getObjectType("human_landmine").typeId, 0.0, 1.0 );

	def onDrop(self):
		self.setState("idle");

	def onIdle(self, target):
		ActionSequence(WaitAction(5000), TripAction(self, 50), ActivateAction(self));

	def onActivate(self, target):
		ActionSequence(WaitAction(350), DieAction(self));
	
	def onDeath(self, killer):
		objs = savage.getRadiusObjects(self.objectId, 150);
		for obj in objs:
			self.damageFalloff(obj, 500, 150);

"""
#@use
!toss target 20 1.0

@toss
!setstate self idle
!delay self 5000

@idling
!scan self 50 activate unit neutral enemy

@activate
!delay self 500

@active
!die self

@die
!damageradius self 150 500

"""

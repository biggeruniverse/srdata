#import vectors;

class beast_fire_trap(GameItem):
	def onUse( self, user, target):
		target.drop(savage.getObjectType("beast_fire_trap").typeId, 0.0, 4.0 );

	def onDrop(self):
		self.setState("idle");
	
	def onIdle(self, target):
		ActionSequence(WaitAction(5000), TripAction(self, 50), ActivateAction(self));

	def onActivate(self, target):
		ActionSequence(WaitAction(500), DieAction(self));

	def onDeath(self, killer):
		objs = savage.getRadiusObjects(self.objectId, 150);
		for obj in objs:
			self.damageFalloff(obj, 500, 150);

"""
#on use, drop the fire ward, and don't let it do anything for 5 seconds.
# if, after that, a neutral or enemy unit is within 50 units of the fireward, explode in half a second
# when the ward explodes, deal 500 units of damage in a radius of 150 units

// beast_fire_trap.gs
@use
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


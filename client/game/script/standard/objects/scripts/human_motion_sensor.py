class human_motion_sensor(GameItem):
	def onUse(self, user, target):
		target.drop(savage.getObjectType("human_motion_sensor").typeId, 0.0, 1.0);

	def onDrop(self):
		self.setState("idle");

"""
@use
!toss target 40 1.0

@toss
!setstate self idle

"""

from savage import WaitAction, ActivateAction, DieAction

class human_demo_pack(GameItem):
	def onUse(self, user, target):
		target.drop(savage.getObjectType("human_demo_pack").typeId, 0.0, 1.0);

	def onDrop(self):
		ActionSequence(savage.WaitAction(7500), savage.ActivateAction(self));

	def onActivate(self, target):
		objs = savage.getRadiusObjects(self.objectId, 125);

		for obj in objs:
			self.damageFalloff(obj, 6500, 125);
		#this ensures proper effect firing
		ActionSequence(savage.WaitAction(200), savage.DieAction(self));


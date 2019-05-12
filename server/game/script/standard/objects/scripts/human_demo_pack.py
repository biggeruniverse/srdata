# (c) 2011 savagerebirth.com

import silverback;
from vectors import Vec3;

class human_demo_pack(GameItem):
	def onUse(self, user, target):
		target.drop(savage.getObjectType("human_demo_pack").typeId, 0.0, 1.0);

	def onDrop(self):
		ActionSequence(silverback.WaitAction(7500), silverback.ActivateAction(self));

	def onActivate(self, target):
		objs = savage.getRadiusObjects(self.objectId, 125);

		for obj in objs:
			self.damageFalloff(obj, 6500, 125);
		#this ensures proper effect firing
		ActionSequence(silverback.WaitAction(200), silverback.DieAction(self));


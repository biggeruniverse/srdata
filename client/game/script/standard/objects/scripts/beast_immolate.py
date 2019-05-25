class beast_immolate(GameItem):
	def onUse(self, user, target):
		#usually you don't see the go_* funcs, they are wrapped up...
		go = savage.go_spawn(savage.getObjectType("beast_immolate").typeId, user.objectId);
		user.addState(user, "beast_immolate", 10000);
		user.attach(go);

	def onAttach(self, to):
		self.setState("idle");
		ActionSequence(WaitForStateSlotAction(self.getOwner(), 6), ActivateAction(self));

	def onActivate(self, target):
		objs = savage.getRadiusObjects(self.getOwner().objectId, 100);
		self.damage(self.getOwner(), 999999);
		for obj in objs:
			self.damageFalloff(obj, 5300, 100);
		self.die();


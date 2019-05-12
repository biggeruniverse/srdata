class human_relocater(GameItem):
	def onUse( self, user, target):
		link = user.drop(savage.getObjectType("human_relocater").typeId, 0.0, 1.0);
		user.setLink(link);

	def onDrop(self):
		user = self.getOwner();
		trigger = user.giveItem(savage.getObjectType("human_relocater_trigger"), user.getCurrentInventorySlotIndex());
		

"""
@use
!toss target 20 1.0
!give target human_relocater_trigger
"""

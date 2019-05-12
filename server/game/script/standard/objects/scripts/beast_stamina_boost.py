class beast_stamina_boost(GameItem):
	def onUse( self, user, target ):
		target.addState(user, "beast_staminaregen" , 10000);


class beast_recharge(GameItem):
	def onUse( self, user, target ):
		#only allow it to be used on siege?
		target.heal( 1000 );
		target.giveStamina(5000);
		target.giveMana(250);

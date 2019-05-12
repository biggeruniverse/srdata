class human_ammo_pack(GameItem):
	def onSpawn( self, target ):
		target.giveAmmo(2.0, "full");

class human_medkit(GameItem):
	def onUse(self, user, target):
		user.healPct(0.33);

# (c) 2011 savagerebirth.com

class CheckAFKHandler:
	def __init__(self):
		self.runner = None;

	def onEvent(self, e):
		if e.eventType == 'status':
			if e.sourceId == GAME_STATUS_NORMAL:
				if self.runner is not None:
					self.runner.stop = True;
				self.runner = CheckAFKRunner();
			elif e.sourceId == GAME_STATUS_SETUP:
				if self.runner is not None:
					self.runner.stop = True;

class CheckAFKRunner:
	def __init__(self):
		self.thread = Timer(self, Cvar_GetValue("sv_checkAFKInterval"));
		self.stop = False;

	def run(self):
		if self.stop is True:
			return;
		players = savage.getPlayers();
		interval = Cvar_GetValue("sv_checkAFKInterval");
		if interval == 0:
			interval = 300;
			CVar_SetValue("sv_checkAFKInterval", 300);

		for player in players:
			if player.getIdleTime()/1000 >= interval and player.getTeam() != 0:
				player.setTeam(0);
				SV_BroadcastNotice(player.getName()+" was moved to spectators for being idle.");

		self.thread = Timer(self, interval);


checkAFK = CheckAFKHandler();
gblEventHandler.addGameListener(checkAFK);

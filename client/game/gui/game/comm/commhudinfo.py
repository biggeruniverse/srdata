#(c) 2011 savagerebirth.com

class CommHudStats(glass.GlassContainer):
	def __init__(self, oid):
		glass.GlassContainer.__init__(self);
		self.objectId = oid;
		self.setOpaque(False);
		self.health = glass.GlassProgressBar();
		self.health.setFrameSize(1);
		self.health.setBaseColor( black );
		self.health.setBackgroundColor( glass.Color(133,11,10) );
		self.health.setForegroundColor( glass.Color(21,255,22) );
		self.health.setSizePct(0.0488, 0.006510);
		self.add(self.health, 0, 0);
		self.build = glass.GlassProgressBar();
		self.build.setFrameSize(1);
		self.build.setBaseColor( black );
		self.build.setBackgroundColor( glass.Color(10,115,110) );
		self.build.setForegroundColor( glass.Color(20,255,248) );
		self.build.setSizePct(0.0488, 0.006510);
		self.add(self.build, 0, 10);

	def update(self):
		obj = savage.getGameObject(self.objectId);
		self.health.setProgress(obj.getHealthPct());
		if obj.isBeingBuilt():
			self.build.setVisible(1);
			self.build.setProgress(obj.getBuildProgress());
		else:
			self.build.setVisible(0);

class CommHudInfo(glass.GlassContainer):
	def __init__(self):
		glass.GlassContainer.__init__(self);
		self.setSize(screenWidth, screenHeight);
		self.bars = {};
		self.setOpaque(False);

	def update(self):
		self.setSizePct(1, 1);
		visobjs = savage.getObjectsWithin(0,0,self.getWidth(), self.getHeight());
		team = savage.getLocalPlayer().getTeam();
		for bar in self.bars.values():
			bar.setVisible(0);

		for obj in visobjs:
			if obj.getTeam() == team:
				v = obj.getScreenTopPosition();
				if obj.objectId not in self.bars:
					stats = CommHudStats(obj.objectId);
					self.add(stats);
					self.bars[obj.objectId] = stats;

				stats = self.bars[obj.objectId];
				stats.setVisible(1);
				stats.setSizePct(0.0488, 3*0.006510);
				stats.setPosition(int(v[0])-25, int(v[1]));
				stats.update();


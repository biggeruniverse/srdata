#copyright (c) savagerebirth.com 2011
#this file generates the resource and cc health information at the top of the screen

import savage;
import glass;
from silverback import *;
import tools;

class CenterResourceContainer(DefaultContainer):

	def __init__(self):
		DefaultContainer.__init__(self);
		self.setOpaque(False);
		self.setVisible(True);
		self.setBackgroundColor(transparency);	

		self.team = None;
		self.lastWorkers = [];

		goldImg = glass.GlassLabel()
		goldImg.setImage("gui/game/images/gold_icon.s2g");
		goldImg.setSize(24,24); # A bit smaller than the redstone one
		self.add(goldImg, 0, 0);

		self.goldLbl = DefaultLabel("00000");
		self.goldLbl.setForegroundColor(gold);
		self.add(self.goldLbl, goldImg.getWidth() + 2, 0);

		self.redstoneImg = glass.GlassLabel();
		self.redstoneImg.setImage("gui/game/images/redstone.s2g");
		self.redstoneImg.setSize(32,32); # Image size
		self.add(self.redstoneImg, self.goldLbl.getX() + self.goldLbl.getWidth() + 5);

		self.redstoneLbl = DefaultLabel("00000");
		self.redstoneLbl.setForegroundColor(tangoRedLight);
		self.add(self.redstoneLbl, self.redstoneImg.getWidth() + self.redstoneImg.getX() + 2, 4);

		self.workerImg = glass.ImageButton();
		self.workerImg.setId("idle");
		self.workerImg.setImage("gui/game/images/human_worker.s2g");
		self.workerImg.setSize(24,24); # Image size
		self.add(self.workerImg, self.redstoneLbl.getX() + self.redstoneLbl.getWidth() + 5);
		self.workerImg.addActionListener(self);

		self.workerLbl = DefaultLabel("00/00");
		self.workerLbl.setForegroundColor(gold);
		self.add(self.workerLbl, self.workerImg.getWidth() + self.workerImg.getX() + 2, 0);

		self.fit(); # let's see if that works!

		#testing stuff:
		self.setWidth(self.getWidth() + 10)

		self.onShow();

	def onShow(self):
		self.team = savage.getLocalTeam();
		race = self.team.getRace();

		self.workerImg.setImage("gui/game/images/" + race + "_worker.s2g");
		self.workerImg.setSize(24,24); # Image size

	def update(self):
		#self.team = savage.getLocalTeam(); # todo! we don't want to do that every frame
		working, total , max = self.team.getWorkerInfo();
		self.workerLbl.setCaption(str(working).zfill(2) + "/" + str(total).zfill(2));

		res = self.team.getResources();
		self.goldLbl.setCaption(str(res['gold']));
		self.redstoneLbl.setCaption(str(res['stone']));

	def onAction(self, e):
		if e.widget.getId() == "idle":
			workers = self.team.getIdleWorkers();
			
			for worker in workers:
				#print(worker.objectId, self.lastWorkers)
				if len(workers) == 1 or worker.objectId  not in self.lastWorkers:
					self.lastWorkers.append(worker.objectId);
					pos = worker.getPosition();
					CL_CenterCamera(pos[0], pos[1]);
					return;
			if len(workers) > 2:
				worker = workers[0];
				self.lastWorkers = [worker];
				pos = worker.getPosition();
				CL_CenterCamera(pos[0], pos[1]);

class BuffPoolContainer(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);

		self.setSize(129, 40);

		self.widgetList = [];

		for i in range(3):

			cont = DefaultContainer();
			cont.setSize(self.getHeight(), self.getHeight());

			img = DefaultImage();
			img.imagePath = "";
			img.setImage("todo");
			img.setSize(24, 24);
			cont.add(img, "center" , "center");
			
			progress = glass.GlassProgressDisc();
			progress.setImage("gui/game/images/white_ring.png");
			progress.setSize(self.getHeight(),self.getHeight());
			progress.setProgress(0);
			cont.add(progress, "center", "center");

			counter = DefaultLabel("123");
			counter.setFont(fontSizeSmall);
			cont.add(counter, "center", "center" );

			self.add(cont, i*43);

			widgets = [counter, progress, img];
			self.widgetList.append(widgets);

	def rebuild(self):

		team = savage.getLocalTeam();
		resources = team.getResources();
		race = team.getRace();

		if race == "beast":
			res = [str(resources["entropy"]), str(resources["strata"]), str(resources["fire"])];
			col = [tangoGreenLight, tangoBlue, tangoOrange];
			img = ["/gui/standard/icons/entropy.s2g", "/gui/standard/icons/strata.s2g", "/gui/standard/icons/fire.s2g"];

		elif race == "human":
			res = [str(resources["magnetic"]), str(resources["electric"]), str(resources["chemical"])];
			col = [tangoRedLight, tangoBlueLight, tangoGreenLight];
			img = ["/gui/standard/icons/magnetic.s2g", "/gui/standard/icons/electric.s2g", "/gui/standard/icons/chemical.s2g"];

		else: 
			# Should never happen, but who knows...
			self.setVisible(False);
			return;

		for i, widgets in enumerate(self.widgetList):
			widgets[0].setForegroundColor(col[i]);
			widgets[0].setCaption(res[i].zfill(3));

			#widgets[1].setProgress(0);
			widgets[1].setForegroundColor(col[i]);

			x, y = widgets[2].getWidth(), widgets[2].getHeight();
			widgets[2].setImage(img[i]);
			widgets[2].setSize(x, y);

	def update(self):

		team = savage.getLocalTeam();
		resources = team.getResources();
		race = team.getRace();

		maxPool = [0, 0, 0];
		res = [];

		if race == "beast":
			resourceNames = ["entropy", "strata", "fire"];

		elif race == "human":
			resourceNames = ["magnetic", "electric", "chemical"];
		else:
			return;
			
		for i, item in enumerate(resourceNames):

			res.append(resources[item]);
			rid = savage.getResourceId(item);

			for go in [b for b in team.getBuildings() if not b.isBeingBuilt()]:
				maxPool[i] += go.getCapacity(rid);
		
		for i, widgets in enumerate(self.widgetList):			
			widgets[0].setCaption(str(res[i]));
			widgets[0].setX(widgets[2].getX() + (widgets[2].getWidth() // 2 - widgets[0].getWidth() // 2));
			try:
				pct = float(res[i]) / float(maxPool[i]);
				widgets[1].setProgress( pct );
			except ZeroDivisionError:
				widgets[1].setProgress(0);

class ResourcePanel(glass.GlassContainer):
	def __init__(self):
		from collections import deque;

		glass.GlassContainer.__init__(self);
		self.setBackgroundColor( glass.Color(0,0,0,128));
		self.setSizePct( 1 , 0.025);
		self.setPosition(0,0);

		self.teamGold = glass.GlassLabel("_12345 ");
		self.teamGold.setForegroundColor(gold);
		self.add(self.teamGold);
		self.teamGold.setPositionPct(0,0);
		self.teamGold.setSizePct(0.1,1);

		self.goldIncome = glass.GlassLabel("_12345 ");
		self.goldIncome.setForegroundColor(gold);
		self.add(self.goldIncome);
		self.goldIncome.setPositionPct(0.09,0);
		self.goldIncome.setSizePct(0.1,1);

		self.stoneCounter = glass.GlassLabel("_12345__");
		self.stoneCounter.setForegroundColor( tangoRedLight);
		self.add(self.stoneCounter);
		self.stoneCounter.setPositionPct(0.15,0);
		self.stoneCounter.setSizePct(0.1,1);

		self.stoneIncome = glass.GlassLabel("_12345__");
		self.stoneIncome.setForegroundColor(tangoRedLight);
		self.add(self.stoneIncome);
		self.stoneIncome.setPositionPct(0.24,0);
		self.stoneIncome.setSizePct(0.1,1);

		self.res1Counter = glass.GlassLabel("_12345__");
		self.add(self.res1Counter);
		self.res1Counter.setPositionPct(0.76,0);
		self.res1Counter.setSizePct(0.06,1);

		self.res2Counter = glass.GlassLabel("_12345__");
		self.add(self.res2Counter);
		self.res2Counter.setPositionPct(0.82,0);
		self.res2Counter.setSizePct(0.06,1);

		self.res3Counter = glass.GlassLabel("_12345__");
		self.add(self.res3Counter);
		self.res3Counter.setPositionPct(0.88,0);
		self.res3Counter.setSizePct(0.06,1);

		self.workerCounter = glass.GlassLabel("_12345__");
		self.workerCounter.setForegroundColor( white );
		self.add(self.workerCounter);
		self.workerCounter.setPositionPct(0.95,0);
		self.workerCounter.setSizePct(0.05,1);

		self.lastTime = Host_Milliseconds();
		self.trackGold = deque();
		self.trackStone = deque();
		self.lastStone = 0;
		self.lastGold = 0;
		
		self.healthBackground = glass.GlassLabel(" ");
		self.add(self.healthBackground);
		self.healthBackground.setPositionPct(0.4,0.05);
		self.healthBackground.setSizePct(0.2,0.9);
		self.healthBackground.setBackgroundColor(tangoRedDark);
		self.healthBackground.setOpaque(True);
		
		self.healthForeground = glass.GlassLabel(" ")
		self.add(self.healthForeground);
		self.healthForeground.setPositionPct(0.4,0.05);
		self.healthForeground.setSizePct(0.2,0.9);
		self.healthForeground.setBackgroundColor(tangoBlue);
		self.healthForeground.setOpaque(True);
		
		self.cc = glass.GlassLabel("");
		self.add(self.cc);
		self.cc.setSizePct(0,1);
		self.cc.setWidth(self.cc.getHeight());
		self.cc.setX( self.healthBackground.getX() - self.cc.getWidth() );

		gblEventHandler.addGameListener(self);
		
	def update(self):
		# Update the resources
		player = savage.getLocalPlayer();
		if player.isCommander() or cvar_getvalue("gui_showTeamStatus") == 1:
			self.setVisible(True);
		else:
			self.setVisible(False);
			return;

		myteam = savage.getLocalPlayer().getTeam();
		team = savage.Team(myteam);
		resources = team.getResources();
		race = team.getRace();

		working, total , max = team.getWorkerInfo();
		workerinfo =  str(working)+"/"+ str(total);
		self.teamGold.setCaption("^icon ../../gui/standard/icons/gold/gold_icon^ "+str(resources["gold"]));
		self.stoneCounter.setCaption("^icon ../../gui/standard/icons/redstone^ "+str(resources["stone"]));
		self.workerCounter.setCaption("^icon ../../gui/standard/comm/build_order^ "+str(workerinfo));

		if race == "beast":
			self.res1Counter.setCaption("^icon ../../gui/standard/icons/entropy^ "+str(resources["entropy"]));
			self.res1Counter.setForegroundColor(tangoGreenLight);
			self.res2Counter.setCaption("^icon ../../gui/standard/icons/strata^ "+str(resources["strata"]));
			self.res2Counter.setForegroundColor(tangoBlueLight);
			self.res3Counter.setCaption("^icon ../../gui/standard/icons/fire^ "+str(resources["fire"]));
			self.res3Counter.setForegroundColor(tangoRedLight);
		elif race == "human":
			self.res1Counter.setCaption("^icon ../../gui/standard/icons/magnetic^ "+str(resources["magnetic"]));
			self.res1Counter.setForegroundColor(tangoRedLight);
			self.res2Counter.setCaption("^icon ../../gui/standard/icons/electric^ "+str(resources["electric"]));
			self.res2Counter.setForegroundColor(tangoBlueLight);
			self.res3Counter.setCaption("^icon ../../gui/standard/icons/chemical^ "+str(resources["chemical"]));
			self.res3Counter.setForegroundColor(tangoGreenLight);

		currentTime = Host_Milliseconds();

		if currentTime  > ( self.lastTime + 10000 ):
			self.lastTime = currentTime;
			self.resetDiffCounters();
			dGold = sum(self.trackGold);
			dStone = sum(self.trackStone);
			dlen = len(self.trackGold);
			self.goldIncome.setCaption( ("%.2f" % (dGold/dlen)) + "/m");
			self.stoneIncome.setCaption( ("%.2f" % (dStone/dlen)) + "/m");
		
		cc = team.getCommandCenter();
		k = cc.getHealthPct();
		
		hue = (k-0.1)/2.7 if k > 0.1 else 0;
		
		self.healthForeground.setWidth(int(k*self.healthBackground.getWidth()));
		self.healthForeground.setBackgroundColor(tools.HSLColor(hue,0.8,0.66));
		w,h = self.cc.getWidth(), self.cc.getHeight();
		self.cc.setImage(cc.getType().getValue("mapIcon"));
		self.cc.setSize(w,h);
		
	def resetDiffCounters(self):
		resources = savage.getLocalTeam().getResources();
		self.trackStone.append(resources["stone"]-self.lastStone);
		self.trackGold.append(resources["gold"]-self.lastGold);
		self.lastGold = resources["gold"];
		self.lastStone = resources["stone"];
		#two minute rolling average
		if len(self.trackGold) > 12:
			self.trackGold.popleft();
			self.trackStone.popleft();

	def onEvent(self, e):
		resources = savage.getLocalTeam().getResources();
		if e.eventType == "player_join":
			self.lastGold = resources["gold"];
			self.lastStone = resources["stone"];
			self.trackGold.clear();
			self.trackStone.clear();
			self.goldIncome.setCaption( "%.2f" % (0.0) + "/m");
			self.stoneIncome.setCaption( "%.2f" % (0.0) + "/m");

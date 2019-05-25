#copyright (c) savagerebirth.com 2011
#this file generates the resource and cc health information at the top of the screen

import savage;
import glass;
from silverback import *;
import tools;

class ResourcePanel(glass.GlassContainer):
	def __init__(self):
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
		self.lastGold = 0;
		self.lastStone = 0;
		
		self.healthBackground = glass.GlassLabel(" ");
		self.add(self.healthBackground);
		self.healthBackground.setPositionPct(0.4,0.05);
		self.healthBackground.setSizePct(0.2,0.9);
		self.healthBackground.setBackgroundColor(tangoRedDark);
		self.healthBackground.setOpaque(1);
		
		self.healthForeground = glass.GlassLabel(" ")
		self.add(self.healthForeground);
		self.healthForeground.setPositionPct(0.4,0.05);
		self.healthForeground.setSizePct(0.2,0.9);
		self.healthForeground.setBackgroundColor(tangoBlue);
		self.healthForeground.setOpaque(1);
		
		self.cc = glass.GlassLabel("");
		self.add(self.cc);
		self.cc.setSizePct(0,1);
		self.cc.setWidth(self.cc.getHeight());
		self.cc.setX( self.healthBackground.getX() - self.cc.getWidth() );
		
	def update(self):
		# Update the resources
		player = savage.getLocalPlayer();
		if player.isCommander() or cvar_getvalue("gui_showTeamStatus") == 1:
			self.setVisible(1);
		else:
			self.setVisible(0);
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

		if currentTime  > ( self.lastTime + 1000 ):

			dt = float(currentTime - self.lastTime);
			dGold = resources["gold"] - self.lastGold;
			dStone = resources["stone"] - self.lastStone;
			self.goldIncome.setCaption( ("%.2f" % (dGold/dt*60.0)) + "/m");
			self.stoneIncome.setCaption( ("%.2f" % (dStone/dt*60.0)) + "/m");
			self.resetDiffCounters();
		
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
		self.lastTime = Host_Milliseconds();
		self.lastGold = resources["gold"];
		self.lastStone = resources["stone"];
	




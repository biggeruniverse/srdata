# (c) 2011 savagerebirth.com
# this file creates the stats window for a given player
from silverback import *;
import glass;
import savage;
			

class StatsWindow(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);

		self.widgetDict = dict(); # The main dict where all the widgets are stored to make updating easier

		self.playerStats = None;

		self.widgetDict["kills"] = [];
		self.widgetDict["deaths"] = [];
		self.widgetDict["assists"] = [];
		self.widgetDict["wins"] = [];
		self.widgetDict["losses"] = [];
		self.widgetDict["draws"] = [];

		self.setBackgroundColor(windowBackground);
		self.setFrameStyle("TrimmedEight");	
		# unified mainmenu content window size (so called modules)
		self.setSize(700, 400);

		# Standard top container:

		top = DefaultContainer();
		self.add(top, 0, 0);
		top.setSize(self.getWidth(), 35);
		top.setBackgroundColor(windowTop);

		
		self.username = DefaultLabel("Fetching stats...");
		self.username.setForegroundColor(tangoYellowDark);
		self.username.setFont(fontSizeLarge);
		top.add(self.username, 20, "bottom");

		self.widgetDict["name"] = self.username;

		self.rank = DefaultLabel("Administrator"); 
		# TODO: what ranks/titles do we have, and how do we separate forum and ingame ranks/titles?
		self.rank.setForegroundColor(glass.Color(214, 184, 139));
		#rank.setFont(fontSizeSmall);
		top.add(self.rank, self.username.getWidth() + 30, "bottom");

		self.widgetDict["custom_title"] = self.rank;

		self.accountCreated = DefaultLabel(" - Account created Aug 31, 2010");
		self.accountCreated.setForegroundColor(glass.Color(119, 95,74));
		self.accountCreated.setFont(fontSizeSmall);
		top.add(self.accountCreated, self.rank.getWidth() + self.rank.getX(), "bottom");

		contentLeft = DefaultContainer();
		contentLeft.setBackgroundColor(transparency);
		self.add(contentLeft, 0, 40);
		contentLeft.setSize(140, self.getHeight() - 35);

		# profile pic border hack:

		profilePicContainer = DefaultContainer();
		profilePicContainer.setBackgroundColor(windowTop);
		profilePicContainer.setSize(126, 126);
		contentLeft.add(profilePicContainer, "center", 10);

		self.profilePic = Avatar(cvar_get("username"));
		self.profilePic.setSize(profilePicContainer.getWidth() - 2, profilePicContainer.getHeight() - 2);
		profilePicContainer.add(self.profilePic, 1, 1); # 1px border, might increase it.

		# Recent matches coming soon...

		recentMatchesLabel = DefaultLabel("Recent Matches");
		contentLeft.add(recentMatchesLabel, profilePicContainer.getX(), profilePicContainer.getHeight() + profilePicContainer.getY() + 20);

		comingSoonLabel = DefaultLabel("Coming soon...");
		contentLeft.add(comingSoonLabel, profilePicContainer.getX(), recentMatchesLabel.getHeight() + recentMatchesLabel.getY() + 3);
		comingSoonLabel.setForegroundColor(glass.Color(119, 95, 74));


		# right container, containing the tabbed area...do I even need it?
		# could be handy if we have to push a message like restart or the return togame/disconnect thing.

		
		contentRight = DefaultContainer();
		self.add(contentRight, contentLeft.getWidth(), 40);
		contentRight.setSize(self.getWidth() - contentLeft.getWidth(), self.getHeight() - 35);
		#contentRight.setBackgroundColor(transparency);		


		# Make some tabs

		tabContainer = glass.GlassTabbedArea();
		contentRight.add(tabContainer, 10, 10);
		tabContainer.setSize(contentRight.getWidth() - 20, contentRight.getHeight() - 20);


		##### Summary #####

		summary = DefaultWindow(); # Somehow I can't add containers to a tabbed area...
		summary.setSize(tabContainer.getWidth() - 5, tabContainer.getHeight());	
		summary.setBackgroundColor(transparency);

		# hacky hacky
		frameContainer = DefaultContainer();
		frameContainer.setBackgroundColor(white);
		frameContainer.setSize(summary.getWidth() - 10, 122);
		summary.add(frameContainer, 5, 0);

		topContainer = DefaultContainer();
		topContainer.setBackgroundColor(glass.Color(14, 7, 7));
		topContainer.setSize(summary.getWidth(), 120);
		summary.add(topContainer, 0, 1);

		levelLabel = DefaultLabel("Account Level");
		levelLabel.setFont(fontSizeLarge);
		levelLabel.setForegroundColor(glass.Color(41, 121, 189));

		self.accountLevel = DefaultLabel("23");
		self.accountLevel.setFont(fontSizeLarge);
		
		topContainer.add(levelLabel, 10, 30);
		topContainer.add(self.accountLevel, levelLabel.getWidth() + 20, 30);

		lastSeenLabel = DefaultLabel("Last seen in-game:");
		lastSeenLabel.setForegroundColor(glass.Color(119, 95, 74));

		self.lastSeenValue = DefaultLabel("N/A");

		topContainer.add(self.lastSeenValue, topContainer.getWidth() - self.lastSeenValue.getWidth() - 10, 30);
		topContainer.add(lastSeenLabel, self.lastSeenValue.getX() - lastSeenLabel.getWidth() - 10, 30);

		progressContainer = DefaultWindow();
		progressContainer.setFrameStyle("TrimmedEight");
		progressContainer.setBackgroundColor(windowTop);
		progressContainer.setSize(topContainer.getWidth() - 20, 30);
		topContainer.add(progressContainer, 10, self.accountLevel.getY() + 35);

		self.level = glass.GlassProgressBar();
		self.level.setSize(progressContainer.getWidth(), progressContainer.getHeight());
		self.level.setForegroundColor(glass.Color(52, 101, 164, 128));
		self.level.setBackgroundColor(white);
		self.level.setBackgroundImage("gui/base/images/progress_bg.tga");
		progressContainer.add(self.level, 1, 1);

		self.xpLabel = DefaultLabel("00,000/20,000 XP");
		self.xpLabel.setFont(fontSizeLarge);
		progressContainer.add(self.xpLabel, "center", "center");
		
		winsContainer = DefaultContainer();
		winsContainer.setBackgroundColor(glass.Color(8, 3, 6));
		winsContainer.setSize((topContainer.getWidth() // 2) - 2, 70);

		winsSummaryLabel = DefaultLabel("Wins");
		winsSummaryLabel.setFont(fontSizeLarge);
		winsSummaryLabel.setForegroundColor(tangoYellowDark);

		winsValue = DefaultLabel("0");

		self.widgetDict["wins"].append(winsValue);

		winsContainer.add(winsSummaryLabel, "center", 15);
		winsContainer.add(winsValue, "center", 40);

		summary.add(winsContainer, "left", topContainer.getHeight() + 15);

		lossesContainer = DefaultContainer();
		lossesContainer.setBackgroundColor(glass.Color(8, 3, 6));
		lossesContainer.setSize(winsContainer.getWidth(), 70);

		lossesSummaryLabel = DefaultLabel("Losses");
		lossesSummaryLabel.setFont(fontSizeLarge);
		lossesSummaryLabel.setForegroundColor(tangoYellowDark);

		lossesValue = DefaultLabel("0");

		self.widgetDict["losses"].append(lossesValue);

		lossesContainer.add(lossesSummaryLabel, "center", 15);
		lossesContainer.add(lossesValue, "center", 40);

		summary.add(lossesContainer, "right", winsContainer.getY());

		killsValue = DefaultLabel("0");
		deathsValue = DefaultLabel("0");
		assistsValue = DefaultLabel("0");
		self.kdValue = DefaultLabel("todo");

		self.widgetDict["kills"].append(killsValue);
		self.widgetDict["deaths"].append(deathsValue);
		self.widgetDict["assists"].append(assistsValue);

		containersList = {"Kills": killsValue, "Deaths": deathsValue, "Assists": assistsValue, "K/D R.": self.kdValue};

		width = (winsContainer.getWidth() // 2) - 2;
		y = winsContainer.getHeight() + winsContainer.getY() + 5;

		for i, key in enumerate(containersList):
			bgContainer = DefaultContainer();
			bgContainer.setBackgroundColor(glass.Color(8, 3, 6));
			bgContainer.setSize(width, 70);
			summary.add(bgContainer, i * width + i * 6, y);

			lbl = DefaultLabel(key);
			lbl.setFont(fontSizeLarge);
			lbl.setForegroundColor(tangoYellowDark);
			bgContainer.add(lbl, "center", 15);
			bgContainer.add(containersList[key], "center", 40);


		##### General stats cell #####

		self.statsTable = DefaultTable();
		self.statsTable.horizontalJustification = glass.Graphics.LEFT;
		#self.statsTable.verticalJustification = DefaultTable.TOP;
		self.statsTable.setFrame(0);
		self.statsTable.setOpaque(1);
		self.statsTable.padding = 1;
		self.statsTable.autoAdjust = False;
		self.statsTable.setAlternate(1);
		self.statsTable.setBackgroundColor(glass.Color(42,16,12));

		# average column

		averageStatsLabel = DefaultLabel("Average");
		averageStatsLabel.setFont(fontSizeSmall);
		averageStatsLabel.setForegroundColor(glass.Color(214, 184, 139));

		youLabel = DefaultLabel("You");
		youLabel.setFont(fontSizeSmall);
		youLabel.setForegroundColor(glass.Color(214, 184, 139));

		general = DefaultLabel("General Statistics");
		general.setFont(fontSizeSmall);
		general.setForegroundColor(glass.Color(214, 184, 139));

		self.statsTable.addRow(general, youLabel, averageStatsLabel);
		#self.statsTable.nextRow("", "", averageStatsLabel);

		expLabel = DefaultLabel("#");
		avgExp = DefaultLabel("#");
		self.statsTable.addRow("Experience:", expLabel, avgExp);

		self.widgetDict["general_xp"] = expLabel;
		#self.widgetDict["average_xp"] = avgExp;

		winsLabel = DefaultLabel("#");
		avgWins = DefaultLabel("#");
		self.statsTable.addRow("Wins:", winsLabel, avgWins);

		self.widgetDict["wins"].append(winsLabel);
		#self.widgetDict["average_wins"] = avgWins;

		drawsLabel = DefaultLabel("#");
		avgDraws = DefaultLabel("#");
		self.statsTable.addRow("Draws:", drawsLabel, avgDraws);

		self.widgetDict["draws"].append(drawsLabel);
		#self.widgetDict["average_draws"] = avgDraws;

		lossesLabel = DefaultLabel("#");
		avgLosses = DefaultLabel("#");
		self.statsTable.addRow("Losses:", lossesLabel, avgLosses);

		self.widgetDict["losses"].append(lossesLabel);
		#self.widgetDict["average_losses"] = avgLosses;

		self.statsTable.addRow("", "", "");

		killsLabel = DefaultLabel("#");
		avgKills = DefaultLabel("#");
		self.statsTable.addRow("Kills:", killsLabel, avgKills);

		self.widgetDict["kills"].append(killsLabel);
		#self.widgetDict["average_kills"] = avgKills;

		assistsLabel = DefaultLabel("#");
		avgAssists = DefaultLabel("#");
		self.statsTable.addRow("Assists:", assistsLabel, avgAssists);

		self.widgetDict["assists"].append(assistsLabel);
		#self.widgetDict["average_assists"] = avgAssists;

		deathsLabel = DefaultLabel("#");
		avgDeaths = DefaultLabel("#");
		self.statsTable.addRow("Deaths:", deathsLabel, avgDeaths);

		self.widgetDict["deaths"].append(deathsLabel);
		self.widgetDict["average_deaths"] = avgDeaths;

		self.kdaLabel = DefaultLabel("#/#/#");
		self.averageKda = DefaultLabel("#/#/#");
		self.statsTable.addRow("Kills/Deaths/Assists:", self.kdaLabel, self.averageKda);

		self.statsTable.addRow("^yMore statistics coming soon.", "", "");


		#self.statsTable.adjustSizeTo(400);


		# Usage stats coming sonewhen...

		"""

		usageStats = DefaultTable();
		usageStats.setFrame(0);
		usageStats.setOpaque(1);
		usageStats.padding = 1;
		usageStats.autoAdjust = False;
		usageStats.setAlternate(0);
		usageStats.setBackgroundColor(glass.Color(42,16,12));

		usage = DefaultLabel("Usage Stats");
		usage.setForegroundColor(glass.Color(214, 184, 139));
		usageStats.horizontalJustification = glass.Graphics.LEFT;
		usageStats.addRow(usage, "");
		usageStats.horizontalJustification = glass.Graphics.CENTER;
		usageStats.nextRow("", "");

		horde = DefaultImage();
		horde.setImage("beasts_icon.png");
		horde.setSize(96,77);

		legion = DefaultImage();
		legion.setImage("humans_icon.png");
		legion.setSize(96,77);

		self.hordePct = DefaultLabel("###%");
		self.legionPct = DefaultLabel("###%");
		# need to calculate those too :(

		usageStats.addRow(horde, legion);
		usageStats.addRow(self.hordePct, self.legionPct);
		usageStats.addRow("", "");

		usageStats.horizontalJustification = glass.Graphics.LEFT;
		rewards = DefaultLabel("Recent Rewards:");
		rewards.setForegroundColor(glass.Color(214, 184, 139));
		usageStats.addRow(rewards, "");
		usageStats.addRow("", "");
		usageStats.addRow("Coming soon...");

		usageStats.adjustSizeTo(300, self.statsTable.getHeight());

		# Recent matches:

		recentMatches = DefaultTable();
		recentMatches.horizontalJustification = glass.Graphics.LEFT;
		#recentMatches.verticalJustification = DefaultTable.TOP;
		recentMatches.setFrame(0);
		recentMatches.setOpaque(1);
		recentMatches.padding = 1;
		recentMatches.autoAdjust = False;
		recentMatches.setAlternate(0);
		recentMatches.setBackgroundColor(glass.Color(42,16,12));


		# TODO
		recent = DefaultLabel("Recent Matches coming soon...")
		recent.setForegroundColor(glass.Color(214, 184, 139));
		row = recentMatches.addRow(recent, "");
		#row.getColumn(0).setColumnSpan(2);
		recentMatches.setColumnWidth(1, 32);

		recentMatches.nextRow("", "", "");

		recentMatches.setAlternate(1);
		
		self.matchesList = [];
		
		for i in xrange(3):
			pic = DefaultImage()
			pic.setImage("eden2_thumb.png");
			pic.setSize(32,32);

			matchID = DefaultLabel("Match #9999\nBeast Horde");
			matchID.setFont(fontSizeSmall);

			result = DefaultLabel("Win");
			recentMatches.addRow(pic, matchID, result);

			self.matchesList.append( [matchID, result] ); # maybe a dict would be better... todo

		recentMatches.adjustSizeTo(300, averageStats.getHeight());
		"""

		self.statsTable.adjustSizeTo( tabContainer.getWidth() - 20);		

		comingSoon = DefaultLabel("Coming soon...");

		tabContainer.addTab("Summary", summary);
		tabContainer.addTab("Detailed Stats", self.statsTable);
		tabContainer.addTab("Matches", comingSoon);
		tabContainer.addTab("Achievements", comingSoon);
		tabContainer.addTab("Rewards", comingSoon);

		# TODO

		#self.button = DefaultButton("test");
		#self.add(self.button, 0,0);
		#self.button.setClickAction("mainmenu.modules['stats'].playerStats.update();");

	def createStats(self, player):
		self.playerStats = PlayerStats(player);
		self.playerStats.addUpdateListener(self);
		self.playerStats.update();
		

	def buildStats(self):
		
		# Somewhen, I have to fix this. It's really bad relying on an exception here, but it works...
		for key in self.widgetDict:
			if key in self.playerStats.stats:
				# check if we have more than one label for a specific value:
				try:
					for lbl in self.widgetDict[key]:						
						lbl.setCaption(str(self.playerStats.stats[key]));
				except TypeError:
					self.widgetDict[key].setCaption(str(self.playerStats.stats[key]));

		# Update labels that need calculation:

		deaths = int(self.playerStats.stats["deaths"]);
		kills = int(self.playerStats.stats["kills"]);
		assists = int(self.playerStats.stats["assists"]);
		if deaths != 0:
			kd = kills / deaths;
			ad = assists / deaths;
			kda = str(kd)[:5] + "/1/" + str(ad)[:5];
		else:
			kd = kills;
			kda = str(kd)[:5] + "/0/" + str(assists)[:5];

		self.kdValue.setCaption(str(kd)[:5]);
		self.kdaLabel.setCaption(kda);

		#todo: calculate xp & level

		# refresh positions where needed:

		self.rank.setX(self.username.getWidth() + self.username.getX() + 15);
		self.accountCreated.setX(self.rank.getWidth() + self.rank.getX());

		"""

		humanTime =	int(self.playerStats.stats["human_time_played"]);
		beastTime = int(self.playerStats.stats["beast_time_played"]);

		#Fuck zero division...

		if humanTime == 0 and beastTime > 0:
			humanPct = "0.0%";
			beastPct = "100%";
		elif beastTime == 0 and humanTime >0:
			humanPct = "100%";
			beastPct = "0.0%";
		elif beastTime == 0 and humanTime == 0:
			humanPct = "0.0%";
			beastPct = "0.0%";
		else:
			humanPct = str( float(humanTime) / float(humanTime + beastTime) * 100 )[:3] + "%";
			beastPct = str( float(beastTime) / float(humanTime + beastTime) * 100 )[:3] + "%";

		self.legionPct.setCaption(humanPct);
		self.hordePct.setCaption(beastPct);

		# Recent matches:

		for i, match in enumerate(self.matchesList):
			match[0].setCaption("Match #" + str(self.playerStats.recentMatches[i][0]) + "\n" + 
								str(self.playerStats.recentMatches[i][3])
								);
			if int(self.playerStats.recentMatches[i][1]) == 0:
				if int(self.playerStats.recentMatches[i][2]) == 0:
					match[1].setCaption("Draw");
				else:
					match[1].setCaption("Loss");
			else:
				match[1].setCaption("Win");
		
		"""
	def updateStats(self):
		self.buildStats();
		self.profilePic.update();

	def onShow(self):
		if self.playerStats == None:
			self.createStats(cvar_getvalue('username'));
		else:
			self.playerStats.update();


class PlayerStats:
	def __init__(self, playerId):
		self.playerId = playerId;
		self.listeners = [];

		self.stats = dict();
		self.recentMatches = [];

		self.httpHandle = -1;

		gblEventHandler.addHttpListener(self);

	def addUpdateListener(self, listener):
		self.listeners.append(listener);

	def update(self):
		self.httpHandle = HTTP_Get("http://savagerebirth.com/api/user/" + str(self.playerId) + "/summary"); #cvar_get("auth_requesturl")+"/user/"+str(self.playerId) + "/summary");

	def onEvent(self, e):
		if e.handle == self.httpHandle:				
			self.httpHandle = -1;
			if e.responseCode != 200:
				return;
			dom = xml.dom.minidom.parseString(e.responseMessage);

			# resetting stats and matches
			self.stats = {};
			self.recentMatches = [];

			# adding name:
			self.stats["name"] = dom.documentElement.getAttribute("name");

			for node in dom.getElementsByTagName("player").item(0).childNodes:
				self.stats[node.tagName] = node.getAttribute("value");

			for node in dom.getElementsByTagName("recent_matches").item(0).childNodes:

				self.recentMatches.append( [
											   node.getAttribute("match_id"), #match id
											   node.getAttribute("win"), #win
											   node.getAttribute("loss"), #loss
											   node.getAttribute("race")  #race
											]);

			dom.unlink();
			for listener in self.listeners:
				listener.updateStats();

			self.httpHandle = -1;




stats = StatsWindow();
mainmenu.addModule("stats", stats);



"""
def frame():
	pass;

def onShow():
	pass;

screen = glass.GUI_CreateScreen("stats");

class StatsWindow(glass.GlassWindow):
	def __init__(self, playerName):
		glass.GlassWindow.__init__(self, playerName+" Stats & Rankings");
		self.httpHandle = -1;
		self.player = playerName;
		self.setBackgroundColor(glass.Color(0,0,0,128));
		self.spinner = glass.GlassLabel();
		self.spinner.setImage("textures/econs/loading/loading0000.s2g");
		self.spinner.setSize(32,32);
		self.add(self.spinner);

		self.title = glass.GlassLabel(self.player+" Stats & Rankings");
		self.add(self.title);

		#create the tabs
		self.tabs = glass.GlassTabbedContainer();
		self.tabs.setOpaque(0)
    
		self.add(self.tabs)
		self.tabs.setSizePct(1,.9)

		self.setTitleVisible(0);
		
		button = glass.GlassButton("Close");
		self.add(button);
		button.addActionListener(self);

		gblEventHandler.addHttpListener(self);

	def show(self, player = None):
		if player is not None:
			self.player = player;
		self.httpHandle = HTTP_Get(cvar_get("auth_requesturl")+"/user/"+self.player);
		self.spinner.setVisible(1);
		self.tabs.setVisible(0);
		self.spinner.setPosition(self.getWidth()/2-16, self.getHeight()/2-16);
		self.title.setCaption("^y"+self.player+" ^wStats & Rankings");
		self.title.setPosition(self.getWidth()/2-self.title.getWidth()/2, 1);
		self.setVisible(1);

	def buildStats(self, xml):
		con_println(xml+"\n");

	def onAction(self, e):
		self.releaseModalFocus();
		self.setVisible(0);

	def onEvent(self, e):
		if e.handle == self.httpHandle:
			if e.responseCode != 200:
				return;
			self.spinner.setVisible(0);
			self.httpHandle = -1;

			self.buildStats(e.responseMessage);
			self.spinner.setVisible(0);
			self.tabs.setVisible(1);

statsWindow = StatsWindow("DieOrFail");
statsWindow.setPositionPct(0.1,0.1);
statsWindow.setSizePct(0.8,0.8);
glass.GUI_ScreenAddWidget("stats", statsWindow);

totalsIndex = {"Username":None, "Nickname":None};
def buildTable(dict):
	table = GlassTablePlus()
	table.setFrame(0)
	for name in dict.keys():
		data = glass.GlassLabel("Loading")
		table.addLabelledRow(name,  data)
		dict[name] = data
	return table
"""

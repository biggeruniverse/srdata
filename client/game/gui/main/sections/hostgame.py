# (c) 2011 savagerebirth.com

import mainmenu;
from silverback import *;
import glass;
import xml.dom.minidom;
import tools;

class HostGameSection(AbstractSection):
	
	def __init__(self):
		AbstractSection.__init__(self);
	   
		
	def onShow(self):

		self.getLocalMaps();
		self.mapList.setSelected(0);

		if isConnected():
			self.reconnectBar.setVisible(1);
			self.content.setY(85);
		else:
			self.reconnectBar.setVisible(0);
			self.content.setY(35);
		
	def create(self):
		
		self.setBackgroundColor(glass.Color(22, 13, 10));
		
		# Top area
		top = DefaultContainer();
		top.setSize(self.getWidth(), 35);
		top.setBackgroundColor(glass.Color(85, 21, 11));
		top.setOpaque(1);
		self.add(top);		
		
		title = DefaultImage();
		title.setImage("txt_hostgame.png");
		top.add(title, "center", "center");
		
		go = DefaultImageButton();		
		go.setImage("btn_host.png");
		go.setCaption("Host");
		go.addActionListener(self)
		top.add(go, 10, "center", "right"); 

		# return to game stuff:

		self.reconnectBar = DefaultContainer();
		self.reconnectBar.setSize(self.getWidth(), 50);
		self.reconnectBar.setVisible(0);
		self.reconnectBar.setBackgroundColor(glass.Color(85, 21, 11));
		self.reconnectBar.setOpaque(1);
		self.add(self.reconnectBar, 0, 35);
		
		gameProgress = DefaultLabel("GAME IN PROGRESS");
		self.reconnectBar.add(gameProgress, "center");
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		self.reconnectBar.add(hr, "center", gameProgress.getHeight() + 3);

		disconnectButton = DefaultButton("LEAVE");
		disconnectButton.setClickAction("""disconnect();mainmenu.modules['menu'].sectionStack['serverlist'].onShow();""");
		self.reconnectBar.add(disconnectButton, 10, 10);

		connectedMessage = DefaultLabel("You are currently connected to a server. Do you want to return?");
		connectedMessage.setFont(fontSizeSmall);
		self.reconnectBar.add(connectedMessage, "center", 27);
		
		returnButton = DefaultButton("RETURN");
		returnButton.setClickAction("spechud.setMode('lobby');GUI_ShowScreen('spechud')");
		self.reconnectBar.add(returnButton, 10, 10, "right");

		self.content = DefaultContainer();
		self.add(self.content, 0, 35);
		self.content.setSize(self.getWidth(), self.getHeight() - 85);

		self.columnWidth = (self.getWidth() - 40) // 3;

		# Left container:

		self.settingsContainer = DefaultContainer();
		self.content.add(self.settingsContainer, 10, 0);
		self.settingsContainer.setSize(self.columnWidth, self.content.getHeight());
		#self.settingsContainer.setBackgroundColor(white);

		settingsTitle = DefaultLabel("Game Settings");
		self.settingsContainer.add(settingsTitle, "center", 10);

		typeLabel = DefaultLabel("Gametype:");
		self.settingsContainer.add(typeLabel, 0, settingsTitle.getHeight() + 30 );

		cvar_register("sv_gametype", 0);
		self.gametype = glass.GlassDropMenu();
		self.gametype.linkCvar("sv_gametype");
		self.gametype.addOption("RTSS",str(GAMETYPE_RTSS));
		self.gametype.addOption("Duel",str(GAMETYPE_DUEL));	
		self.gametype.setSelectedValue("0");
		self.settingsContainer.add(self.gametype, typeLabel.getWidth() + 20, typeLabel.getY());
		self.gametype.setWidth(60);

		raceLabel = DefaultLabel("Races:");
		self.settingsContainer.add(raceLabel, 0, self.gametype.getY() + 30 );

		cvar_register("sv_team1race", 0, "human");
		cvar_register("sv_team2race", 0, "beast");
		self.race = glass.GlassDropMenu();
		self.race.linkCvar("sv_team1race");
		self.race.addOption("HvsB","human");
		self.race.addOption("HvsH","human");
		self.race.addOption("BvsB","beast");
		self.race.setSelectedValue("HvsB");
		self.settingsContainer.add(self.race, self.gametype.getX(), raceLabel.getY());
		self.race.setWidth(60);

		div1 = DefaultDivider();
		div1.setWidth(self.settingsContainer.getWidth());
		self.settingsContainer.add(div1, 0, self.race.getY() + 40);

		cvar_register("sv_xp_mult", 0, "1.0");
		xpSlider = DefaultSlider();
		xpSlider.linkCvar("sv_xp_mult");
		xpSlider.setScaleEnd(10.0);
		xpSlider.setScaleStart(0.0);
		xpSlider.setWidth(self.settingsContainer.getWidth() - 15);
		self.settingsContainer.add(xpSlider, 0, div1.getY() + 25 );

		xpLabel = DefaultLabel("XP multiplier");
		self.settingsContainer.add(xpLabel, 0, xpSlider.getY() + 13 );	

		div2 = DefaultDivider();
		div2.setWidth(self.settingsContainer.getWidth());
		self.settingsContainer.add(div2, 0, xpLabel.getY() + 35);	

		cvar_register("sv_gold_mult", 0, "1.0");
		goldSlider = DefaultSlider();
		goldSlider.linkCvar("sv_gold_mult");
		goldSlider.setScaleEnd(10.0);
		goldSlider.setScaleStart(0.0);
		goldSlider.setWidth(self.settingsContainer.getWidth() - 15);
		self.settingsContainer.add(goldSlider, 0, div2.getY() + 25 );

		goldLabel = DefaultLabel("Gold multiplier");
		self.settingsContainer.add(goldLabel, 0, goldSlider.getY() + 13 );


		# mid container:

		self.listContainer = DefaultContainer();
		self.content.add(self.listContainer, self.columnWidth + 20, 0);
		self.listContainer.setSize(self.columnWidth, self.content.getHeight());
		#self.listContainer.setBackgroundColor(white);

		mapsTitle = DefaultLabel("Local Map List");
		self.listContainer.add(mapsTitle, "center", 10);

		self.mapList = glass.GlassListBox();	
		self.mapList.addSelectionListener(self);
		self.mapList.setBackgroundColor(transparency);
		self.mapList.setForegroundColor(glass.Color(211, 201, 168));
		#self.mapList.setSelectionColor()

		self.mapScroll = glass.GlassScrollArea(self.mapList);			
		self.mapScroll.setSize(self.listContainer.getWidth(), self.listContainer.getHeight() - 60);
		self.listContainer.add(self.mapScroll, 0, mapsTitle.getHeight() + 30);

		# right container:

		self.mapContainer = DefaultContainer();
		self.content.add(self.mapContainer, self.columnWidth * 2 + 30, 0);
		self.mapContainer.setSize(self.columnWidth, self.content.getHeight());
		#self.mapContainer.setBackgroundColor(white);

		self.overhead = glass.GlassLabel();
		#self.overhead.setImage("");
		self.overhead.setSize(self.mapContainer.getWidth(), self.mapContainer.getWidth());
		self.mapContainer.add(self.overhead, "center", self.mapScroll.getY());

		# todo: map stats and information

		comingSoon = DefaultLabel("Map stats and information \ncoming soon!");
		self.mapContainer.add(comingSoon, 0, self.overhead.getHeight() + 70);

		self.getLocalMaps();

	def getLocalMaps(self):
		self.mapList.clear();
		paths = File_ListFiles("/world","*.s2z",0);
		for path in paths:
			name = path.rsplit("/",1)[1][:-4];
			self.mapList.addItem(name);
		
	def onAction(self, e):
		if e.widget.getCaption() == "Host":
			gameMap = self.mapList.getItem(self.mapList.getSelected());
			loading.setWorld(gameMap);
			World_Load(gameMap);

	def onValueChanged(self, e):
		value = e.widget.getItem(e.widget.getSelected());
		overheadPath = "/world/" + value + "_overhead.jpg";
		Host_VerifyOverhead(overheadPath);
		self.overhead.setImage(overheadPath, 1);
		self.overhead.setSize(self.mapContainer.getWidth(), self.mapContainer.getWidth());

		
mainmenu.modules["menu"].addSection("hostgame", HostGameSection());

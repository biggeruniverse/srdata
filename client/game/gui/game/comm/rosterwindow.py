from silverback import *;
import glass;

class CommRosterWindow(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		self.setFrameStyle("TrimmedEight");
		self.setMovable(1);

		self.setSize(500, 300);
		self.setVisible(0);
		
		self.players = [];

		self.setBackgroundColor(windowBackground);

		# top bar:

		top = DefaultContainer();
		top.setSize(self.getWidth(), 35);
		top.setBackgroundColor(windowTop);
		self.add(top);

		title = DefaultLabel("Player Roster");
		title.setForegroundColor(tangoYellow);
		title.setFont(fontSizeLarge);
		top.add(title, "center", "center");
		
		self.list = DefaultTable();
		self.list.setFrame(0);
		self.clearList();	
		# self.add(self.list,0,0)
		
		self.scroll = glass.GlassScrollArea(self.list);
		self.scroll.setSize(self.getWidth() - 5, self.getHeight() - 10);
		self.scroll.setBackgroundColor(transparency);
		self.add(self.scroll, 0, 42);

		self.build();	

		gblEventHandler.addGameListener(self);
		
	def clearList(self):
		self.list.erase()


		level = DefaultLabel("");
		level.setImage("/gui/standard/comm/upgrade_stronghold.s2g");
		level.setSize(24,24);

		#kda = glass.GlassLabel();
		#kda.setFont(fontSizeLarge);
		#kda.setCaption("^icon ../../gui/game/images/kills^/^icon skull_red^/^icon skull_green^ ");
		#kda.setAlignment(1);
		#kda.adjustSize();

		req = DefaultImageButton();
		req.setImage("request.s2g");
		req.setSize(24,24);

		gold = DefaultLabel("");
		gold.setImage("/gui/standard/icons/gold/gold_icon.s2g");
		gold.setSize(24,24); 

		#self.headingRow = self.list.nextRow( empty, "", level, kda, req, empty, gold, empty);
		#self.headingRow.setBackgroundColor(glass.Color(35,20,16));

		self.headingRow = self.list.nextRow("", "", level, "^icon ../../gui/game/images/kills^/^icon skull_red^/^icon skull_green^ ",
                                            req, "", gold, "");

		self.headingRow.setFocusable(0);		

		#for i in xrange(2,6):
		#	self.list.setColumnWidth(i, 80);

		#row = self.list.nextRow(DefaultDivider());
		#row.getColumn(0).setColumnSpan(8);
		
	def build(self):
		self.clearList()
		
		self.team = savage.getLocalTeam();
		self.players = []
		
		self.playerDict = dict();
		i = 0;

		for player in self.team.getPlayers():

			if player.isCommander():
				continue;

			self.players.append(player);
			i += 1;

			unit = glass.GlassLabel();
			unit.setImage(player.getIcon());
			unit.setSize(24,24);			
				
			name = DefaultLabel(player.getFormattedName());
			#name.setForegroundColor( white );
			#name.setAlignment(2);									
				
			level = DefaultLabel(str(player.getLevel()));
			level.setForegroundColor( tangoBlue );
			#level.setAlignment(2);
			#level.setFont(fontSizeLarge);


			kda = DefaultLabel("^g" + str(player.getKills()) + "^w/^r" + 
										str(player.getDeaths()) + "^w/^l" + str(player.getAssists()))
			#kda.setAlignment(2);
			#kda.setFont(fontSizeLarge);	
			#kda.adjustSize();		
				
			request = glass.ImageButton();
			#request.setSize(24,24);
			request.setImage("/gui/main/images/yestr.s2g");			
			request.setSize(24,24);
				
			officer = glass.ImageButton();
			#officer.setSize(24,24);
			if player.isOfficer():
				officer.setImage("gui/game/images/demote_"+self.team.getRace()+".s2g");
				officer.setClickAction("CL_RequestDemote(" + str(player.objectId) + ")");
			else:				
				officer.setImage("gui/game/images/promote_"+self.team.getRace()+".s2g");
				officer.setClickAction("CL_RequestPromote(" + str(player.objectId) + ")");
					
			officer.setSize(24,24);
				
			goldLabel = DefaultLabel(str(player.getGold()));
			goldLabel.setForegroundColor( themeGold);
			#goldLabel.setAlignment(1);
				
			gold = glass.ImageButton();
			#gold.setSize(24,24);
			gold.setImage("/gui/standard/icons/gold/nl_coins14.s2g");
			gold.setClickAction("CL_RequestGiveGold("+str(player.objectId) + ", 100)");
			gold.setSize(24,24);
				
			row = self.list.nextRow(unit, name, level, kda, request, officer, goldLabel, gold);

			self.playerDict[player.objectId] = row #Store the rows and players in a dict to trace back the widgets

		#self.list.adjustSize();
		#self.setSize(self.list.getWidth() +10, 250);
		#self.list.adjustJustification();	
		#self.setSize(self.list.getWidth() +10, 250);
		#self.scroll.setSize(self.getWidth(), self.getHeight());

		self.list.useColumnDividers();
		self.headingRow.setAlternate(0);
		self.list.adjustWidthTo(self.scroll.getWidth()-10);

	def updateCount(self):
		for player in self.players:
				kda = self.playerDict[player.objectId].getColumn(3).getContent(glass.GlassLabel);
				kda.setCaption("^g" + str(player.getKills()) + "^w/^r" + 
									str(player.getDeaths()) + "^w/^l" + str(player.getAssists()));

	def updatePictures(self):
		for player in self.players:
			officer = self.playerDict[player.objectId].getColumn(5).getContent(glass.ImageButton);
			if player.isOfficer():				
				officer.setImage("/gui/game/images/demote_"+self.team.getRace()+".s2g");
				officer.setSize(24,24);
				officer.setClickAction("CL_RequestDemote(" + str(player.objectId) + ")");
			else:
				officer.setImage("/gui/game/images/promote_"+self.team.getRace()+".s2g");
				officer.setSize(24,24);
				officer.setClickAction("CL_RequestPromote(" + str(player.objectId) + ")");
			unit = self.playerDict[player.objectId].getColumn(0).getContent(glass.GlassLabel);
			unit.setImage(player.getIcon());
			unit.setSize(24,24);
		#self.list.adjustSize();
		#self.setSize(self.list.getWidth() +10, 250);
		#self.list.adjustJustification();
				
	def updateRequests(self):
		for player in self.players:
			pass;
			
	def toggle(self):
		if self.isVisible():
			self.setVisible(0);
		else:
			self.build();
			self.setVisible(1);		
			
	def onEvent(self, e):
		if e.eventType == "player_join" or e.eventType == "player_leave":
			self.build(); # Builds the complete window new, could be made more efficient 
		elif e.eventType == "obituary":
			self.updateCount();
		elif e.eventType == "promoted" or e.eventType == "demoted":
			self.updatePictures();

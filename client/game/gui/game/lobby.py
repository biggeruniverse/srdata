# Copyright (c) 2012 savagerebirth.com 
# Define a lobby window for use in the spechud

from silverback import *;
import glass;
import savage;

def lobbyShowCorrectScreen(status):
	if status == PLAYER_STATUS_LOBBY:
		CL_RequestLoadout();
	elif status == PLAYER_STATUS_UNITSELECT:
		GUI_ShowScreen('loadout');
	elif status == PLAYER_STATUS_PLAYER:
		GUI_ShowScreen('hud');
	elif status == PLAYER_STATUS_COMMANDER:
		GUI_ShowScreen('commhud');
	elif status == PLAYER_STATUS_SPECTATE:
		spechud.setMode('hud');GUI_ShowScreen('spechud')

class LobbyWindow(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		
		self.setSize(1000, 700);
		self.setPosition(screenWidthPct(.5)-500, screenHeightPct(.5)-350);
		self.setFrameStyle("TrimmedEight");
		self.setBackgroundColor(glass.Color(40,20,20));

		# todo: check how many teams the map/server supports!
		totalTeamList = [savage.Team(1), savage.Team(2)];

		self.teamContainerList = [];

		self.currentTeam = 1; #0,1,2,3,4 ...

		dotString = ""
		for team in totalTeamList:
			teamList = TeamList(team, "left", int(self.getWidth()*0.45), int(self.getHeight()*0.7));
			self.add(teamList);
			teamList.setY(int(self.getHeight() * 0.0714));
			self.teamContainerList.append(teamList);
			dotString += " 0 ";

		# TODO: Use images and a container!
		self.dots = DefaultLabel(dotString);
		self.add(self.dots, self.getWidth()//2 - self.dots.getWidth()//2, int(self.getHeight()*0.73));

		self.switchTeams("left"); 

		# Spec button
		self.specButton = DefaultButton("Spectators");
		self.add(self.specButton, self.getWidth()//2 - self.specButton.getWidth()//2, 10);
		self.specButton.addActionListener(self);

		# Spec Window:
		self.specWindow = DefaultWindow();		
		self.specWindow.setBackgroundColor(glass.Color(70,20,20));
		self.add(self.specWindow);
		self.specWindow.setSizePct(0.15, 0.4);
		self.specWindow.setPosition(self.getWidth()//2 - self.specWindow.getWidth()//2, self.specButton.getY()+ self.specButton.getHeight() + 10)
		self.specWindow.setVisible(False);

		joinSpec = DefaultButton("Enlist now");
		joinSpec.setWidth(self.specWindow.getWidth());
		joinSpec.setClickAction("CL_RequestTeam(0);spechud.setMode('hud');setMouseMode(MOUSE_RECENTER)");
		self.specWindow.add(joinSpec, self.specWindow.getWidth()//2 - joinSpec.getWidth()//2, 0);

		#Fuck lists, they're buggy if you don't put them in their own container:

		specListContainer = DefaultContainer();
		specListContainer.setSize(self.specWindow.getWidth(), self.specWindow.getHeight() - joinSpec.getHeight()- 5);
		self.specWindow.add(specListContainer, 0, joinSpec.getHeight() + 5);

		self.specList = DefaultTableList();
		self.specList.setSelectionColor(glass.Color(70, 40, 40, 180));		
		specListContainer.add(self.specList);		

		specScroll = glass.GlassScrollArea(self.specList);
		specScroll.setBackgroundColor(transparency);
		specScroll.setHorizontalScrollPolicy(glass.GlassScrollArea.SHOW_NEVER);	
		specListContainer.add(specScroll, 0, 0);
		specScroll.setSize(specListContainer.getWidth(), specListContainer.getHeight());		

		# Move in/out animation?

		# Chatbox

		chatContainer = DefaultContainer();
		self.add(chatContainer);	
		chatContainer.setPositionPct(0.25, 0.78);	
		chatContainer.setSizePct(0.5, 0.2);
		chatContainer.setBackgroundColor(glass.Color(0,0,0,128));

		self.chatBox = HUDChatBox();		
		chatContainer.add(self.chatBox);		
		self.chatBox.setSizePct(1, 1);
		self.chatBox.resize();
		self.chatBox.alwaysShowInput(True);
		self.chatBox.inputType.setVisible(False);
		self.chatBox.buffer.setVisible(False);
		self.chatBox.historyBuffer.parentScroll.setVisible(True);
		self.chatBox.historyBuffer.parentScroll.setAutoscroll(True); # TODO: Fix auto scroll

		# Leave button 
		leave = DefaultButton("<< Menu");
		leave.setClickAction("GUI_ShowScreen('mainmenu')");
		self.add(leave);
		leave.setPositionPct(0.1, 0.9);

		# Play button, only shown if you're on a team
		self.play = DefaultButton("Play >>");
		self.play.addActionListener(self);
		self.add(self.play);
		self.play.setPosition(int(self.getWidth()*0.9) - self.play.getWidth(), int(self.getHeight()*0.9));

	def switchTeams(self, direction):
		if direction == "left" and self.currentTeam > 0:
			team1 = self.currentTeam - 1;
		elif direction == "right" and self.currentTeam < len(self.teamContainerList) - 2:
			team1 = self.currentTeam + 1;
		else:
			return;

		self.currentTeam = team1;
		team2 = team1 + 1;

		dotString = "";

		for i, teamList in enumerate(self.teamContainerList):
			if i == team1:
				teamList.setVisible(True);
				teamList.setX(self.getWidth()//2 - teamList.getWidth() - 10);
				teamList.changeSide("left");
				dotString += " ^icon ../../gui/game/images/roundhi^ ";
			elif i == team2:
				teamList.setVisible(True);
				teamList.setX(self.getWidth()//2 + 10);
				teamList.changeSide("right");
				dotString += " ^icon ../../gui/game/images/roundhi^ ";
			else:
				teamList.setVisible(False);
				dotString += " ^icon ../../gui/game/images/round^ ";

		self.dots.setCaption(dotString);
		#self.dots.adjustSize();

	def setVisible(self, value):
		if value == True or value == 1:
			self.build();
		if savage.getLocalTeam().teamId != 0:
			self.play.setVisible(True);
		else:
			self.play.setVisible(False);

		DefaultWindow.setVisible(self, value);

	def build(self):
		for teamList in self.teamContainerList:
			teamList.build();
			if len(self.teamContainerList) < 3:
				teamList.scrollTeamsArrow.setVisible(False);

		self.specList.erase();
		for player in savage.Team(0).getPlayers():
			self.specList.nextRow(player.getFormattedName());
		try:
			self.specList.setColumnWidth(0,self.specWindow.getWidth() - 10);
			self.specList.adjustWidthTo(self.specWindow.getWidth() - 10);
		except ZeroDivisionError:
			con_println("ZeroDivisionError: Trying to call adjustWidthTo() on an empty table!\n")

	def toggleSpecList(self):
		# for now, just make it visible:
		if self.specWindow.isVisible():
			self.specWindow.setVisible(False);
		else:
			self.specWindow.setVisible(True);

	def onAction(self, e):
		if e.widget.getCaption() == "Spectators":
			self.toggleSpecList();
		elif e.widget.getCaption().startswith("Play"):
			status = savage.getLocalPlayer().getStatus();
			lobbyShowCorrectScreen(status);

	def onEvent(self, e):
		# update lists
		# update kills??
		# update commander/officer
		pass

	def update(self):
		for teamlist in self.teamContainerList:
			teamlist.update()

class TeamList(DefaultContainer):
	def __init__(self, team, side, w, h):
		DefaultContainer.__init__(self);
		#self.setBackgroundColor(glass.Color(0,0,0,128));
		self.team = team

		self.setSize(w, h);

		self.side = side; #Is it on the left or right?
		self.rowPlayerDict = {}; # {row: player}		

		self.kills = DefaultLabel("^icon ../../gui/game/images/kills^^g999"); #str(self.team.getKills()));
		#self.kills.setWidth(int(self.getWidth()*0.15));
		self.add(self.kills);		

		self.description = DefaultLabel("");
		self.add(self.description);
		if self.team.getRace() == "human":
			self.description.setCaption("The Legion of Man");
		else:
			self.description.setCaption("The Beast Horde");

		self.scrollTeamsArrow = glass.ImageButton();
		self.scrollTeamsArrow.setClickAction("spechud.lobby.switchTeams('"+ self.side + "')");
		self.add(self.scrollTeamsArrow);

		self.comm = DefaultLabel("Comm: ^rNO COMMANDER");		

		self.listContainer = DefaultContainer();		
		self.listContainer.setBackgroundColor(glass.Color(0,0,0,128));
		self.add(self.listContainer);
		self.listContainer.setSizePct(0.8, 0.9);

		self.list = DefaultTableList();
		self.list.padding = 5
		self.list.setSelectionColor(glass.Color(70, 40, 40));		
		self.listContainer.add(self.list, 0, 0);

		self.enlist = DefaultButton("Enlist now!");	
		self.enlist.setClickAction("CL_RequestTeam("+str(team.teamId)+");CL_RequestLoadout();");
		self.enlist.setHeight(self.list.getRowHeight());
		self.enlist.setWidth(self.listContainer.getWidth());	

		self.scroll = glass.GlassScrollArea(self.list);
		self.scroll.setBackgroundColor(transparency);
		self.scroll.setSize(self.listContainer.getWidth(), self.listContainer.getHeight());
		self.scroll.setHorizontalScrollPolicy(glass.GlassScrollArea.SHOW_NEVER);

		self.listContainer.add(self.scroll, 0, 0);

		# build and position everything:
		self.build();
		self.changeSide(self.side);

	def build(self):
		self.list.erase();
		self.rowPlayerDict = {};

		w = self.listContainer.getWidth() // 7

		players = self.team.getPlayers();

		commRow = self.list.nextRow( self.comm);
		enlistRow = self.list.nextRow(self.enlist);

		if len(players) == 0:			
			self.list.adjustWidthTo(self.listContainer.getWidth());
			self.comm.setCaption("Comm: ^rNO COMMANDER")
			return;

		commRow.getColumn(0).setColumnSpan(2);
		commRow.setFocusable(False);
		enlistRow.getColumn(0).setColumnSpan(4);	
		enlistRow.setFocusable(False);

		self.kills.setCaption("^icon ../../gui/game/images/kills^^g%d/^r%d/^y%d" % (self.team.getKills(),self.team.getDeaths(), self.team.getAssists()));
		
		for player in players:
			if player.isCommander():
				self.comm.setCaption("Comm: " + player.getFormattedName());
				continue;
			name = DefaultLabel(player.getFormattedName());
			row = self.list.nextRow(name, "^g" + str(player.getKills()), "^r" + str(player.getDeaths()), "^l" + str(player.getAssists()));
			self.rowPlayerDict[row] = player;
		

		self.list.setColumnWidth(0, w*4);
		self.list.setColumnWidth(1, w);
		self.list.setColumnWidth(2, w);
		self.list.setColumnWidth(3, w);
		self.list.adjustWidthTo(self.listContainer.getWidth());

	def changeSide(self, side):		
		self.side = side
		self.scrollTeamsArrow.setClickAction("spechud.lobby.switchTeams('"+ self.side + "')");
		if self.side == "left":					
			self.description.setPosition(self.getWidth() //2 - self.description.getWidth()//2, 0);
			self.listContainer.setPosition(int(self.getWidth() * 0.2), self.kills.getHeight());
			self.scrollTeamsArrow.setImage("gui/game/images/arrow_left.tga");
			self.scrollTeamsArrow.setSize(self.getWidth() - self.listContainer.getWidth() - 10, int(self.listContainer.getWidth()*0.7));
			self.scrollTeamsArrow.setPosition(0, self.getHeight()//2 - self.scrollTeamsArrow.getHeight()//2);
			self.kills.setPosition(self.listContainer.getX() - self.kills.getWidth(),0);	
		else:
			self.description.setPosition(self.getWidth()//2 - self.description.getWidth()//2, 0);		
			self.listContainer.setPosition(0, self.kills.getHeight() );
			self.kills.setPosition(self.listContainer.getWidth(), 0);
			self.scrollTeamsArrow.setImage("gui/game/images/arrow_right.tga");
			self.scrollTeamsArrow.setSize(self.getWidth() - self.listContainer.getWidth() - 10, int(self.listContainer.getWidth()*0.7));
			self.scrollTeamsArrow.setPosition(self.getWidth()-self.scrollTeamsArrow.getWidth(), self.getHeight()//2 - self.scrollTeamsArrow.getHeight()//2);
		
			
	def update(self):
		self.kills.setCaption("^icon ../../gui/game/images/kills^^g%d/^r%d/^y%d" % (self.team.getKills(),self.team.getDeaths(), self.team.getAssists()));

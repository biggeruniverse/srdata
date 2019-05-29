# (c) 2010 savagerebirth.com

from silverback import *;
import savage;
import glass;
import math;

class TeamScore(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		self.setSizePct(.9, .9);
		self.setPositionPct(.05, 0.05);
		self.build();
		self.setTitleVisible(False);
		self.setTitleBarHeight(0);
		self.setBackgroundColor(transparency);
		self.setVisible(False);
		

	#called when we want to update the window
	def update(self):
		teamsList = [[],[],[],[],[],[],[],[],[]];
		
		
		players = savage.getPlayers();
		for p in players:
			teamsList[p.getTeam()].append(p);

		#self.world.setCaption(cvar_get("world_name"));
		#self.world.adjustSize();
		#self.world.setFont(fontSizeLarge);
		#self.world.setX( (self.getWidth() - self.world.getWidth())//2 )
	
		#fire a request for scores
		CL_RequestScores();

		# clear tables, add up team scores as players are added to the tables

		for team in range(1,int(cvar_getvalue("sv_numteams"))):

			tableWin = self.tables[ team ];
			table = tableWin.table;
			comm = tableWin.comm;
			teamLabel = tableWin.teamLabel;
			

			currentTeam = teamsList[team];
			teamObj = savage.Team(team);
			tmk = 0
			tmd = 0
			rowCount = 1;
			playerCount = len(teamsList[team]);

			comm.setCaption("^555Commander: ^rNo Commander!");
			teamLabel.setCaption("^555Team " + str(team) + " ^w" + teamObj.getRace());
			i=0;
			while i < playerCount:
				p = currentTeam[i];
				
				row = table.getRow(rowCount);
				row.setVisible(True);

				tmk += p.getKills();
				tmd += p.getDeaths();
				
				rank, name, level, kills, deaths, assists, ping = [
				  table.getWidget(rowCount, k, type=glass.GlassLabel) for k in range(7)
				];
				rank.setVisible(True);
				if p.isCommander():
					rank.setImage("gui/standard/icons/comm_crown.s2g");
					comm.setCaption("^555Commander: " + p.getFormattedName());
				elif p.isOfficer():
					rank.setImage("models/"+teamObj.getRace()+"/items/icons/officer1.s2g");
				else:
					rank.setImage("textures/econs/transparent.s2g");

				rank.setSize(16,16);
						
				name.setCaption( p.getFormattedName() );
				level.setCaption( str(p.getLevel()));
				kills.setCaption( str(p.getKills() ));
				deaths.setCaption( str(p.getDeaths()));
				assists.setCaption( str(p.getAssists()));
				ping.setCaption( str(p.getPing()));
				
				i += 1;
				rowCount += 1;

			while i < self.MAX_PLAYERS_PER_TEAM:

				row = table.getRow(rowCount);
				row.setVisible(False);

				cellList = [table.getWidget(rowCount, k, type=glass.GlassLabel) for k in range(7)];
				rank = cellList[0];
				rank.setVisible(False);
				
				for w in cellList[1:]:
					w.setCaption("");
				
				rowCount += 1;
				i += 1;
		

	def build(self):
		#self.world = glass.GlassLabel("12345678901234567890");
		#self.world.setForegroundColor(glass.Color(177,135,75));
		#self.add(self.world, 0,0);

		self.tables = [None]; #one table for each non-spec team
		for i in range (1,9):

			tableWindow = DefaultWindow();
			tableWindow.setBackgroundColor(glass.Color(70,20,20, 180));
			self.add(tableWindow, 0, 0);

			tableWindow.teamLabel = DefaultLabel("^555Team 1 ^wHuman");
			tableWindow.add(tableWindow.teamLabel,0,0);

			tableWindow.comm = DefaultLabel("^555Commander ^wLearningToComm");
			tableWindow.add(tableWindow.comm);

			tableWindow.div = DefaultDivider();
			tableWindow.add(tableWindow.div, 0, tableWindow.teamLabel.getHeight() + 5);

			# fuck scrolls
			tableWindow.listContainer = DefaultContainer();
			tableWindow.add(tableWindow.listContainer, 0, tableWindow.div.getHeight() + tableWindow.div.getY() + 5);

			tableWindow.table = DefaultTable();
			tableWindow.listContainer.add(tableWindow.table,0,0);

			self.tables.append(tableWindow);

			tableWindow.table.setFrame(False);
			tableWindow.table.setOpaque(True);
			tableWindow.table.padding = 1;
			tableWindow.table.autoAdjust = False;
			tableWindow.table.setAlternate(False);

			#tableWindow.scroll = glass.GlassScrollArea(tableWindow.table);
			#tableWindow.listContainer.add(tableWindow.scroll, 0, 0);
			#tableWindow.scroll.setBackgroundColor(transparency);			
			#tableWindow.scroll.setHorizontalScrollPolicy(glass.GlassScrollArea.SHOW_NEVER);


			headingRow = tableWindow.table.addRow("", "Player", "^bLV", "^gK", "^rD", "^lA", "Ping");
			headingRow.setOpaque(False);
			headingRow.setBackgroundColor(glass.Color(70,20,20, 0));
			#divRow = tableWindow.table.addRow(DefaultDivider());
			#divRow.getColumn(0).setColumnSpan(7);

			for j in range( self.MAX_PLAYERS_PER_TEAM ):
				rank = glass.GlassLabel();
				rank.setSize(16,16);
				
				name = glass.GlassLabel(" 12345678901234 ");
				name.setBackgroundColor( glass.Color(40,20,20) );
				name.setHeight(25);
				name.setOpaque(True);				
				
				level = glass.GlassLabel("12");
				level.setForegroundColor( tangoBlue );
				level.setBackgroundColor( glass.Color(30,15,15) );
				level.setAlignment(1);
				level.setHeight(25);
				level.setOpaque(True);
				
				kills = glass.GlassLabel(" 123 ");
				kills.setForegroundColor( tangoGreen );
				kills.setBackgroundColor( glass.Color(40,20,20) );
				kills.setAlignment(1);
				kills.setHeight(25);
				kills.setOpaque(True);
				
				deaths = glass.GlassLabel(" 123 ");
				deaths.setForegroundColor( tangoRed);
				deaths.setBackgroundColor( glass.Color(30,15,15) );
				deaths.setAlignment(1);
				deaths.setHeight(25);
				deaths.setOpaque(True);
				
				assists = glass.GlassLabel(" 123 ");
				assists.setForegroundColor( tangoYellowLight);
				assists.setBackgroundColor( glass.Color(40,20,20) );
				assists.setAlignment(1);
				assists.setHeight(25);
				assists.setOpaque(True);
				
				ping = glass.GlassLabel("1234");
				ping.setBackgroundColor( glass.Color(30,15,15) );
				ping.setAlignment(1);
				ping.setHeight(25);
				ping.setOpaque(True);
				
				row = tableWindow.table.addRow( rank, name, level, kills, deaths, assists, ping);
				#row.setOpaque(True);
				row.setBackgroundColor(glass.Color(70,20,20, 0));
				row.setOpaque(False);
				#for j in range(row.getColumnCount()):
				#	cell = row.getColumn(j);
				#	cell.setOpaque(True);
				#	cell.setBaseColor(glass.Color(70,70,70))
	
	def layoutRowIndex( self, tableCount):
		return math.ceil(tableCount/ 2.0) -1; #2.0 because we're using 2 columns
	
	def arrange(self):
		#call when the number of teams might change - joining a server and changing map
		#should I cache/store these vars as properties of self?
		numTeams = int(cvar_getvalue("sv_numteams")); #cvar_getvalue is always a float
		numColumns = 2.0;
		numRows = self.layoutRowIndex( numTeams -1 ) + 1;
		tableW = 0.4;
		tableH = 0.9/numRows;
		#create a meta-table, with 2 columns and enough rows as neccesary to hold the rest of the sub-tables
		tableEntries = math.ceil(  self.MAX_PLAYERS_PER_TEAM / numRows );
		for i in range(1,numTeams):
			rowIndex = self.layoutRowIndex(i);
			
			tableX = 0.05 + 0.5*((i-1) % 2);
			tableY = 0.05 + rowIndex/numRows; #FIXME this is wrong, the padding is not always 5%
			tableWin = self.tables[i];
			
			tableWin.setPosition( int(self.getWidth() * tableX),int(self.getHeight() * tableY));
			#table.adjustSizeToPct ( tableW, 0.9);
			tableWin.setSize(int(tableW*self.getWidth()), int(tableH*self.getHeight()));
			tableWin.setVisible(True);

			tableWin.div.setWidth(tableWin.getWidth() - 5);
			tableWin.listContainer.setSize(tableWin.getWidth(), tableWin.getHeight() - (tableWin.div.getHeight() + tableWin.div.getY() + 5));
			tableWin.table.adjustSizeTo(tableWin.listContainer.getWidth() - 20);
			#tableWin.scroll.setSize(tableWin.listContainer.getWidth() - 10, tableWin.listContainer.getHeight() );
			tableWin.comm.setPosition(tableWin.getWidth() - tableWin.comm.getWidth(),0);
			
		for i in range(numTeams, 9): #hide the rest of the tables
			tableWin = self.tables[i];
			tableWin.setVisible(False);
	
	MAX_PLAYERS_PER_TEAM = 32;

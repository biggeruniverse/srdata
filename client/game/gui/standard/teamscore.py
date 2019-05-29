# (c) 2010 savagerebirth.com

from silverback import *;
import savage;
import glass;
import math;

class TeamScore(glass.GlassWindow):
	def __init__(self):
		glass.GlassWindow.__init__(self);
		self.setSizePct(.9, .9);
		self.setPositionPct(.05, 0.05);
		self.build();
		self.setTitleVisible(0);
		self.setTitleBarHeight(0);
		self.setBackgroundColor(glass.Color(0,0,0,100));
		self.setVisible(False);
		

	#called when we want to update the window
	def update(self):
		teamsList = [[],[],[],[],[],[],[],[],[]];
		
		players = savage.getPlayers();
		for p in players:
			teamsList[p.getTeam()].append(p);

		self.world.setCaption(cvar_get("world_name"));
		self.world.setFont(fontSizeLarge);
		self.world.setX( (self.getWidth() - self.world.getWidth())//2 )
	
		#fire a request for scores
		CL_RequestScores();

		# clear tables, add up team scores as players are added to the tables

		for team in range(1,int(cvar_getvalue("sv_numteams"))):
			table = self.tables[ team ];
			currentTeam = teamsList[team];
			tmk = 0
			tmd = 0
			rowCount = 0;
			playerCount = len(teamsList[team]);
			i = 0;
			while i < playerCount:
				p = currentTeam[i];
				
				tmk += p.getKills();
				tmd += p.getDeaths();
				
				rank, name, xp, kills, deaths, assists, ping = [
				  table.getWidget(rowCount, k, type=glass.GlassLabel) for k in xrange(7)
				];
				rank.setVisible(True);
				if p.isCommander():
					rank.setImage("gui/standard/icons/comm_crown.s2g")
				elif p.isOfficer():
					rank.setImage("models/human/items/icons/officer1.s2g")
				else:
					rank.setVisible(False);
				rank.setSize(16,16);
						
				name.setCaption( p.getFormattedName() );
				xp.setCaption( str(p.getXp()));
				kills.setCaption( str(p.getKills() ));
				deaths.setCaption( str(p.getDeaths()));
				assists.setCaption( str(p.getAssists()));
				ping.setCaption( str(p.getPing()));
				
				i += 1;
				rowCount += 1;
			while i < self.MAX_PLAYERS_PER_TEAM:
				cellList = [table.getWidget(rowCount, k, type=glass.GlassLabel) for k in xrange(7)];
				rank = cellList[0];
				rank.setVisible(False);
				
				for w in cellList[1:]:
					w.setCaption("");
				
				rowCount += 1;
				i += 1;

	def build(self):
		self.world = glass.GlassLabel("12345678901234567890");
		self.world.setForegroundColor(glass.Color(177,135,75));
		self.add(self.world, 0,0);
		self.tables = [None]; #one table for each non-spec team
		for i in range (1,9):
			table = GlassTablePlus();
			self.add(table,0,0);
			self.tables.append(table);
			table.setFrame(0);
			table.setOpaque(0);
			table.autoAdjust = False;
			for j in range( self.MAX_PLAYERS_PER_TEAM ):
				rank = glass.GlassLabel();
				rank.setSize(16,16);
				
				name = glass.GlassLabel("12345678901234567890");
				
				xp = glass.GlassLabel("12345");
				xp.setForegroundColor( tangoBlue );
				xp.setAlignment(1);
				
				kills = glass.GlassLabel("123");
				kills.setForegroundColor( tangoGreen );
				kills.setAlignment(1);
				
				deaths = glass.GlassLabel("123");
				deaths.setForegroundColor( tangoRed);
				deaths.setAlignment(1);
				
				assists = glass.GlassLabel("123");
				assists.setForegroundColor( tangoYellowLight);
				assists.setAlignment(1);
				
				ping = glass.GlassLabel("1234");
				ping.setAlignment(1);
				
				table.addRow( rank, name, xp, kills, deaths,assists, ping);
	
	def layoutRowIndex( self, tableCount):
		return math.ceil(tableCount/ 2.0) -1; #2.0 because we're using 2 columns
	
	def arrange(self):
		#call when the number of teams might change - joining a server and changing map
		#should I cache/store these vars as properties of self?
		numTeams = cvar_getvalue("sv_numteams"); #cvar_getvalue is always a float
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
			table = self.tables[i];
			
			table.setPositionPct( tableX, tableY);
			table.adjustSizeToPct ( tableW, 0.9);
			table.setHeight( int(tableH*self.getHeight()));
			table.setVisible(True);
			
		for i in range(numTeams, 9): #hide the rest of the tables
			table = self.tables[i];
			table.setVisible(False);
	
	MAX_PLAYERS_PER_TEAM = 32;



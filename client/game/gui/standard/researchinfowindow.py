#copyright (c) 2011 savagerebirth.com
#this file generates and updates the research info window used in spechud and the unit info window used in 
#both spechud and commhud

import glass;
import savage;

class ResearchInfoWindow(glass.GlassWindow):
	ICON_SIZE = 48;
	HEADER_ICON_SIZE = 32;
	PADDING = 4;
	
	def __init__(self):
		glass.GlassWindow.__init__(self, "Research");
		self.setVisible(False);
		self.setMovable(0);
		self.setFocusable(False);
		self.setTitleVisible(0);
		self.setTitleBarHeight(0);
		self.setBackgroundColor(glass.Color(255,255,255,127));
		
		self.table = GlassTablePlus();
		self.add(self.table);
		self.table.setPosition(self.PADDING,self.PADDING+1);
		self.table.makeBlank();
		self.table.autoAdjust = False;
		self.table.setCellPadding(self.PADDING//2);
		self.headers = [];
		self.widgets = [];
		
		header_beast = ["/gui/standard/comm/upgrade_stronghold.s2g",
			"/models/beast/buildings/icons/nexus.s2g",
			"/models/beast/buildings/icons/entropy.s2g",
			"/models/beast/buildings/icons/strata.s2g",
			"/models/beast/buildings/icons/fire.s2g",
			"/models/beast/buildings/icons/lair.s2g",
			"/models/beast/buildings/icons/siege.s2g",
			"/models/beast/buildings/icons/sanctuary.s2g"
		];
		header_human = ["/gui/standard/comm/upgrade_stronghold.s2g",
			"/models/human/buildings/icons/arsenal.s2g",
			"/models/human/buildings/icons/magnetic.s2g",
			"/models/human/buildings/icons/electric.s2g",
			"/models/human/buildings/icons/chemical.s2g",
			"/models/human/buildings/icons/selectionstronghold.s2g",
			"/models/human/buildings/icons/siege.s2g",
			"/models/human/buildings/icons/monastery.s2g"
		];
		levels = [1,2,3,1,2];		
		
		def makeHeaderWidget(x):
			w = glass.GlassLabel("");
			if x != None:
				w.setImage(x);
			w.setSize(self.HEADER_ICON_SIZE, self.HEADER_ICON_SIZE);
			return w;
		
		def makeLevelWidget(x):
			w = glass.GlassLabel(str(x));
			w.setSize(self.ICON_SIZE, self.ICON_SIZE);
			w.setFont(fontSizeLarge);
			w.setAlignment(glass.Graphics.CENTER);
			return w;
		
		self.header_beast = [ makeHeaderWidget(x) for x in header_beast ];
		self.header_human = [ makeHeaderWidget(x) for x in header_human ];
		self.levels = [ makeLevelWidget(x) for x in levels];
	
	def rebuildResearchable(self,team):
		self.table.clear();
		self.teamObj = team;
		allItems = self.teamObj.getResearchableItems();
		allWeapons = self.teamObj.getResearchableWeapons();
		allUnits = self.teamObj.getResearchableUnits();	
		
		if self.teamObj.getRace() == "human":
			self.headers = self.header_human;
			huntingBow = savage.getObjectType("human_bow");
			allWeapons[0].insert(0,huntingBow);
			nomad = savage.getObjectType("human_nomad");
			allUnits.insert(0,nomad);
		elif self.teamObj.getRace() == "beast":
			self.headers = self.header_beast;
			scav = savage.getObjectType("beast_scavenger");
			allUnits.insert(0,scav);		
		
		medic = allUnits.pop(3); 
		mt = [go for go in allWeapons[0] if go.getValue("requirement1") == medic.getName()]; 			
	
		medictech1 = mt[0];
		medictech2 = savage.getObjectType(self.teamObj.getRace() + "_revive"); ## TODO: fix shaman shield thingy
		#medictech2 = mt[1];
		
		siege1 = allUnits.pop(3); 
		allUnits.append(None);
		siege2 = allUnits.pop(3);
		allUnits.append(None);
		
		medicrow = [None, medic, None, medictech1, medictech2 ];
		siegerow = [None, siege1, siege2, None, None]		
		self.rows = [];				
		self.table.addRow(self.headers[0], *self.levels);
		
		for i in range(4):
			row = [];
			try:
				for j in range(3):
					row.append(allWeapons[i][j]);
				for k in range(2):
					row.append(allItems[i][k]);
			except IndexError:
				pass
			self.rows.append(row);
		row = [];
		for i in range(3):
			row.append(allUnits[i]);
		self.rows.append(row);				
		self.rows.append(siegerow);
		self.rows.append(medicrow);			
		
		for i, row in enumerate(self.rows):
			for j, obj in enumerate(row):
				widget = glass.GlassLabel("");
				if obj != None:						
					widget.setImage( obj.getValue("icon")+".s2g" );				
				widget.setSize(self.ICON_SIZE, self.ICON_SIZE);
				row[j] = widget;
				self.widgets.append([obj, widget]);
			row = [ self.headers[i+1] ] + row;
			self.table.addRow(*row);
		
		self.table.adjustSize();
		self.table.adjustJustification();
		self.setSize(self.table.getWidth() + self.PADDING*3, self.table.getHeight() + 2 + self.PADDING*3);
		
	def updateResearch(self):		 		
		for widget in self.widgets:				
			if widget[0] != None and widget[0] not in self.teamObj.getObjects():				
					widget[1].setForegroundColor(tangoGrey5);				
		
	def open(self):
		self.setVisible(True);
	
	def close(self):
		self.setVisible(False);
		
class UnitInfoWindow(glass.GlassWindow):	
	PADDING = 4;
	def __init__(self):	
		glass.GlassWindow.__init__(self, "Units");
		self.setMovable(0);
		self.setFocusable(False);
		self.setTitleVisible(0);
		self.setTitleBarHeight(0);
		self.setBackgroundColor(transparency);
		
		self.table = GlassTablePlus();
		self.add(self.table);
		self.table.setPosition(0,0);
		self.table.makeBlank();
		self.table.autoAdjust = False;		
		
	def buildUnitInfo(self, team):		
		self.table.clear();
		self.widgets = [];
		self.team = team;
		units = self.team.getUnits();
		for unit in units:			
			if unit.isUnitType() and not unit.isWorkerType():				
				label = glass.GlassLabel("");
				label.setAlignment(glass.Graphics.RIGHT);
				label.setImage(unit.getValue("icon")+".s2g");
				label.setSize(32, 32);
				label.setVisible(False);				
				self.widgets.append([unit.getName(),label]);				
		
	def updateUnitInfo(self):	
		self.table.clear();
		row = [];
		activeUnits = self.team.getUnitsInUse();
		self.setVisible(False);
		for widget in self.widgets:				
			count = activeUnits[widget[0]];			
			if count > 0:		
				row.append(widget[1]);
				widget[1].setCaption("\n" + str(count));
				widget[1].setVisible(True);					
				self.setVisible(True);
		self.table.addRow(*row);
		self.table.adjustSize();
		self.table.adjustJustification();
		self.setSize(self.table.getWidth() + 5, self.table.getHeight());

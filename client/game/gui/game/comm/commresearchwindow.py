#copyright (c) 2011 savagerebirth.com
#this file generates and updates the research pop-up used on the comm hud

import glass;
import savage;

class CommResearchWindow(glass.GlassWindow):
	ICON_SIZE = 48;
	HEADER_ICON_SIZE = 32;
	PADDING = 4;
	
	def __init__(self):
		glass.GlassWindow.__init__(self, "Research");
		self.setVisible(0);
		self.setAlpha(0);
		self.setMovable(0);
		self.setFocusable(0);
		self.setTitleVisible(0);
		self.setTitleBarHeight(0);
		self.setBackgroundColor(glass.Color(255,255,255,127));
		
		self.table = DefaultTable();
		self.add(self.table);
		self.table.setPosition(self.PADDING,self.PADDING+1);
		self.table.makeBlank();
		self.table.autoAdjust = False;
		self.table.setCellPadding(self.PADDING//2);
		
		self.teamObj = None;
		
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
		
		
	def onTeamChange(self):
		#TODO call this on show, or on some team-changing game event
		self.teamObj = savage.Team( savage.getLocalPlayer().getTeam() );
		self.rebuild();
		
	def rebuild(self):
		self.table.clear();
		
		#1. create lists of object types
		# each list represents a column
		# use None to represent a blank space
		items = self.teamObj.getResearchableItems();
		weapons = self.teamObj.getResearchableWeapons();
		units = self.teamObj.getResearchableUnits();
		
		#nomad/scav can't be researched
		units.insert(0,None);
		
		medic = units.pop(3); #medic gets its own row
		mt = [go for go in weapons[0] if go.getValue("requirement1") == medic.getName()]; 

		#hunting bow needs a place holder
		if self.teamObj.getRace() == "human":
			weapons[0].insert(0,None);
	
		medictech1 = mt[0];
		medictech2 = None;
		#medictech2 = mt[1];
		
		seige1 = units.pop(3); #seige gets its own row
		units.append(None);
		seige2 = units.pop(3);
		units.append(None);
		
		medicrow = [None, medic, None, medictech1, medictech2 ];
		seigerow = [None, seige1, seige2, None, None]
		
		rows = [];

		#2.add the header row to the table
		if self.teamObj.getRace() == "human":
			self.table.addRow(*self.header_human);
		elif self.teamObj.getRace() == "beast":
			self.table.addRow(*self.header_beast);
		
		for i in range(3):
			row = [ weapons[0][i], weapons[1][i], weapons[2][i], weapons[3][i], units[i], seigerow[i], medicrow[i]];
			rows.append(row);
		for i in range(2):
			row = [ items[0][i], items[1][i], items[2][i], items[3][i], units[i+3], seigerow[i+3], medicrow[i+3] ];
			rows.append(row);

		
		self.table.rows[0].setBackgroundColor(tangoGrey2);
		
		#3. fill in the rest of the table
		
		for i, row in enumerate(rows):
			for j, obj in enumerate(row):
				#i. convert the object types to widgets
				if obj == None:
					widget = glass.GlassLabel("");
				else:
					name = obj.getName();
					widget = glass.ImageButton(name,obj.getValue("icon")+".s2g");
					widget.setClickAction( "commhud.ResearchSimple('"+name+"');" );
				widget.setSize(self.ICON_SIZE, self.ICON_SIZE);
				row[j] = widget;
			
			#ii. add in the level labels
			row = [ self.levels[i] ] + row;
			#iii. then add the rows
			self.table.addRow(*row);
		
		self.table.adjustSize();
		self.table.adjustJustification();
		self.setSize(self.table.getWidth() + self.PADDING*3, self.table.getHeight() + 2 + self.PADDING*3);
		self.setX( commhud.quickbar.getX() + commhud.research.getX() + (commhud.research.getWidth() - self.getWidth())//2 );
		self.setY( commhud.quickbar.getY() + commhud.research.getY() - self.getHeight() - self.PADDING );
	
	def open(self):
		ActionSequence(FadeInAction(self));
	
	def close(self):
		ActionSequence(FadeOutAction(self));
		
	def getTooltipFor(self, objtype):
		#TODO this generates the tooltips, but when do we need to set them? In frame?
		"""General format
		
		<icon> <name> (possible coloured by tech type)
		<gold> <gold cost> <stone> <stone cost>
		<one line description>
		Requires:
			- <Requisite 1>
			- <Requisite 2>
		Colour them green if they're met, red if they're not met and yellow if they're being researched/will be met soon
		"""
		
		team = savage.Team(savage.getLocalPlayer().getTeam());
		
		tooltip = "^icon " + objtype.getValue("icon") + "^ " + objtype.getValue("description") + "\n";
		tooltip += "^w^icon ../../gui/standard/icons/gold/gold_icon^^y" + str(objtype.getValue("goldCost"));
		tooltip += " ^w^icon ../../gui/standard/icons/redstone^^900"+str(objtype.getValue("stoneCost")) + "\n";
		tooltip += "^w"+objtype.getValue("tooltip") + "\n";
		tooltip += "Requires:\n";
		
		for requirement in ("builder1","builder2","requirement1","requirement2"):
			value = objtype.getValue(requirement);
			if value == "":
				continue;
				
			notMet = True;
			inProgress = False;
			
			if requirement.startwith("builder"):
				notMet = not team.hasBuilding(value); #TODO
				inProgress = notMet and team.isBuilding(value); #TODO
			elif requirement.startswith("requirement"):
				currentResearch = [ot.getName() for ot in team.getResearch()];
				inProgress = value in currentResearch;
				notMet = not team.isResearched(value);

			color = "^y" if inProgress else "^r" if notMet else "^g";
			tooltip += color + " - " + value + "\n";
		return tooltip;
		
	def update(self):
		pass;
		#TODO make this get called by some game event, and onShow
		#1. determine which research options are available (i.e. which have pre-requisites fully met?)
			#let them have full alpha and be of normal colour
		#2. determine which research options are already researched
			#let them have full alpha and a green tint. they should not be clickable.
		#3. determine which research options are not available (i.e. which don't have pre-requisites met)
			#let them have partial alpha and a grey tint. they should not be clickable.
		#Remark: we should build something to determine this into GameObject, we're already doing viability checks in getTooltipFor
		
	


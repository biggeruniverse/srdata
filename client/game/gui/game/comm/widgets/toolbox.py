#(c) 2012 savagerebirth.com

from silverback import *;
import glass;
import savage;

class ToolBox(DefaultWindow):

	def __init__(self):
		DefaultWindow.__init__(self);
		self.setFrameStyle("Shadow");

		# I'm not sure about fixed or pct size here...
		# Pct for now, might change later!
		#self.setSize(screenHeightPct(.3), screenHeightPct(.3));
		self.setSize(10 + (48+3)*4, 48 + (48+3)*3)

		self.setBackgroundColor(windowCommhud);

		self.currentSelection = None;

		# What do we need?

		# 1. TabbedArea

		self.tabContainer = glass.GlassTabbedArea();
		self.add(self.tabContainer, 1, 1);
		self.tabContainer.setSize(self.getWidth() - 2, self.getHeight() - 2);
		self.tabContainer.setBackgroundColor(transparency);

		tabWidth = self.tabContainer.getWidth();
		tabHeight = self.tabContainer.getHeight();   

		# 1.1 Build Menu and Commands --> Contextmenu

		self.commandsMenu = ContextMenu();
		self.commandsMenu.setSize(tabWidth, tabHeight);
		self.commandsMenu.setBackgroundColor(windowCommhud); # Too dark imo, needs adjusting
		self.tabContainer.addTab("Cmd", self.commandsMenu);

		self.buildMenu = ContextMenu();
		self.buildMenu.setSize(tabWidth, tabHeight);
		self.buildMenu.setBackgroundColor(windowCommhud); # Too dark imo, needs adjusting
		self.tabContainer.addTab("Build", self.buildMenu);

		# 1.2 Research list
		
		# 1.3 Tithe Window (why not)

		self.tax = TitheSettings();
		self.tabContainer.addTab("Tax", self.tax)

		# 1.4 Request settings

		requestSettings = RequestSettings();
		self.tabContainer.addTab("Req", requestSettings);

	def handleSelection(self):
		if self.currentSelection == None:
			return;
		elif len(self.currentSelection.list) == 0:
			self.commandsMenu.buildContext(commcontexts.contextDict["global"]); # Might use global commands here!
			self.commandsMenu.context.object = None;
		elif len(self.currentSelection.list) == 1:
			# we have a single selection!
			obj = self.currentSelection.list[0];
			ot = obj.getType();			
			if ot.isUnitType():
				self.commandsMenu.object = obj;		
				try:
					self.commandsMenu.buildContext(commcontexts.contextDict[ot.getName()]);				
				except KeyError:
					self.commandsMenu.buildContext(commcontexts.contextDict["global"]);
			else:
				self.commandsMenu.object = None;
				self.commandsMenu.buildContext(commcontexts.contextDict["global"]);				
		else:
			if self.currentSelection.containsUnits():
				self.commandsMenu.buildContext(commcontexts.contextDict[savage.getLocalTeam().getRace() + "_worker"])
			else:
				self.commandsMenu.object = None;
				self.commandsMenu.buildContext(commcontexts.contextDict["global"]);				

	def onShow(self):
		# For now, always show the build context!
		self.buildMenu.buildContext(commcontexts.contextDict[savage.getLocalTeam().getRace() + "_build"]);
		self.commandsMenu.buildContext(commcontexts.GlobalContext());
		self.handleSelection();

	def onSelection(self, e):
		#Always keep track of the current selection
		#No idea if that's good code, might just pass the list/selected objects.
		self.currentSelection = e.selection;
		self.handleSelection();

# This is the old toolbar, I'll leave it here to have some kind of reference for now. 
"""
class CommToolBar(CommAbstractWidget):
	
	def create(self):
		
		self.items = [];
		
		#self.addListener(self);
		
		self.setSize(screenWidth, screenHeightPct(.33));
		self.setPosition(0, screenHeight - self.getHeight());
	   
		self.minimap = CommMiniMap()
		self.minimap.create()
		self.add(self.minimap, 0, self.getHeight()-self.minimap.getHeight())
 
		self.primary = DefaultContainer();
		self.primary.setBackgroundColor(glass.Color(0, 0, 0, 128));
		self.primary.setSize(25, 68);
		self.add(self.primary, self.minimap.getWidth(), self.getHeight()-68);
		
		build = DefaultButton("B");
		build.setSize(20, 20);
		build.addActionListener(self);
		self.primary.add(build, 3, 3);
		
		research = DefaultButton("R");
		research.addActionListener(self);
		research.setSize(20, 20);
		self.primary.add(research, 3, 25);
		
		info = DefaultButton("Q");
		info.addActionListener(self);
		info.setSize(20, 20);
		self.primary.add(info, 3, 47);
		
		#self.workerIcon = DefaultImageButton();
		#self.workerIcon.setImage("models/" + str(commhud.team.getRace()) + "/units/worker/icon.s2g");
		#self.workerIcon.setSize(build.getHeight(), build.getHeight());
		#self.primary.add(self.workerIcon, self.primary.getWidth() - build.getHeight() - 5, 5);        
		
		self.secondary = DefaultContainer();
		self.secondary.setBackgroundColor(glass.Color(0, 0, 0, 128));
		self.secondary.setSize(screenWidthPct(.5), screenHeightPct(.1));
		self.secondary.setVisible(0);
		self.add(self.secondary, self.minimap.getWidth()+self.primary.getWidth(), self.getHeight()-self.secondary.getHeight());
		
		self.closeHandle = DefaultLabel("<");
		self.closeHandle.setSize(1, self.getHeight() - 2);
		self.closeHandle.addActionListener(self);
		self.closeHandle.setVisible(0);
		self.add(self.closeHandle, self.getWidth() - 15, 1);
		
		# build items
		self.buildList = DefaultContainer();
		self.buildList.setSize(self.secondary.getWidth() - 2, self.secondary.getWidth() - 2);
		self.secondary.add(self.buildList, 1, 1);
		
		
		# research items
		self.researchList = DefaultContainer();
		self.researchList.setSize(self.secondary.getWidth() - 2, self.secondary.getWidth() - 2);
		self.secondary.add(self.researchList, 1, 1);
		
		# info items
		self.infoList = DefaultContainer();
		self.infoList.setSize(self.secondary.getWidth() - 2, self.secondary.getWidth() - 2);
		self.secondary.add(self.infoList, 1, 1);
		self.quickTable = DefaultTable();
		self.infoList.add(self.quickTable);
		
		gblEventHandler.addGameListener(commhud.researchManager);
		gblQueue.addListener(commhud.researchManager);
		self.buildBuild();
		self.buildResearch();
		self.buildQuick();


		self.contextmenu = ContextMenu()
		self.contextmenu.setSize(screenHeightPct(.25), screenHeightPct(.25))
		self.add(self.contextmenu, "right", "bottom")

		commhud.selection.addListener(self)
	   
	def onAction(self, e):
		
		# this could be better but meh
		if e.widget.getCaption() == "<":
			self.secondary.setVisible(0);
			self.closeHandle.setVisible(0);
		elif e.widget.getCaption() in ("B", "R", "Q"):
			self.buildList.setVisible(0);
			self.researchList.setVisible(0);
			self.infoList.setVisible(0);
			self.closeHandle.setVisible(1);
			self.secondary.setVisible(1);
			
			if e.widget.getCaption() == "B":
				selected = self.buildList;
			elif e.widget.getCaption() == "R":
				selected = self.researchList;
			elif e.widget.getCaption() == "Q":
				selected = self.infoList;
				
			selected.setVisible(1);
			self.secondary.setWidth(selected.getWidth() + 5);
			self.closeHandle.setX(self.secondary.getWidth() - 5);

	def frame(self):
		pass;

	# TODO: I don't think I erase/clear here properly
	def rebuild(self):
		self.clearBuild();
		self.buildBuild();
		
		self.clearResearch();
		self.buildResearch();
		
		#self.clearQuick();
		#self.buildQuick();
		
	def clearResearch(self):
		self.researchList.erase();
		#self.researchListItems = [];

	def clearBuild(self):
		self.buildList.clear();

	def clearQuick(self):
		self.quickTable.clear();
	   
	def buildBuild(self):
		self.buildList.add(commhud.researchManager);
		commhud.researchManager.setSizePct(1,1);
 
	def buildResearch(self):
		
		team = commhud.team;
		
		tierData = [
			{'units': [], 'weapons': [], 'items': []}, 
			{'units': [], 'weapons': [], 'items': []},
			{'units': [], 'weapons': [], 'items': []}
		];
		
		researchable = team.getResearchable();
		
		units = [ typeobj for typeobj in researchable if typeobj.isUnitType()];
		if len(units)>0:
			units.pop(0);
		weapons = [ typeobj for typeobj in researchable if typeobj.isWeaponType() or typeobj.isMeleeType()];
		items = [ typeobj for typeobj in researchable if typeobj.isItemType()];
		
		for unit in units:
			tierData[unit.getValue("needBasePoints") - 1]["units"].append(unit);

		for w in weapons:
			if w.getName() == "human_potion" or w.getName() == "beast_heal" or w.getName().endswith("_revive"):
				items.append(w);
				continue;
			
			if w.getName().endswith("_weapon") == False and w.getName().endswith("_melee") is False:
				tierData[w.getValue("needBasePoints") - 1]["weapons"].append(w);
		
		for item in items:
			if item.getName() != "human_relocater_trigger":
				tierData[item.getValue("needBasePoints") - 1]["items"].append(item);
		
		r = 0;
		i = 1;
		x = 3;
		for data in tierData:        
			r += x;
			container = DefaultContainer();
			container.setBackgroundColor(glass.Color(0, 0, 0, 90));
			self.researchList.add(container, r, 2);
			
			x = 3;
			tier = DefaultLabel("Tier " + str(i));
			container.add(tier, x + 20, 3);
			
			for unit in data["units"]:
				item = ResearchItemIcon(unit);
				item.setSize(40, 43);
				container.add(item, x, 22);
				x += 42;
				
			startX = x;
			for weapon in data["weapons"]:
				weapon.img = img = DefaultImageButton();
				img.setImage(weapon.getValue("icon") + ".s2g", False);
				img.setSize(30, 30);
				img.setTooltip(weapon.getValue("description"));
				container.add(img, x, 3);
				x += 32;
				
			endX = x;
			x = startX;
			for item in data["items"]:
				item.img = img = DefaultImageButton();
				img.setImage(item.getValue("icon") + ".s2g", False);
				img.setSize(30, 30);
				img.setTooltip(item.getValue("description"));
				container.add(img, x, 35);
				
				x += 32;
				
			i += 1;
			x = max(endX, x);
			container.setWidth(x);
			x += 7;
			
		self.researchList.setWidth(r + container.getWidth());
		
	def buildQuick(self):
		self.quickTable.clear();

		b = DefaultButton("RESIGN");
		b.setClickAction("CL_RequestResign()");

		c = DefaultButton("ROSTER");
		c.setClickAction("commhud.rosterWindow.toggle()");

		d = DefaultButton("REQUESTS");
		d.setClickAction("commhud.widgetStack['requestsettings'].toggle()");

		e = DefaultButton("TITHE");
		e.setClickAction("commhud.widgetStack['tithesettings'].toggle()");

		self.quickTable.addRow(b,c,d,e);
		
	def onEvent(self, e):
		con_println("triggered\n");
		return;
	
		if e.eventType == "research_begin":
			#dayum. work!
			r = savage.ResearchItemIcon(e.objtype, e.sourceId, savage.getGameTime(), 0);
			#do we have this exact thing already? remove it first (just purchased)
			for item in self.items:
				if item.item.objtype == e.objtype:
					if item.action == None:
						item.item.builder = e.sourceId;
					elif item.action.item == r: #who is naming this stuff? :P
						item.action = None;
					return;

			item = ResearchManagerItem(r);
			self.itemsContainer.add(item);
			self.items.append(item);

		elif e.eventType == "research_complete" or e.eventType == "research_cancel":
			for item in self.items:
				if item.item.objtype == e.objtype and item.item.builder == e.sourceId:
					self.items.remove(item);
					self.itemsContainer.remove(item);
					item.erase();

		elif e.eventType == "research_queued":
			for item in self.items:
				if item.item.objtype == e.objtype and item.item.builder == e.sourceId:
					item.action = None;

		elif e.eventType == "team_reset":
			for item in self.items:
				self.itemsContainer.remove(item);
				item.erase();
			del self.items[:];

	def onSelection(self, e):
		con_println("new selection")
		#TODO: switch context menu here
		
class ResearchItemIcon(DefaultContainer):
	
	def __init__(self, obj):
		DefaultContainer.__init__(self);
		
		self.obj = obj;
		
		self.icon = DefaultImageButton();
		self.icon.setImage(obj.getValue("icon") + ".s2g", False);
		self.icon.setTooltip(obj.getValue("description"));
		self.add(self.icon);
		
		# listener
		
	def setSize(self, w, h):
		self.icon.setSize(w, h);
		DefaultContainer.setSize(self, w, h);
		
	def setWidth(self, w):
		self.icon.setWidth(w);
		DefaultContainer.setWidth(w);
		
	def setHeight(self, h):
		self.icon.setHeight(h);
		DefaultContainer.setHeight(h);
	   
#commhud.researchManager = ResearchManager();
#commhud.addWidget('toolbar', CommToolBar());

"""

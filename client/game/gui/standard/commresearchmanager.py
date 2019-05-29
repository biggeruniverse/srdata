#copyright 2011 (c) savagerebirth.com
#this file creates a way to interact with the research queue via the gui 

import savage;
import glass;
import math;

class ResearchManager(glass.GlassWindow):
	VERTICAL_PADDING = 6;
	
	def __init__(self):
		glass.GlassWindow.__init__(self);
		self.setCaption("Research Queue");
		self.setBackgroundColor(black);
		
		self.setSizePct(0.45, 0.2);
		self.centerWindow();
		self.setVisible(False);
		self.setAlpha(128);
		self.setTitleVisible(0);

		self.itemsContainer = glass.GlassContainer();
		self.itemsContainer.setSize(300,150);
		self.scrollArea = glass.GlassScrollArea(self.itemsContainer);
		self.scrollArea.setScrollPolicy( glass.GlassScrollArea.SHOW_AUTO , glass.GlassScrollArea.SHOW_NEVER );
		self.add(self.scrollArea);
		self.scrollArea.setSizePct(1,.85);
		
		self.items = [];
	
	def onEvent(self, e):
		if e.eventType == "research_begin":
			#dayum. work!
			r = savage.ResearchItem(e.objtype, e.sourceId, savage.getGameTime(), 0);
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


	def onResearchQueued(self, action):
			r = action.item;
			con_println(str(action));
			item = ResearchManagerItem(r, action);
			self.itemsContainer.add(item);
			self.items.append(item);

	def update(self):
		width = 0;
		for i,item in enumerate(self.items):
			item.setX(width);
			width = width + item.getWidth() + 10;
			try:
				item.update();
			except e:
				con_println(e);
		self.itemsContainer.setWidth(width);
		
	
	def close(self):
		ActionSequence(FadeOutAction(self));
	def open(self):
		ActionSequence(FadeInAction(self));
	
class ResearchManagerItem(glass.GlassContainer):
	ICON_SIZE = 64;
	STATUS_ICON_SIZE = 16;
	PADDING = int(math.ceil(STATUS_ICON_SIZE/2.0));
	BAR_PADDING = 1;
	VERTICAL_PADDING = 2;
	
	def __init__(self, item, action=None):

		self.item = item;
		self.action = action;
		
		glass.GlassContainer.__init__(self);
		self.setSize(int(self.ICON_SIZE*1.5 + 2 * self.PADDING), int(self.ICON_SIZE*1.5 + 2 * self.PADDING));
		self.setOpaque(0);
		
		self.name = glass.GlassLabel(item.getType().getValue("description"));
		self.name.setPosition(self.PADDING,self.PADDING);
		self.name.setWidth(self.ICON_SIZE);
		self.name.setAlignment(glass.Graphics.CENTER);
		self.add(self.name);
		
		lineh = self.name.getHeight();
		
		self.icon = glass.GlassLabel();
		self.icon.setImage(item.getType().getValue("icon")+".s2g");
		self.icon.setX(self.PADDING)
		self.icon.setY(self.name.getY() + self.name.getHeight() + self.VERTICAL_PADDING );
		self.icon.setSize(self.ICON_SIZE, self.ICON_SIZE);
		self.add(self.icon)
		
		self.close = glass.ImageButton("close","/gui/standard/cancel.s2g");
		self.close.setSize( self.STATUS_ICON_SIZE , self.STATUS_ICON_SIZE )
		#need to be able to handle what happens when that gets clicked somehow
		self.close.setX( self.icon.getX() + self.icon.getWidth() - self.close.getWidth()//2 )
		self.close.setY( self.icon.getY() );
		self.add(self.close);
		self.close.addActionListener(self);
		
		self.bar = glass.GlassProgressBar();
		self.bar.setX( self.icon.getX() + self.BAR_PADDING );
		self.bar.setY( self.icon.getY() + self.icon.getHeight() + self.VERTICAL_PADDING + self.BAR_PADDING );
		self.bar.setWidth( self.ICON_SIZE - 2*self.BAR_PADDING );
		self.bar.setHeight(11)
		self.add(self.bar)
		
		self.barText = glass.GlassLabel("");
		self.barText.setX( self.bar.getX() + self.BAR_PADDING);
		self.barText.setY( self.bar.getY() + self.BAR_PADDING);
		self.barText.setWidth( self.bar.getWidth() - 2*self.BAR_PADDING);
		self.barText.setHeight( self.bar.getHeight()- 2*self.BAR_PADDING);
	
		self.status_icon = glass.GlassLabel("");
		self.status_icon.setImage("/textures/econs/transparent.s2g");
		self.status_icon.setSize( self.STATUS_ICON_SIZE , self.STATUS_ICON_SIZE );
		self.status_icon.setPosition( self.close.getX(), self.close.getY() + self.ICON_SIZE );
		self.add(self.status_icon);
		
	def update(self):
		w,h = self.status_icon.getWidth(), self.status_icon.getHeight();
		
		if self.action == None or self.action.areReqsMet(): #researching
			research=savage.Team(savage.getLocalPlayer().getTeam()).getResearch();
			matchitems = [i for i in research if i == self.item];
			del research[:];
			if len(matchitems) == 1:
				self.bar.setBackgroundColor(transparency);
				self.bar.setForegroundColor(tangoGreen);
				self.bar.setProgress(matchitems[0].percentComplete);
				self.item.percentComplete = matchitems[0].percentComplete;
			elif len(matchitems) > 1:
				raise Exception("Failure of Space-Time!"); #throw an exception this should never happen...
			
			self.status_icon.setImage("/gui/standard/icons/alert_gear.png");

		elif self.item.areTechRequirementsMet() == False:
			self.bar.setBackgroundColor(tangoRed);
			self.bar.setBaseColor(tangoRedDark);
			self.status_icon.setTooltip("Tech");
			self.status_icon.setImage( "/gui/standard/icons/alert_warning.png" );
			
		elif self.item.areResourceRequirementsMet() == False: #still in queue
			self.bar.setBackgroundColor(tangoRed);
			self.bar.setBaseColor(tangoRedDark);
			self.status_icon.setTooltip("Resources");
			self.status_icon.setImage( "/gui/standard/icons/alert_warning.png" );

		#elif status == "resource":
		#	self.bar.setAlignment(glass.Graphics.CENTER);
		#	self.bar.setBackgroundColor(tangoGrey3);
		#	self.bar.setBaseColor(tangoGrey4);
		#	self.status.setImage( "Pile of gold and redstone here.s2g" );

		elif self.action != None: #still in queue
			self.bar.setBackgroundColor(transparency);
			self.bar.setBaseColor(transparency);
			self.status_icon.setImage("/gui/standard/icons/alert_timer.s2g");

		self.status_icon.setSize( w,h );
		
		#called by researchmanager.update??
		#1. ask the queue to determine what the status of this item is
		#2. self.setStatus( the status )
		#3. based on the status, re-configure the bits and bobs

	def onAction(self, e):
		CL_RequestCancel(self.item.builder, self.item.objtype.typeId);


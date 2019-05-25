#copyright (c) 2011 savagerebirth.com
#this file is used for the commhud

import glass;
import savage;
import math;

class RadialContextMenu(ContextMenu):
	RADIUS = 100;
	BUTTON_RADIUS = 16;
	BUTTON_DISTANCE = 100-16;
	def __init__(self):
		self.alphastep = 30;
		
		ContextMenu.__init__(self);
		self.setSize(self.RADIUS*2, self.RADIUS*2);
		self.setAlpha(0);
		
		self.object = None;
		self.validSelection = None;  
		self.action = None;

		self.currentButtons = [];
		self.coords = (0,0);
		self.context = commcontexts.emptycontext;
		self.lastContext = commcontexts.emptycontext;

		gblEventHandler.addGameListener(self);
	
	def rebuildMenu(self):
		#use after the menu has been clear() -ed
		self.bg = glass.GlassLabel();
		self.bg.addMouseListener(self);
		self.bg.setImage("/gui/game/images/contextmenu_bg.s2g");
		self.bg.setForegroundColor(glass.Color(255,255,255,150));
		self.add(self.bg);
		
		#self.main = glass.GlassButton("Default Action");
		#self.main.setWidth(int(0.8*self.RADIUS));
		#self.main.setPosition( (self.getWidth()-self.main.getWidth())//2, (self.getWidth()-self.main.getHeight())//2 );
		#self.main.setClickAction("commhud.defaultAction(); commhud.contextmenu.close();");
		#self.add(self.main);

		self.info = self.InfoContainer();
		self.info.setSize(int(self.RADIUS * 1.2), int(self.RADIUS * 1.2));
		self.add(self.info, "center", "center");	
		
		self.currentButtons = [];
	
	def buildContext(self, context):
		self.lastContext = self.context;
		self.context = context;
		self.clear();
		self.rebuildMenu();
		for action, status in self.context.getContextActions().iteritems():
			button = self.context.getButtonAction(action);
			if status == Hidden:
				button.setVisible(0);
				button.setEnabled(0);
			elif status == Disabled:
				button.setVisible(1);
				button.setEnabled(0);
				button.setForegroundColor(tangoGrey5);
			elif status == Enabled:
				button.setVisible(1);
				button.setEnabled(1);
				button.setForegroundColor(white);
			self.add(button);
			self.currentButtons.append(button);
		
		self.resizeToAlpha();		
	
	def switchContexts(self, ctx):
		Sound_PlaySound("/sound/gui/closecontext.ogg");
		ActionSequence(self.ContractAction(self, "switch"), self.RebuildAction(self, ctx), self.ExpandAction(self, "switch") );

	def resizeToAlpha(self):
		if self.getAlpha() == 0:
			self.setVisible(0);
			return;
		else:
			self.setVisible(1);
 		a = self.getAlpha() / 255.0;
		self.bg.setSize( int(a*self.getWidth()), int(a*self.getHeight()) );
		self.bg.setPosition(int((1-a)*self.getWidth()/2),int((1-a)*self.getHeight()/2));
		angle = math.pi-((1-a)*math.pi/4);
		da = 2*math.pi/self.MAX_BUTTONS;
		self.info.setSize( int(a*self.RADIUS*1.2), int(a * self.RADIUS*1.2));
		self.info.setPosition(self.getWidth() // 2 - self.info.getWidth() //2, self.getHeight() // 2 - self.info.getHeight() //2)

		for button in self.currentButtons:
			x = a*self.BUTTON_DISTANCE * math.sin(angle)+self.RADIUS;
			y = a*self.BUTTON_DISTANCE * math.cos(angle)+self.RADIUS;
			x -= a*self.BUTTON_RADIUS;
			y -= a*self.BUTTON_RADIUS;
			#Big: I kinda like the buttons having static size...
			button.setSize( int(a*self.BUTTON_RADIUS*2) , int(a*self.BUTTON_RADIUS*2) );
			button.setPosition(int(x),int(y));
			
			angle -= da;

	def update(self):
		if self.object != None:
			self.recenter();
			self.info.hp.setProgress(self.object.getHealthPct());
			self.info.hpLabel.setCaption(str(self.object.getHealth()));

			research = savage.getLocalTeam().getResearch();
			active = False;
			for item in research:
				if item.builder == self.object.objectId:
					#self.info.icon.setVisible(1);
					self.info.progress.setProgress(item.percentComplete);
					self.info.icon.build(item);
					#if not self.action:
					active = True;
			if not active:
				self.info.progress.setProgress(0);
				self.info.icon.setVisible(0);

	def recenter(self):		
		x, y = self.object.getScreenTopPosition();
		self.setPosition(int(x) - self.RADIUS, int(y) - self.RADIUS);
	
	def onMouseClick(self, e):
		#if e.widget != 
		commhud.commInput.onMouseClick(e);
		
	def onMouseMotion(self, e):
		pass;
	
	def onMousePress(self, e):
		pass;
	
	def onMouseReleased(self, e):
		pass;
	
	def onMouseDrag(self, e):
		pass;
	
	def onMouseEnter(self, e):
		pass;

	def onMouseExit(self, e):
		pass;
		
	def open(self):
		if not self.isVisible():
			Sound_PlaySound("/sound/gui/opencontext.ogg");
			self.action = ActionSequence(self.ExpandAction(self));
	
	def close(self):
		if self.isVisible():
			Sound_PlaySound("/sound/gui/closecontext.ogg");
			self.action = ActionSequence(self.ContractAction(self));

	def handleSelection(self):

		if self.validSelection and not self.action:
			try:
				ctx = commcontexts.contextDict[self.validSelection.getType().getName()];
			except KeyError:
				# We got a wrong object that has no defined context.
				con_println("^rKeyError in RadialContextMenu");
				self.object = None;
				self.close();
				return;

			# Finally we got a valid context \o/
			ctx.object = self.validSelection;
			self.object = self.validSelection;

			self.buildContext(ctx);

			# The ContextMenu should be always on top of the building!
			objX, objY = self.validSelection.getScreenTopPosition();
			x = int(objX) - self.RADIUS;
			y = int(objY) - self.RADIUS;
			self.setPosition(x, y);
			self.open();

		else:
			self.object = None;
			if self.action:
				return;
			else:
				self.close();

	def newResearch(self, item):
		if self.getAlpha() == 255 and not self.action:
			# Find out what button we have to move:
			for button in self.currentButtons:
				actionName = "Research "+item.getType().getValue("description");
				if actionName == button.name:
					self.action = ActionSequence(self.MoveAction(self, button));
					self.info.icon.build(item);
					self.info.icon.setVisible(0);

					#self.info.icon.icon.setImage(item.getType().getValue("icon") + ".s2g");
					#self.info.icon.setVisible(1);		

			#self.MoveAction
			#self.info.icon.build(item);

	def onSelection(self, e):
		self.validSelection = None;

		if e.isSingle():
			obj = e.selection.list[0];
			if obj.getType().isBuildingType() and not obj.getType().isMine():
				self.validSelection = obj;

		self.handleSelection();
	
	def onEvent(self, e):
		if e.eventType == "research_begin" and self.object:			
			if e.sourceId == self.object.objectId:
				ri = savage.ResearchItem(e.objtype, e.sourceId, savage.getGameTime(), 0);
				self.newResearch(ri);

		elif e.eventType == "research_complete":
			self.buildContext(self.context);
	

	class InfoContainer(DefaultContainer):
		def __init__(self):
			DefaultContainer.__init__(self);

			self.progress = glass.GlassProgressDisc();
			self.progress.setImage("gui/game/images/purple_ring.png");
			self.progress.setAlpha(155)
			self.progress.setSizePct(1,1);
			self.progress.setProgress(0);
			self.add(self.progress);

			self.icon = self.ResearchIcon();
			self.add(self.icon);
			self.icon.setSize(32, 32);
			#self.icon.setVisible(0);

			self.hp = glass.GlassProgressBar();
			self.hp.setBackgroundColor(white);
			#self.hp.setForegroundColor(glass.Color(255,21,22, 128));
			self.hp.setForegroundColor(tools.HSLColor(0.33,0.8,0.66));			
			self.hp.setBackgroundImage("gui/base/images/progress_bg.tga");
			self.hp.setSizePct(0.35, 0.075);
			self.add(self.hp, "center", self.icon.getY() + self.icon.getHeight() + 7);
			self.hp.setProgress(1);

			self.hpLabel = DefaultLabel("9001");
			self.hpLabel.setFont(fontSizeSmall);
			self.add(self.hpLabel, "center", self.hp.getY() - 2);

		def setSize(self, w, h):
			DefaultContainer.setSize(self, w, h);
			self.progress.setSizePct(1, 1);

			self.icon.setSize(32, 32);
			self.icon.setPosition(self.getWidth() // 2 - self.icon.getWidth() // 2, self.getHeight() // 2 - self.icon.getHeight() // 2);

			self.hp.setSizePct(0.35, 0.075);
			self.hp.setPosition(self.getWidth() // 2 - self.hp.getWidth() // 2, self.icon.getY() + self.icon.getHeight() + 7);

			self.hpLabel.setPosition(self.getWidth() // 2 - self.hpLabel.getWidth() // 2, self.hp.getY() - 2);

		class ResearchIcon(DefaultContainer):

			def __init__(self):
				DefaultContainer.__init__(self);
				self.setOpaque(1);
				#self.setBackgroundColor(tangoGreen);

				self.item = None;

				#self.name = glass.GlassLabel(item.getType().getValue("description"));
				#self.name.setPosition(2, 2);
				#self.name.setFont(fontSizeSmall);
				#self.name.setWidth(self.ICON_SIZE);
				#self.name.setAlignment(glass.Graphics.CENTER);
				#self.add(self.name);
				
				self.icon = DefaultImage();
				self.icon.imagePath = "";
				self.icon.setImage("gui/game/images/transparent.s2g");
				self.add(self.icon);
				
				#self.close = glass.ImageButton("close","/gui/standard/cancel.s2g");
				#self.add(self.close, "bottom", "right");
				#self.close.addActionListener(self);

			def build(self, item):
				self.item = item;
				self.icon.setImage(item.getType().getValue("icon")+".s2g");
				self.icon.setOpaque(1);

				self.icon.setSizePct(1, 1);				

			def setSize(self, w, h):
				DefaultContainer.setSize(self, w, h);

				self.icon.setSizePct(1, 1);
				self.icon.setPosition(0,0);

				#self.close.setSizePct(0.25, 0.25);
				#self.close.setPosition(self.getWidth() - self.close.getWidth(), self.getHeight() - self.close.getHeight());

			def onAction(self, e):
				if e.widget.getCaption() == "close" and self.item:
					CL_RequestCancel(self.item.builder, self.item.objtype.typeId);	

	class ExpandAction(Action):
		def __init__(self, menu, flag=None):
			Action.__init__(self);
			self.menu = menu;
			self.flag = flag;
	
		def isDone(self):
			if self.menu.getAlpha() >= 255:
				self.menu.action = None;
				if self.flag != "switch":
					self.menu.handleSelection();				
				return True;
			else:
				return False;
		
		def run(self):
			self.menu.setAlpha( int(min(255,self.menu.getAlpha() + self.menu.alphastep)) );
			self.menu.resizeToAlpha();
	
	class ContractAction(Action):
		def __init__(self, menu, flag=None):
			Action.__init__(self);
			self.menu = menu;
			self.flag = flag;
			
		def isDone(self):
			if self.menu.getAlpha() <= 0:
				self.menu.action = None;
				if self.flag != "switch":
					self.menu.handleSelection();				
				return True;
			else:
				return False;
		
			
		def run(self):
			self.menu.setAlpha( int(max(0,self.menu.getAlpha() - self.menu.alphastep)) );
			self.menu.resizeToAlpha();
		
	class RebuildAction(Action):
		def __init__(self, menu, ctx):
			Action.__init__(self);
			self.menu = menu;
			self.ctx = ctx;
		
		def isDone(self):
			return True;
		
		def run(self):
			self.menu.buildContext(self.ctx);

	class MoveAction(Action):
		def __init__(self, menu, button, qeuePos=0):
			Action.__init__(self);
			self.menu = menu;
			self.button = button;

			self.tx = self.menu.getWidth() // 2 - self.button.getWidth() // 2
			self.ty = self.menu.getHeight() // 2 - self.button.getHeight() // 2
			self.posx = float(self.button.getX());
			self.posy = float(self.button.getY());

			x = (self.tx - self.button.getX());
			y = (self.ty - self.button.getY());
			l = math.hypot(x, y);

			self.dx = (x/l);
			self.dy = (y/l);
			
		def isDone(self):
			x = abs(self.tx - self.posx);
			y = abs(self.ty - self.posy);
			if x < 5 and  y < 5:
				self.button.setPosition(self.tx, self.ty);
				self.menu.action = None;
				self.menu.handleSelection();
				self.menu.info.icon.setVisible(1);
				return True;
			else:
				return False;		
			
		def run(self):
			self.posx += self.dx*3; #instead of a constant factor here, one
			self.posy += self.dy*3; #could experiement with polynomial or trig functions
			self.button.setPosition(int(self.posx), int(self.posy));


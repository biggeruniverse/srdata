#copyright (c) 2011 savagerebirth.com
#this file is used for the commhud

import glass;
import savage;
import math;

class ContextMenu(glass.GlassContainer):
	def __init__(self):
		self.alphastep = 30;
		self.RADIUS = 100;
		self.BUTTON_RADIUS = 16;
		self.BUTTON_DISTANCE = self.RADIUS - self.BUTTON_RADIUS;
		self.MAX_BUTTONS = 12;
		
		glass.GlassContainer.__init__(self);
		self.setSize(self.RADIUS*2, self.RADIUS*2);
		self.setAlpha(0);
		
		self.object = None;
		self.currentButtons = [];
		self.coords = (0,0);
		self.context = commcontexts.emptycontext;
		self.lastContext = commcontexts.emptycontext;
	
	def rebuildMenu(self):
		#use after the menu has been clear() -ed
		self.bg = glass.GlassLabel();
		self.bg.addMouseListener(self);
		self.bg.setImage("/gui/standard/contextmenu_bg.s2g");
		self.bg.setForegroundColor(glass.Color(255,255,255,150));
		self.add(self.bg);
		
		#self.main = glass.GlassButton("Default Action");
		#self.main.setWidth(int(0.8*self.RADIUS));
		#self.main.setPosition( (self.getWidth()-self.main.getWidth())//2, (self.getWidth()-self.main.getHeight())//2 );
		#self.main.setClickAction("commhud.defaultAction(); commhud.contextmenu.close();");
		#self.add(self.main);
		
		self.currentButtons = [];
	
	def buildContext(self, context):
		self.lastContext = self.context;
		self.context = context;
		self.clear();
		self.rebuildMenu();
		for action, status in self.context.getContextActions().iteritems():
			button = self.context.getButtonAction(action);
			if status == Hidden:
				button.setVisible(False);
				button.setEnabled(0);
			elif status == Disabled:
				button.setVisible(True);
				button.setEnabled(0);
				button.setForegroundColor(tangoGrey5);
			elif status == Enabled:
				button.setVisible(True);
				button.setEnabled(1);
				button.setForegroundColor(white);
			self.add(button);
			self.currentButtons.append(button);
		
		self.resizeToAlpha();
	
	def switchContexts(self, ctx):
		Sound_PlaySound("/sound/gui/closecontext.ogg");
		ActionSequence(self.ContractAction(self), self.RebuildAction(self, ctx), self.ExpandAction(self) );
	
	def resizeToAlpha(self):
		if self.getAlpha() == 0:
			self.setVisible(False);
			return;
		else:
			self.setVisible(True);
 		a = self.getAlpha() / 255.0;
		self.bg.setSize( int(a*self.getWidth()), int(a*self.getHeight()) );
		self.bg.setPosition(int((1-a)*self.getWidth()/2),int((1-a)*self.getHeight()/2));
		angle = math.pi-((1-a)*math.pi/4);
		da = 2*math.pi/self.MAX_BUTTONS;
		for button in self.currentButtons:
			x = a*self.BUTTON_DISTANCE * math.sin(angle)+self.RADIUS;
			y = a*self.BUTTON_DISTANCE * math.cos(angle)+self.RADIUS;
			x -= a*self.BUTTON_RADIUS;
			y -= a*self.BUTTON_RADIUS;
			#Big: I kinda like the buttons having static size...
			button.setSize( int(a*self.BUTTON_RADIUS*2) , int(a*self.BUTTON_RADIUS*2) );
			button.setPosition(int(x),int(y));
			
			angle -= da;
	
	def onMouseClick(self, e):
		#if e.widget != 
		commhud.comminputhandler.onMouseClick(e);
		

	def onMouseMotion(self, e):
		pass;
	
	def onMousePress(self, e):
		pass;
	
	def onMouseReleased(self, e):
		pass;
	
	def onMouseDrag(self, e):
		pass;
	
	def open(self):
		Sound_PlaySound("/sound/gui/opencontext.ogg");
		ActionSequence(self.ExpandAction(self));
	
	def close(self):
		if self.isVisible():
			Sound_PlaySound("/sound/gui/closecontext.ogg");
			ActionSequence(self.ContractAction(self));
	
	class ExpandAction(Action):
		def __init__(self, menu):
			Action.__init__(self);
			self.menu = menu;
	
		def isDone(self):
			return self.menu.getAlpha() >= 255;
		
		def run(self):
			self.menu.setAlpha( int(min(255,self.menu.getAlpha() + self.menu.alphastep)) );
			self.menu.resizeToAlpha();
	
	class ContractAction(Action):
		def __init__(self, menu):
			Action.__init__(self);
			self.menu = menu;
			
		def isDone(self):
			return self.menu.getAlpha() <= 0;
			
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

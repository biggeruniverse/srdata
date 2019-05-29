# (c) 2011 savagerebirth.com

from silverback import *;
import savage;

class HostServerWindow(glass.GlassWindow):
	def __init__(self):
		glass.GlassWindow.__init__(self, "Host Server");		
		self.setSizePct(0.45, 0.4);
		self.setBackgroundColor(glass.Color(0,0,0,128));
		self.setTitleVisible(0);
		self.setVisible(False);			
		
		self.gametypeLabel = glass.GlassLabel("Gametype");
		self.add(self.gametypeLabel);
		self.gametypeLabel.setPositionPct(0.075,0.05);
		
		self.gametype = glass.GlassDropMenu();
		self.gametype.linkCvar("sv_gametype");
		self.gametype.addOption("RTSS","0");
		self.gametype.addOption("Duel","1");		
		self.add(self.gametype);
		self.gametype.setPosition(int((1.5* self.gametypeLabel.getX()) + self.gametypeLabel.getWidth()),self.gametypeLabel.getY());
		self.gametype.setWidth(int(self.getWidth()*0.15));		

		self.overhead = glass.ImageButton();
		self.add(self.overhead);
		self.overhead.setPosition(int(self.getWidth()*0.5),int((2* self.gametypeLabel.getY()) + self.gametypeLabel.getHeight()));		
		self.overhead.setBackgroundColor(white);
		self.overhead.setImage("/world/eden2_overhead.jpg");
		self.overhead.setSize(int(0.25*screenHeight),int(0.25*screenHeight));		
		
		self.select_map = glass.GlassListBox();	
		self.select_map.addSelectionListener(self);
		self.select_map.setBackgroundColor(white);

		self.mapScroll = glass.GlassScrollArea(self.select_map);			
		self.mapScroll.setPosition(self.gametypeLabel.getX(), self.overhead.getY());
		self.mapScroll.setSize((self.gametype.getWidth() + self.gametype.getX())-self.mapScroll.getX(),self.overhead.getHeight());
		self.add(self.mapScroll);				
		
		self.close = glass.GlassButton("Close");
		self.add(self.close);		
		self.close.setPositionPct(0.075,0.85);
		self.close.addActionListener(self);	
		
		self.startserver = glass.GlassButton("Start Server >>");		
		self.add(self.startserver);
		self.startserver.setPosition(self.overhead.getX() + self.overhead.getWidth() - self.startserver.getWidth(),self.close.getY());
		self.startserver.addActionListener(self);
		
		self.settings = glass.GlassButton("Settings");		
		self.add(self.settings);
		self.settings.setPosition(self.overhead.getX(),self.gametype.getY());
		self.settings.addActionListener(self);
		
		
	def showHostServerWindow(self):
		if self.isVisible():
			self.setVisible(False);
		else: 
			self.requestMoveToTop();
			self.setVisible(True);	
			self.select_map.clear();
			paths = File_ListFiles("/world","*.s2z",0);
			for path in paths:
				name = path.rsplit("/",1)[1][:-4];
				self.select_map.addItem(name);
			self.select_map.setSelected(0);
	
	def hostServer(self):
		self.setVisible(False);
		World_Load(self.select_map.getItem(self.select_map.getSelected()));
	
	def onValueChanged(self, e):
		value = e.widget.getItem(e.widget.getSelected());
		overhead_path = "/world/" + value + "_overhead.jpg";
		self.overhead.setImage(overhead_path);
		self.overhead.setSize(int(0.248*screenHeight),int(0.248*screenHeight));
		pass;
		
	def onAction(self, e):
		if e.widget.getCaption() == "Start Server >>":
			self.hostServer();
		elif e.widget.getCaption() == "Close":			
			self.setVisible(False);
		elif e.widget.getCaption() == "Settings": #TODO
			pass;

# (c) 2011 savagerebirth.com
# this file creates the stats window for a given player
from silverback import *;
import glass;

totalsIndex = {"Username":None, "Nickname":None};
def buildTable(dict):
	table = GlassTablePlus()
	table.setFrame(0)
	for name in dict.keys():
		data = glass.GlassLabel("Loading")
		table.addLabelledRow(name,  data)
		dict[name] = data
	return table

class StatsWindow(glass.GlassWindow):
	def __init__(self, playerName):
		glass.GlassWindow.__init__(self, playerName+" Stats & Rankings");
		self.httpHandle = -1;
		self.player = playerName;
		self.setBackgroundColor(glass.Color(0,0,0,128));
		self.spinner = glass.GlassLabel();
		self.spinner.setImage("textures/econs/loading/loading0000.s2g");
		self.spinner.setSize(32,32);
		self.add(self.spinner);

		self.title = glass.GlassLabel(self.player+" Stats & Rankings");
		self.add(self.title);

		#create the tabs
		self.tabs = glass.GlassTabbedContainer();
		self.tabs.setOpaque(0)
    
		self.add(self.tabs)
		self.tabs.setSizePct(1,.9)

		self.setTitleVisible(0);
		
		button = glass.GlassButton("Close");
		self.add(button);
		button.addActionListener(self);

		gblEventHandler.addHttpListener(self);

	def show(self, player = None):
		if player is not None:
			self.player = player;
		self.httpHandle = HTTP_Get(cvar_get("auth_requesturl")+"/user/"+self.player);
		self.spinner.setVisible(1);
		self.tabs.setVisible(0);
		self.spinner.setPosition(self.getWidth()/2-16, self.getHeight()/2-16);
		self.title.setCaption("^y"+self.player+" ^wStats & Rankings");
		self.title.setPosition(self.getWidth()/2-self.title.getWidth()/2, 1);
		self.setVisible(1);

	def buildStats(self, xml):
		con_println(xml+"\n");

	def onAction(self, e):
		self.releaseModalFocus();
		self.setVisible(0);

	def onEvent(self, e):
		if e.handle == self.httpHandle:
			if e.responseCode != 200:
				return;
			self.spinner.setVisible(0);
			self.httpHandle = -1;

			self.buildStats(e.responseMessage);
			self.spinner.setVisible(0);
			self.tabs.setVisible(1);


# copyright (c) 2011 savagerebirth.com
# this file lets popular people stalk and be stalked by their buddies in-game

from silverback import *;
import glass;

class Buddy:
	def __init__(self, name, status=False):
		self.name = name; #these are intended to be USERNAMES, realnames
		self.connected = status;
		self.status = "";

	def __lt__(self, other):
		return self.name < other.name;
	
	def __eq__(self, other):
		if isinstance(other, str):
			return self.name == other;
		return self.name == other.name;
	
	def __str__(self):
		return "Buddy object for " + self.name + ". Connected: "+str(self.connected);
	
	def isOnline(self):
		return self.connected;

class BuddyListManager:
	ACCEPTED_SCOPES = ("irc_join","irc_quit","irc_connect");
	BUDDYLIST_PATH = "/settings/buddylist.list"; #any objections?
	def __init__(self):
		self.lists = [];  #list is a BuddyListGUI instances
		self.buddies = []; #list of Buddy instances
		gblEventHandler.addNotifyListener(self);
	
	def addList(self, list): 
		self.lists.append(list);
		
	def updateLists(self):
		onlinelist = [buddy for buddy in self.buddies if buddy.isOnline()];
		onlinecount = len(onlinelist);
		
		for list in self.lists:
			list.update(self.buddies, onlinelist, onlinecount);
		
	def addBuddy(self,buddy_name):
		if not self.isBuddy(buddy_name):
			self.buddies.append(Buddy(buddy_name));
			self.buddies.sort(); #this is a mutator, I always forget that
			self.writeBuddies();
	
	def removeBuddy(self, buddy_name):
		#TODO add in /deletebuddy in hcc
		for i, buddy in enumerate(self.buddies):
			if buddy.name == buddy_name:
				self.buddies.pop(i); #if it was sorted before, it's sorted now
				self.writeBuddies();
				break;
	
	def getBuddies(self):
		online_users = IRC_GetChannelUsers();
		for buddy in self.buddies:
			buddy.connected = buddy.name in online_users;
			#self.buddies modified in-place yuss, like a boss
		return self.buddies;
	
	def getBuddyByName(self, buddy_name):
		for buddy in self.buddies:
			if buddy.name == buddy_name:
				return buddy;
	
	def isBuddy(self, name):
		for buddy in self.buddies:
			if buddy.name == name:
				return True;
		return False;
		
	def readBuddies(self):
		f = File_Open(self.BUDDYLIST_PATH, "r");
		self.buddies = [];
		for line in File_ReadLines(f):
			buddy = Buddy(line);
			if buddy not in self.buddies:
				self.buddies.append(buddy);
		File_Close(f);
		self.getBuddies(); #self.buddies modified in-place
		self.updateLists();
		
	def writeBuddies(self):
		f = File_Open(self.BUDDYLIST_PATH,"w");
		for buddy in self.buddies:
			File_Write(f, buddy.name+"\r\n");
		File_Close(f);
		self.updateLists();
		
	def onEvent(self, e):
		if e.scope not in self.ACCEPTED_SCOPES:
			return;
		
		if e.scope == "irc_connect":
			self.readBuddies(); #this calls updateLists();
			return;
		if not self.isBuddy(e.fromstr):
			return;
		if e.scope == "irc_join":
			self.getBuddyByName(e.fromstr).connected = True;
		elif e.scope == "irc_quit":
			self.getBuddyByName(e.fromstr).connected = False;


gblBuddyManager = BuddyListManager();

#is this the like list of buddies? yes, the bit of gui that appears in serverlist, lobby or wherever ok
class BuddyListGUI(glass.GlassContainer):
	WIDTH_PROPORTION = 0.22;
	HEIGHT_PROPORTION = 0.45;
	PADDING = 3;
	
	def __init__(self):
		glass.GlassContainer.__init__(self);
		gblBuddyManager.addList(self);
		
		self.setSizePct(self.WIDTH_PROPORTION, self.HEIGHT_PROPORTION);
		self.toggle = glass.GlassButton("0");
		#either add in a custom button background here, including the buddy logo
		#or just bodge it with ^icon^
		#wtf was I thinking, GlassButton accepts an icon param
		self.toggle.setY( self.getHeight() - self.toggle.getHeight());
		self.toggle.addMouseListener(self);
		self.add(self.toggle);
		
		self.window = glass.GlassWindow();
		self.window.setCaption("Buddies");
		self.window.setAlpha(0);
		self.window.setVisible(0);
		self.window.setMovable(0);
		self.window.setSize(self.getWidth(), self.getHeight() - self.toggle.getHeight());
		self.window.setPosition(0,0);
		self.add(self.window);
		
		ca = self.window.getChildrenArea();
		
		self.new = glass.ImageButton();
		self.new.setImage("/gui/standard/icons/plus.s2g");
		self.new.setX(ca.width - self.PADDING - self.new.getWidth());
		self.new.addMouseListener(self);
		self.window.add(self.new);
		
		self.input = glass.GlassTextField("Add new...");
		self.input.setX( self.PADDING );
		self.input.setWidth( self.new.getX() - self.PADDING - self.input.getX() );
		self.input.addMouseListener(self);
		self.window.add(self.input);
		
		y2 = max(self.new.getHeight(),self.input.getHeight());
		y1 = ca.height - y2;
		self.new.setY( y1 + (y2-self.new.getHeight())//2 );
		self.input.setY( y1 + (y2-self.input.getHeight())//2 );
			
		self.listbox = glass.GlassListBox();
		self.listbox.setBackgroundColor(transparency);
		
		self.scroll = glass.GlassScrollArea(self.listbox);
		self.scroll.setSize( ca.width, y1 - self.PADDING);
		self.window.add(self.scroll);
		self.listbox.setWidth(ca.width - self.scroll.getScrollbarWidth());
	
	def setAlignment(self, align):
		offset = self.getWidth() - self.toggle.getWidth();
		if align == glass.Graphics.CENTER:
			offset //= 2;
		elif align == glass.Graphics.LEFT:
			offset = 0;
		self.toggle.setX(offset);
		self.toggle.setAlignment(align);

	def onMouseClick(self, e):
		if e.widget == self.toggle:
			self.toggleWindow();
		elif e.widget == self.new:
			name = self.input.getText();
			if name != "Add new...":
				gblBuddyManager.addBuddy( name );
				self.input.setText("Add new...");
	
	def onMousePress(self, e):
		if e.widget == self.input:
			if self.input.getText() == "Add new...":
				self.input.setText("");
			e.widget.onMousePressed();
			#TODO make this work
	def onMouseMotion(self, e): 
		pass;
	def onMouseReleased(self, e):
		pass;
	def onMouseDrag(self, e):
		pass;
	def newRow(self,name="",icon=None,online=False):
		#icon for clan icons (#TODO)
		delete = glass.ImageButton();
		delete.setImage("/gui/standard/icons/minus.s2g");
		delete.setClickAction("gblBuddyManager.removeBuddy("+name+");");
		
		if icon == None:
			icon = "^icon transparent^";
		#else, determine the ^icon string for the user's clan icon
		
		label = glass.GlassLabel(icon + name);
		label.setX(delete.getX() + delete.getWidth() + self.PADDING);
		label.setWidth(self.listbox.getWidth() - label.getX());
		label.setForegroundColor(tangoGrey3 if not online else white);
		
		container = glass.GlassContainer();
		container.add(label);
		container.add(delete);
		container.setWidth(self.listbox.getWidth());
		h = max(label.getHeight(), delete.getHeight());
		container.setHeight(h);
		label.setY((h-label.getHeight())//2);
		delete.setY((h-delete.getHeight())//2);
		
		self.listbox.addWidgetItem(container);
		
	def update( self, buddylist, onlinelist, onlinecount):
		self.toggle.setCaption(str(onlinecount));
		offlinelist = [buddy for buddy in buddylist if buddy not in onlinelist ];
		self.listbox.clear();
		for buddy in buddylist:
			self.newRow(buddy.name,online=buddy.connected);
			#TODO pass in the clan icon
	
	def toggleWindow(self):
		if self.window.getAlpha() == 0:
			ActionSequence(FadeInAction(self.window));
		else:
			ActionSequence(FadeOutAction(self.window));
		#I think, need to check this


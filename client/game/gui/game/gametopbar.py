
from silverback import *;

class GameTopBar(MainTopBar):
	def __init__(self):
		MainTopBar.__init__(self);	
		self.mousemode = getMouseMode();	

		self.setHeight(screenHeight);
		self.setBackgroundColor(glass.Color(0,0,0,128));
		# Yey for overlay-feeling

		## Graphics Panel ##

		self.graphicspanel = GraphicsPanel();		
		self.add(self.graphicspanel);
		self.graphicspanel.setPosition(20, screenHeight // 2 - self.graphicspanel.getHeight() // 2);

	def buildLeftContainer(self):
		left = MainTopBar.buildLeftContainer(self);
		left.home.setClickAction("""GUI_ShowScreen('mainmenu');mainmenu.showModule('menu');""");
		

		return left;
	
	def buildAuthedContainer(self):
		authed = MainTopBar.buildAuthedContainer(self);

		# We need to change a few things:

		# Demos will change to options:
		authed.middle.demos.setImage("icons/options.png")
		authed.middle.demos.setSize(21, 21);
		authed.middle.demos.addActionListener(self);

		# No logging out, lobby instead:		
		authed.middle.logout.setImage("icons/lobby.png")
		authed.middle.logout.setSize(21, 21);
		authed.middle.logout.addActionListener(self);

		# Update the username:
		username = DefaultLabel(cvar_get("username"));
		authed.middle.add(username, "center", "center");
		# Update clickactions:
		authed.right.chat.setClickAction("hud.topBar.openChat()");

		return authed;

	#def buildUnauthedContainer(self):
	#	pass;

	def isAuthed(self):
		# check if we're authed:
		if cvar_get("auth_sessionid") != "":
			return True;
		else:
			return False;

	def addChat(self):
		self.buddyRoster.test = "HUD"
		# Hack them directly on the current screen!
		self.add(self.buddyRoster, screenWidth - self.buddyRoster.getWidth() - 5, self.sectionHeight);
		self.add(self.chatBox, screenWidth // 2 - self.chatBox.getWidth() // 2, screenHeight // 2 - self.chatBox.getHeight() // 2);

	def setVisible(self, v):
		MainTopBar.setVisible(self, v);

		self.authed.setVisible( self.isAuthed() );
		self.notAuthed.setVisible( not self.isAuthed() );

		if v:			
			self.mousemode = getMouseMode();
			#if self.mousemode == MOUSE_FREE:
			#	self.mousemode = MOUSE_RECENTER; #stop the gui from getting the main game stuck
			setMouseMode(MOUSE_FREE);
		else:
			setMouseMode(self.mousemode);

	def openChat(self):

		if self.buddyRoster.isVisible() != self.chatBox.isVisible():
			self.buddyRoster.setVisible(True);
			self.chatBox.setVisible(True);
			return;
		self.buddyRoster.setVisible(not self.buddyRoster.isVisible());
		self.chatBox.setVisible(not self.chatBox.isVisible());

	# Stuff we don't need from MainTopBar:
	def doAutoLogin(self):
		pass;

	def startLogin(self):
		pass;

	def startLogout(self):
		pass;

	def onAction(self, e):
		if e.widget == self.authed.middle.logout:
			if savage.getLocalPlayer().getStatus() == PLAYER_STATUS_UNITSELECT:
				CL_RequestLobby();
			else:
				spechud.setMode('lobby');
				GUI_ShowScreen('spechud');
		elif e.widget == self.authed.middle.demos:
			self.graphicspanel.setVisible(not self.graphicspanel.isVisible());

	def onEvent(self, e):
		pass;

	def onKeyPress(self, e):
		pass;
			
	def onKeyReleased(self, e):
		pass;
	

# (c) 2011 savagerebirth.com

from silverback import *;
import logging;
import glass;
from sleekxmpp import JID;
import stackless;

logger = logging.getLogger("gui");

class MainTopBar(DefaultContainer):
	def __init__(self):
		
		self.httpHandle = -1;
		DefaultContainer.__init__(self);
		
		# loggin in = 1
		# logging out = 2
		# not working = 0
		self.status = 0;
		
		self.setSize(screenWidth, 40);
		
		bg = DefaultImage();
		bg.setImage("top_bar.s2g");
		bg.setSize(screenWidth, 32);
		self.add(bg);
		
		self.sectionWidth = screenWidth // 4;
		self.sectionHeight = 35;
		
		self.left = self.buildLeftContainer();
		self.authed = self.buildAuthedContainer();
		self.notAuthed = self.buildUnauthedContainer();
		
		self.loginOverlay = DefaultContainer();
		self.loginOverlay.setBackgroundColor(glass.Color(0, 0, 0, 153));
		self.loginOverlay.setSize(screenWidth, 31);
		self.loginOverlay.setOpaque(True);
		self.loginOverlay.setVisible(False);
		
		self.loginOverlayLabel = DefaultLabel("Logging in...");
		self.loginOverlay.add(self.loginOverlayLabel, "center", "center");
		
		self.add(self.loginOverlay);

		# chat roster stuff, will get added later to the screen, even if it is a bit hacky...
		self.buddyRoster = BuddyRoster();
		self.buddyRoster.setVisible(False);
		self.buddyRoster.setOpaque(True);
		self.chatBox = JabberChatBox();
		self.chatBox.setId("chat")
		self.chatBox.setVisible(False);

		self.addChat();

		gblEventHandler.addHttpListener(self);
		
		#self.doAutoLogin();

		self.notehandler = NotificationHandler();
		glass.GUI_GetScreen(glass.GUI_CurrentScreen()).add(self.notehandler);
		self.notehandler.setPosition(screenWidth - self.notehandler.getWidth() - 10, self.getHeight() + 10);
		
	def buildLeftContainer(self):
		left = DefaultContainer();
		left.setSize(self.sectionWidth + 30, self.sectionHeight);
		self.add(left);
		
		time = Clock();
		left.add(time, 10, "center");
		
		x = time.getWidth() + 9;
		incX = 30;

		left.home = MainIcon("home");
		left.home.setClickAction("mainmenu.showModule('menu')");
		left.add(left.home, x, "center");
		
		#log = MainIcon("log");
		#log.setClickAction("mainmenu.showPopup('log', 'below');");
		#left.add(log, x, "center");
		
		return left;
	
	def buildAuthedContainer(self):
		
		authed = DefaultContainer();
		authed.setSize(self.sectionWidth * 3, self.sectionHeight);
		authed.setVisible(False);
		self.add(authed, self.sectionWidth);
		
		middle = DefaultContainer();
		middle.setSize(self.sectionWidth * 2, self.sectionHeight);
		authed.add(middle);
		
		username = DefaultContainer();
		username.setBackgroundColor(glass.Color(0, 0, 0, 70));
		username.setOpaque(True);
		username.setSize(150, 19);
		middle.add(username, "center", "center");

		middle.logout = MainIcon("logout");
		middle.logout.setCaption("logoutConfirm");
		middle.logout.addActionListener(self);
		middle.add(middle.logout, 95, "center", "center");
		
		stats = MainIcon("stats");
		stats.setClickAction("mainmenu.showModule('stats');mainmenu.modules['stats'].createStats(cvar_get('auth_sessionid'))");
		middle.add(stats, 125, "center", "center");

		clans = MainIcon("clans");
		clans.setClickAction("mainmenu.showModule('clans')");
		middle.add(clans, username.getX() - clans.getWidth() - 9, "center")

		middle.demos = MainIcon("demos");
		middle.demos.setClickAction("mainmenu.showModule('demos')");
		middle.add(middle.demos, username.getX() - middle.demos.getWidth()*2 - 18, "center");		

		
		self.confirmLogout = DefaultConfirm("Are you sure you want to logout?", None, "Logout");
		self.confirmLogout.ok.addActionListener(self);
		import mainmenu;
		mainmenu.add(self.confirmLogout);
		
		right = DefaultContainer();
		right.setSize(self.sectionWidth, self.sectionHeight);
		authed.add(right, self.sectionWidth * 2);

		right.chat = MainIcon("chat");
		right.chat.setClickAction("mainmenu.topBar.openChat()");
		right.add(right.chat, right.getWidth() - right.chat.getWidth() - 10, "center");		
		
		authed.middle = middle;
		authed.right = right;

		return authed;
	
	def buildUnauthedContainer(self):
		
		notAuthed = DefaultContainer();
		notAuthed.setSize(self.sectionWidth * 3, self.sectionHeight);
		#notAuthed.setVisible(False);
		self.add(notAuthed, self.sectionWidth);

		notAuthed.right = DefaultContainer();
		notAuthed.right.setSize(self.sectionWidth * 2, self.sectionHeight);
		notAuthed.add(notAuthed.right);
		
		autoLogin = DefaultCheckBox();
		autoLogin.linkCvar("autologin");
		notAuthed.right.add(autoLogin, 5, 2, "right", "center");
		
		autoLoginLabel = DefaultLabel("Auto Login: ");
		notAuthed.right.add(autoLoginLabel, autoLogin.getWidth(), "center", "right");
		
		plus = autoLogin.getWidth() + autoLoginLabel.getWidth();
		bgColor = glass.Color(18, 5, 4);
		fgColor = glass.Color(180, 180, 180);
		
		self.username = DefaultTextField(cvar_get("username"));
		self.username.setPlaceHolder("Username...");
		self.username.setBackgroundColor(bgColor);
		self.username.setForegroundColor(fgColor);
		self.username.setSize(110, 20);
		self.username.addKeyListener(self);
		notAuthed.right.add(self.username, 171 + plus, "center", "right");
		
		self.password = DefaultTextField(cvar_get("password"));
		self.password.setPlaceHolder("password...");
		self.password.setBackgroundColor(bgColor);
		self.password.setForegroundColor(fgColor);
		self.password.setSize(110, 20);
		self.password.addKeyListener(self);
		self.password.setHidden(True);
		notAuthed.right.add(self.password, 51 + plus, "center", "right");
		
		submit = MainIcon("go");
		submit.setCaption("login");
		submit.addActionListener(self);
		notAuthed.right.add(submit, 20 + plus, "center", "right");
		
		label = DefaultLabel("Login:");
		notAuthed.right.add(label, 281 + plus, "center", "right");
		
		return notAuthed;

	def setVisible(self, v):
		DefaultContainer.setVisible(self, v);
		self.notehandler.setVisible(v);
		if not v:
			self.chatBox.setVisible(v);
			self.buddyRoster.setVisible(v);

	def addChat(self):
		# Hack them directly on the current screen!
		glass.GUI_GetScreen(glass.GUI_CurrentScreen()).add(self.buddyRoster);
		glass.GUI_GetScreen(glass.GUI_CurrentScreen()).add(self.chatBox);
		self.buddyRoster.setPosition(screenWidth - self.buddyRoster.getWidth() - 5, self.sectionHeight);
		self.chatBox.setPosition(screenWidth // 2 - self.chatBox.getWidth() // 2, screenHeight // 2 - self.chatBox.getHeight() // 2);
		
	def doAutoLogin(self):
		if cvar_getvalue("autologin") == 1:
			self.startLogin(True);
		
	def startLogin(self, auto=False):
		if cvar_get("auth_sessionid") == "":
			
			self.doingAuto = auto;
			
			if auto == False:             
				username = self.username.getText();
				password = self.password.getText();
			
				if username == "" or password == "":                
					mainmenu.alert("Please enter a username and password.");
					return;
			
				cvar_set("username", username);
				cvar_set("password", password);
		
				self.password.setText("");
		
			self.notAuthed.setVisible(False);
			self.loginOverlayLabel.setCaption("^icon loading/loading0000^Logging in...");
			self.loginOverlay.setVisible(True);
			
			cvar_set("auth_requesturl", ApiUrl);
			self.httpHandle = CL_Auth_Authenticate();
			
			self.status = 1;
		
	def startLogout(self):
		# Tell Sleek it should log out too:
		#task = stackless.tasklet(gblXMPPHandler.xmpp.disconnect());
		#task.setup();
		gblXMPPHandler.chatEvent("chat_logout", "", "User logged out.");
		self.status = 2;
		self.httpHandle = CL_Auth_Logout();
		cvar_set("auth_sessionid", "");
		cvar_set("username", "");
		cvar_set("password", "");
		
		self.authed.setVisible(False);
		self.loginOverlayLabel.setCaption("^icon loading/loading0000^Logging out...");
		self.loginOverlay.setVisible(True);

	def openChat(self):
		if self.buddyRoster.isVisible() != self.chatBox.isVisible():
			self.buddyRoster.setVisible(True);
			self.chatBox.setVisible(True);
			return;

		self.buddyRoster.setVisible(not self.buddyRoster.isVisible());
		self.chatBox.setVisible(not self.chatBox.isVisible());


	def onAction(self, e):
		
		if e.widget.getCaption() == "login":
			self.startLogin();
		elif e.widget.getCaption() == "logoutConfirm":
			self.confirmLogout.setVisible(True);
		elif e.widget.getCaption() == "Logout":
			self.confirmLogout.setVisible(False);
			self.startLogout();
		
	def onEvent(self, e):
		if e.handle == self.httpHandle and (self.status == 1 or self.status == 2):
			self.loginOverlay.setVisible(False);
			
			if self.status == 2:
				self.notAuthed.setVisible(True);
				self.status = 0;
				self.httpHandle = -1;
				return;
		   
			try: 
				if e.responseCode == 202:
					dom = xml.dom.minidom.parseString(e.responseMessage);
					authNode = dom.getElementsByTagName("auth")[0];
				
					sessionNode = authNode.getElementsByTagName("user")[0];
					cvar_set("auth_sessionid", sessionNode.getAttribute("session"));
					cvar_set("auth_guid", sessionNode.getAttribute("id"));

					cvar_set("username", self.username.getText());
					if cvar_get("name") == "UnnamedNewbie":
						cvar_set("name", self.username.getText());
					self.authed.setVisible(True);
				
					username = DefaultLabel(str(sessionNode.getAttribute("name")));
					self.authed.middle.add(username, "center", "center");

					dom.unlink();
					gblEventHandler.notifyEvent("auth", "", "login");

					#make sure chat gets connected now
					#Big: I put it in it's own tasklet, or else it blocks the eventhandler the whole time it is connecting
					#DoF: If we were already connected and logged out, just reconnect.
					#if gblXMPPHandler.xmpp == None:
					connection = gblXMPPHandler.connect
					#else:
					#connection = gblXMPPHandler.reconnect
					task = stackless.tasklet(connection);
					task.setup();

				else:
					cvar_set("auth_sessionid", "");
					cvar_set("username", "");
					cvar_set("password", "");
				
					if self.doingAuto == False:
						errorNode = xml.dom.minidom.parseString(e.responseMessage).getElementsByTagName("error")[0];
						message = errorNode.getElementsByTagName("message")[0];
						mainmenu.alert(str(message.childNodes[0].nodeValue));
				
					self.notAuthed.setVisible(True);
			except:
				logger.error("Unexpected error parsing login data!\n");
				self.notAuthed.setVisible(True);
			
			self.status = 0;
			self.httpHandle = -1;
			
			
				
	def onKeyPress(self, e):
		if e.key == glass.Key.ENTER:
			self.startLogin();
		#elif e.key == glass.Key.TAB:
		#    self.focusNext();
			
	def onKeyReleased(self, e):
		pass;

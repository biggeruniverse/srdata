import logging;
import glass;
from sleekxmpp import JID

logger = logging.getLogger("gui")


class BuddyRoster(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		self.setFrameStyle("TrimmedEight");
		self.setBackgroundColor(windowBackground);
		self.lastClickTime = 0;
		self.lastClickSelect = -1;	

		self.activeList = None;	

		self.setSize(200, 500);

		self.widgets = {}; # {"group": grouplist}

		# The dict that keeps trac of the contacts
		self.contacts = {}; # {group: {'jid': name, "status": status }}

		top = DefaultContainer();
		self.add(top, 0, 0);
		top.setSize(self.getWidth(), 35);
		top.setBackgroundColor(windowTop);

		title = DefaultLabel("Buddy List");
		title.setForegroundColor(tangoYellowDark);
		title.setFont(fontSizeLarge);
		top.add(title, "center", "center");

		# Init the group tabs

		self.rosterGroup = glass.GlassTabbedContainer();
		self.rosterGroup.setWidth(self.getWidth() - 5);

		self.scroll = glass.GlassScrollArea(self.rosterGroup);
		self.scroll.setSize(self.getWidth() - 5, self.getHeight() - 60);
		self.scroll.setBackgroundColor(transparency);
		self.scroll.setHorizontalScrollPolicy(glass.GlassScrollArea.SHOW_NEVER);
		self.add(self.scroll, 0, 35);
		#self.buildList();

		# control bar

		self.diff = inputLineHeight + 2

		self.controlBar = DefaultContainer();
		self.controlBar.setBackgroundColor(glass.Color(0,0,0,128));
		self.controlBar.setSize(self.getWidth(), inputLineHeight + 35);
		self.add(self.controlBar, 0, self.getHeight() - self.controlBar.getHeight() + self.diff);

		self.addFriend = DefaultButton(" + ");
		self.addFriend.setSize(20, 20);
		self.addFriend.addActionListener(self);

		self.deleteFriend = DefaultImageButton();
		self.deleteFriend.setImage("icons/logout.png");
		self.deleteFriend.setSize(20, 20);
		self.deleteFriend.setCaption("delete");
		self.deleteFriend.addActionListener(self);

		self.deleteOverlay = DefaultContainer();
		self.deleteOverlay.setBackgroundColor(glass.Color(0,0,0,200));
		self.deleteOverlay.setSize(20,20);

		self.stats = DefaultImageButton();
		#stats.setClickAction("mainmenu.showModule('stats')"); TODO
		self.stats.setImage("icons/stats.png");
		self.stats.setSize(20, 20);
		self.stats.setCaption("stats");
		self.stats.addActionListener(self);

		self.statsOverlay = DefaultContainer();
		self.statsOverlay.setBackgroundColor(glass.Color(0,0,0,200));
		self.statsOverlay.setSize(20,20);

		self.match = DefaultImageButton();
		#stats.setClickAction("mainmenu.showModule('stats')"); TODO
		self.match.setImage("icons/lobby.png");
		self.match.setSize(20, 20);
		self.match.setCaption("match");
		self.match.addActionListener(self);

		self.matchOverlay = DefaultContainer();
		self.matchOverlay.setBackgroundColor(glass.Color(0,0,0,200));
		self.matchOverlay.setSize(20,20);

		self.controlBar.add(self.addFriend, 5, 5);
		self.controlBar.add(self.deleteFriend, 30, 5);
		self.controlBar.add(self.stats, 55, 5);
		self.controlBar.add(self.match, 80, 5);

		self.controlBar.add(self.deleteOverlay, 30, 5);
		self.controlBar.add(self.statsOverlay, 55, 5);
		self.controlBar.add(self.matchOverlay, 80, 5);

		self.enterName = DefaultTextBox();
		self.enterName.setFont(fontSizeSmall);
		self.controlBar.add(self.enterName, 5, 30 );
		self.enterName.setSize(162, inputLineHeight);

		self.invite = DefaultButton(" Add");
		self.invite.setFont(fontSizeSmall);
		self.controlBar.add(self.invite);
		self.invite.setSize(inputLineHeight, inputLineHeight);
		self.invite.setPosition(self.getWidth() - self.invite.getWidth() - 12, self.enterName.getY());
		self.invite.addActionListener(self);	


		self.connectingOverlay = DefaultContainer();
		self.add(self.connectingOverlay, 0, 0);
		self.connectingOverlay.setSize(self.getWidth(), self.getHeight());
		self.connectingOverlay.setBackgroundColor(glass.Color(0,0,0,200));

		self.loginOverlayLabel = DefaultLabel("");
		self.connectingOverlay.add(self.loginOverlayLabel, "center", "center");

		gblXMPPHandler.addListener(self);
	
	def setVisible(self, v):
		self.updateRoster();
		DefaultWindow.setVisible(self, v);
	

	def updateRoster(self, roster = None):

		self.widgets = {};
		self.rosterGroup.erase();

		# Do a full update of every list entry we have:
		if roster != None:
			self.contacts = roster;
		
		for group, jidList in self.contacts.items():
			groupList = self.addGroup(group);
			#groupList.erase();			

			for jid in jidList:
				status = self.handleStatus( jidList[jid] );
				row = groupList.nextRow( status, jid, " ---- ");
				row.setId(str(jid));

			groupList.adjustWidthTo(self.scroll.getWidth()-10);

	def addGroup(self, groupName):

			# Check if we already registered that group:
			#if groupName in self.contacts:
			#	return;

			jidList = DefaultTableList();

			
			jidList.addSelectionListener(self);

			jidList.setSelectionColor(transparency);
			jidList.addMouseListener(self);
			
			self.widgets[ groupName ] = jidList;
			#self.contacts[ groupName ] = {};

			# Add the group to the rosterwindow:
			self.rosterGroup.addTab(groupName, jidList);	
			return jidList;		

	def updateControlBar(self):
		if self.activeList == "Friends":
			self.deleteOverlay.setVisible(False);
			#self.statsOverlay.setVisible(False);
		else:
			self.deleteOverlay.setVisible(True);
			#self.statsOverlay.setVisible(True);

		name = self.getSelection();
		if self.contacts[self.activeList][name] != "Offline" or Client_GetStateString("svr_name") == "Awaiting State Strings..." or cvar_get("server_address") == "":
			self.matchOverlay.setVisible(False);
		else:
			self.matchOverlay.setVisible(True);

	def getSelection(self, i=1):
		jidList = self.widgets[self.activeList];
		return jidList.getItem( jidList.getSelected(), i);

	def handleStatus(self, status):
		if status == "Online":
			return " ^go ";
		elif status == "Away":
			return " ^yo ";
		elif status == "Offline":
			return " ^rx ";
		elif status == "Ingame":
			return " ^bo ";
		else:
			logger.debug("^rError while handling status in chat.py");
			return " ^rx ";

	def onMousePress(self, e):
		pass; 
		
	def onMouseReleased(self, e):
		pass; 

	def onMouseClick(self, e):
		if self.lastClickTime + 500 >= Host_Milliseconds() and e.widget.getSelected() == self.lastClickSelect:
			name = e.widget.getRowId(e.widget.getSelected());
			# I'm going to use the gblEventHandler for that here too, could do it callback stlye tho
			gblXMPPHandler.chatEvent("chat_create", name, "");
		self.lastClickTime = Host_Milliseconds();
		self.lastClickSelect = e.widget.getSelected();

	def onAction(self, e):
		if e.widget.getCaption() == " Add":
			user = self.enterName.getText();
			gblXMPPHandler.chatEvent("chat_subscribe", "", user);

		elif e.widget.getCaption() == " + ": # TODO!!!
			self.setHeight(self.getHeight() + self.diff);
			self.diff = -self.diff;

		elif e.widget.getCaption() == "delete":
			name = self.getSelection();

			#task = thread.Thread(gblXMPPHandler.handleSubscripton,(name, 'unsubscribe'), {})

		elif e.widget.getCaption() == "stats":
			#TODO: we need an ingame stats window!
				mainmenu.showModule('stats');
				# todo!
		elif e.widget.getCaption() == "match":
			if cvar_get("server_address") == "" or Client_GetStateString("svr_name") == "Awaiting State Strings...":
				gblXMPPHandler.chatNotification("notify_error", "Match Invite Error", "You're currently not on a server.");
				return;

			name = self.getSelection();
			svrName = Client_GetStateString("svr_name");
			svr = cvar_get("server_address") + ":" + cvar_get("server_port");

			msg = "Hello " + name + ", play with me on " + svrName;

			if self.contacts[self.activeList][name] == "Ingame":
				#gblXMPPHandler.chatEvent("notify_match_invite", cvar_get('username'), name); todo
				gblXMPPHandler.chatEvent("chat_match_invite", name + '@savagerebirth.com/savage', msg, svr);
			else:
				gblXMPPHandler.chatEvent("chat_send_msg", name, "Hello " + name + ", come and play a nice Savage: Rebirth match with me!");
			
			
			#thread.Thread(gblXMPPHandler.sendInvite,(name + '@savagerebirth.com/savage', svrName), {})

	def onValueChanged(self, e):		
		for group, jidList in self.widgets.items():
			jidList.setSelectionColor(transparency);
			if jidList == e.widget:
				e.widget.setSelectionColor(glass.Color(20,0,0,128));
				self.activeList = group;
		self.updateControlBar();
		

	def onChatEvent(self, e):
		if e.scope == "chat_establish":
			self.connectingOverlay.setVisible(True);
			self.loginOverlayLabel.setCaption("^icon loading/loading0000^Logging in...");
			self.connectingOverlay.setSize(self.getWidth(), self.getHeight());
			self.loginOverlayLabel.setX(self.getWidth() // 2 - self.loginOverlayLabel.getWidth() // 2);

		elif e.scope == "chat_connect":
			self.connectingOverlay.setVisible(False);
			self.connectingOverlay.setSize(0,0); # Don't want it to block mouse stuff!

		elif e.scope == "chat_quit":
			self.connectingOverlay.setVisible(True);
			self.loginOverlayLabel.setCaption("Disconnected \nfrom chat service.");
			self.connectingOverlay.setSize(self.getWidth(), self.getHeight());
			self.loginOverlayLabel.setPosition(self.getWidth() // 2 - self.loginOverlayLabel.getWidth() // 2, self.getHeight() // 2 - self.loginOverlayLabel.getHeight() // 2);

		elif e.scope == "roster_update":
			self.updateRoster(e.string); # bad naming here, but screw it.

		elif e.scope == "chat_logged_out":
			self.updateRoster({});

			self.loginOverlayLabel.setCaption("Logged out\nfrom chat service.");
			self.connectingOverlay.setSize(self.getWidth(), self.getHeight());
			self.loginOverlayLabel.setPosition(self.getWidth() // 2 - self.loginOverlayLabel.getWidth() // 2, self.getHeight() // 2 - self.loginOverlayLabel.getHeight() // 2);

		if e.scope =="chat_contact_update":	
			for group in self.contacts:
				if e.fromstr in self.contacts[group]:
					self.contacts[group][e.fromstr] = e.string;
					for row in self.widgets[group].rows:
						if row.getId() == e.fromstr:
							row.getColumn(0).getContent(glass.GlassLabel).setCaption(self.handleStatus(e.string));
			#if self.isVisible():
			#	self.updateRoster();

class JabberChatBox(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);

		self.mucParticipants = {};
		self.currentRoom = "help";

		self.lastClickTime = 0;
		self.lastClickSelect = -1;		

		# muc stuff:

		self.left = DefaultWindow();
		self.left.setFrameStyle("TrimmedEight");
		self.add(self.left, 0, 50);
		self.left.setSize(155, 300);
		self.left.setBackgroundColor(windowBackground);

		self.list = DefaultTableList();
		self.list.setSelectionColor(transparency);
		self.list.addMouseListener(self);

		self.scroll = glass.GlassScrollArea(self.list);
		self.scroll.setBackgroundColor(transparency);
		self.scroll.setHorizontalScrollPolicy(glass.GlassScrollArea.SHOW_NEVER);
		self.left.add(self.scroll);
		self.scroll.setPosition(5, 5);
		self.scroll.setSize(self.left.getWidth() - 19, self.left.getHeight() - 40);

		self.enterName = DefaultTextBox();
		self.enterName.setFont(fontSizeSmall);
		self.left.add(self.enterName);
		self.enterName.setSize(120, inputLineHeight);
		self.enterName.setPosition(5, self.left.getHeight() - inputLineHeight - 8);

		self.invite = DefaultButton(" + ");
		self.invite.setFont(fontSizeSmall);
		self.left.add(self.invite);
		self.invite.setSize(inputLineHeight, inputLineHeight);
		self.invite.setPosition(self.left.getWidth() - self.invite.getWidth() - 12, self.enterName.getY());
		self.invite.addActionListener(self);

		# Window part:
		self.window = DefaultWindow();
		self.window.setFrameStyle("TrimmedEight");
		self.window.setBackgroundColor(windowBackground);

		self.setSize(650, 400);
		self.window.setSize(450, 400);
		self.add(self.window, 145, 0);

		top = DefaultContainer();
		self.window.add(top, 0, 0);
		top.setSize(self.window.getWidth(), 35);
		top.setBackgroundColor(windowTop);

		title = DefaultLabel("Chatbox");
		title.setForegroundColor(tangoYellowDark);
		title.setFont(fontSizeLarge);
		top.add(title, "center", "center");

		# Alright, TabbedArea is being a dick when it comes to sizes, have to pass them to __init__:
		self.chatBox = TabbedChatBox(self.window.getWidth(), self.window.getHeight() - top.getHeight());
		self.chatBox.setVisible(True);
		self.window.add(self.chatBox, 0, top.getHeight() );
		self.chatBox.resize();
		self.chatBox.addSelectionListener(self);		

		gblXMPPHandler.addListener(self);

	def updateList(self):
		self.list.erase();
		if self.currentRoom in self.mucParticipants:
			for user in self.mucParticipants[self.currentRoom]:
				self.list.nextRow(user);
		self.list.adjustWidthTo(self.scroll.getWidth() - 5);

	def logout(self):		
		# No clue if that's good code...probably not.
		#self.chatBox.setSelectedTab(0); # Select the "System" tab.
		self.chatBox.setSelectedTab(0);
		"""
		tabs = self.chatBox.chatTabs.copy();
		for tabName in tabs:
			if tabName != "System":			
				self.chatBox.deleteTab(tabName);
		"""

	def onMousePress(self, e):
		pass; 
		
	def onMouseReleased(self, e):
		pass; 

	def onMouseClick(self, e):
		if self.lastClickTime + 500 >= Host_Milliseconds() and e.widget.getSelected() == self.lastClickSelect:
			name = e.widget.getRowId(e.widget.getSelected());
			# I'm going to use the gblEventHandler for that here too, could do it callback stlye tho
			gblXMPPHandler.chatEvent("chat_create", name, "");
		self.lastClickTime = Host_Milliseconds();
		self.lastClickSelect = e.widget.getSelected();

	def onAction(self, e):
		if e.widget.getCaption() == " + ":
			name = self.enterName.getText();
			self.enterName.setText("");			

			gblXMPPHandler.chatEvent("muc_invite_sent", cvar_get('username'), name, self.currentRoom);

	def onValueChanged(self, e):
		box = e.widget
		if box == self.chatBox:
			tab = box.getSelectedTab()
			if box.chatTabs[tab].chatBox.isConference:
				self.left.setVisible(True);
			else:
				self.left.setVisible(False);

	def onChatEvent(self, e):
		if e.scope == "chat_create" or e.scope == "chat_msg" or e.scope == "chat_history_update":
			if e.fromstr not in self.chatBox.chatTabs and e.fromstr != "":
				self.chatBox.openConversation(e.fromstr);

		elif e.scope == "muc_msg" or e.scope == "muc_presence":
			if e.room not in self.chatBox.chatTabs and e.room != "":
				self.chatBox.openConversation(e.room, conference=True);		

		elif e.scope == "muc_subject":
			if e.room in self.chatBox.chatTabs:
				self.chatBox.chatTabs[e.room].contactStatus.setCaption(e.string);

		elif e.scope == "chat_contact_update":
			if e.fromstr in self.chatBox.chatTabs:
				self.chatBox.chatTabs[e.fromstr].contactStatus.setCaption(e.string);

		elif e.scope == "chat_logged_out":
			self.logout();

		if e.scope == "muc_presence" or e.scope == "muc_roster_update":			
			if e.room not in self.mucParticipants and e.room != "":
				self.mucParticipants[e.room] = [e.fromstr];
			elif e.string == "available" and e.fromstr not in self.mucParticipants[e.room]:
				self.mucParticipants[e.room].append(e.fromstr);
			elif e.string == "unavailable" and e.fromstr in self.mucParticipants[e.room]:
				self.mucParticipants[e.room].remove(e.fromstr);
			self.updateList();


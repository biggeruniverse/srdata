
from silverback import *;
import glass;
from ringbuffer import RingBuffer;

class ChatBox( glass.GlassContainer ):
	def __init__(self, scopeList):
		self.scopeList = scopeList;
		glass.GlassContainer.__init__(self);
		self.setOpaque(False);
	
		self.buffer = MessageBuffer( self.scopeList );
		for i in range(10):
			self.buffer.addRow(" ");
		self.buffer.setEditable(False);
		self.buffer.showTime(True);
		self.buffer.addListener(self)

		self.scroll = glass.GlassScrollArea(self.buffer);
		self.scroll.setScrollPolicy( glass.GlassScrollArea.SHOW_NEVER , glass.GlassScrollArea.SHOW_ALWAYS  );
		self.scroll.setAutoscroll(True);
		self.add(self.scroll);
		self.buffer.parentScroll = self.scroll;
		
		self.input = glass.GlassTextField();
		self.input.setForegroundColor( white );
		self.input.setBackgroundColor( glass.Color(0,0,0,128) );
		self.add( self.input);
		self.input.addKeyListener( self);
		
		self.bShowInput = False;
		
	
	def onKeyPress(self, e):
		if e.key == glass.Key.ESCAPE: #escape
			self.deactivate();
	
	def onKeyReleased(self, e):
		if e.key == glass.Key.ENTER:
			content = self.input.getText().rstrip();
			if content == "":
				self.deactivate();
				return;
			self.buffer.addRow(content);
	
	def alwaysShowInput( self, x ):
		if x == 1:
			x=True
		if x == True:
			self.input.setVisible(True);
		self.bShowInput = x;
		
	def resize( self ):
		self.scroll.setSize( self.getWidth() , int(self.getHeight() - 0.4*inputLineHeight) );
		self.buffer.setSize( self.scroll.getWidth(), self.scroll.getHeight() );
		self.input.setSize(self.getWidth(), inputLineHeight);
		self.input.setPosition(0, self.getHeight() - inputLineHeight );
		
	def deactivate( self ):
		self.input.setText("");
		if not self.bShowInput:
			self.input.setVisible(False); #this also REMOVES the focus
	
	def activate( self ):
		self.input.setText("");
		self.input.setVisible(True);
		self.input.requestFocus();

class MenuChatBox(ChatBox):
	def __init__(self, name, scopeList, isConference=False):		
		glass.GlassContainer.__init__(self);

		self.setOpaque(False);
		self.jid = name;
		self.isConference = isConference;
		self.scopeList = scopeList;
	
		self.buffer = MessageBuffer( self.scopeList );
		self.buffer.setEditable(False);
		self.buffer.showTime(True);

		self.scroll = glass.GlassScrollArea(self.buffer);
		self.scroll.setScrollPolicy( glass.GlassScrollArea.SHOW_NEVER , glass.GlassScrollArea.SHOW_ALWAYS  );
		self.scroll.setAutoscroll(False);
		self.add(self.scroll);
		self.buffer.parentScroll = self.scroll;

		# extending the input box to make it look a bit better:

		self.inputContainer = DefaultContainer();
		self.inputContainer.setBackgroundColor(glass.Color(23,14,13));
		self.add(self.inputContainer);

		self.div = DefaultContainer();
		self.div.setBackgroundColor(glass.Color(30,26,25));
		self.inputContainer.add(self.div);
		
		self.input = glass.GlassTextField();
		self.input.setForegroundColor( white );
		self.input.setBackgroundColor( glass.Color(0,0,0,128) );
		self.inputContainer.add( self.input);
		self.input.addKeyListener( self);
		
		self.bShowInput = False;

		gblXMPPHandler.addListener(self);	

	def resize( self ):
		self.inputContainer.setSize(self.getWidth(), 2 * inputLineHeight);
		self.inputContainer.setPosition(0, self.getHeight() - self.inputContainer.getHeight())

		self.div.setSize(self.inputContainer.getWidth(), 1);
		self.div.setPosition(0, 0);

		self.scroll.setSize( self.getWidth() - 5 , self.getHeight() - self.inputContainer.getHeight() );
		self.buffer.setSize( self.scroll.getWidth() - 10, self.scroll.getHeight() );

		self.input.setSize(self.inputContainer.getWidth() - 25, inputLineHeight);
		self.input.setPosition(8, self.inputContainer.getHeight() - int(1.5*inputLineHeight) );

	def onKeyReleased(self, e):
		if e.key == glass.Key.ENTER:
			content = self.input.getText().rstrip();
			if content == "":
				self.deactivate();
				return;
			#self.buffer.addRow(content);
			self.input.setText("");
			#self.scroll.setVerticalScrollAmount(99999999);  #Since autoscroll is somehow broken, this makes sure it scrolls automatically to the bottom.
			if self.isConference:
				gblXMPPHandler.chatEvent("muc_send_msg", cvar_get('username'), content, room=self.jid);	
			else:
				gblXMPPHandler.chatEvent("chat_send_msg", self.jid, content);

	# messagebuffer is still an gblEventHandler-Listener and no XMPP one, so I have to 
	# pass fake events. kind of hacky, but better than changing the whole messagebuffer.
	def onChatEvent(self, e):
		# check if the chat_event got delivered to the right place:
		#if e.scope == "chat_msg" or e.scope == "chat_send_msg" or e.scope == "chat_create":

		if self.isConference:
			if e.scope.startswith("muc_"):
				if str(e.room) != self.jid:
					return;
				else:
					self.buffer.onEvent(e);
					self.scroll.setVerticalScrollAmount(99999999);
		else:
			if str(e.fromstr) != self.jid:
				return;		
			elif e.scope.startswith("chat_"):			
				# pass the event to the messagebuffer:
				self.buffer.onEvent(e);
				self.scroll.setVerticalScrollAmount(99999999);

class ConversationTab(DefaultContainer):
	def __init__(self, jid, isConference=False):
		DefaultContainer.__init__(self);

		self.jid = jid

		#self.setBackgroundColor(tangoGrey5);

		# A conversation tab consists of:
		
		# 1. profile pic:
		self.setVisible(True);
		self.picContainer = DefaultContainer();
		self.picContainer.setBackgroundColor(tangoOrangeDark);
		self.add(self.picContainer);

		self.pic = DefaultImage();
		self.pic.setImage("nopic.png");
		self.picContainer.add(self.pic, 2, 2);

		# 2. The name and status of the contact
		self.contactName = DefaultLabel(self.jid);		
		self.add(self.contactName);
		self.contactStatus = DefaultLabel(""); #TODO
		self.contactStatus.setForegroundColor(tangoGreen);
		self.add(self.contactStatus);		

		# 3. various option buttons, e.g. Invite to game, Invite to chat, View Stats...
		# TODO

		# 3.1: Conference stuff:
		if isConference:

			self.pic.setImage("icons/clans.png")
			self.contactName.setCaption(self.jid + " conference");
			self.contactStatus.setForegroundColor(tangoOrange);


		# 4. The chatbox itself:
		self.div = DefaultContainer();
		self.div.setBackgroundColor(glass.Color(30,26,25));
		self.add(self.div);

		self.chatboxContainer = DefaultContainer();
		self.chatboxContainer.setBackgroundColor(glass.Color(23,14,13));
		self.div.add(self.chatboxContainer, 1, 1)

		scopes = ["chat_msg", "chat_send_msg", "chat_join","chat_connect", "chat_history_update",
		    "muc_msg", "muc_presence", "chat_quit", "chat_disconnect"] if self.jid != "System" else ["chat_join","chat_connect",
		    "chat_history_update", "chat_establish", "chat_quit", "chat_disconnect"];

		self.chatBox = MenuChatBox(self.jid, scopes, isConference);
		self.chatBox.alwaysShowInput(True);
		self.chatboxContainer.add(self.chatBox);

		#self.oldBufferEvent = self.chatBox.buffer.onEvent;
		#self.chatBox.buffer.onEvent = self.bufferEvent;

		if self.jid == "System":
			self.chatBox.alwaysShowInput(False);
			self.chatBox.input.setVisible(False);
			self.pic.setImage("/icons/options.png");
			self.contactStatus.setCaption("");

	def resize(self):

		# I love that part.... :|
		# Place the picture at the top left, next to it username and status
		w = self.getWidth();
		h = self.getHeight();
		
		self.picContainer.setPosition(10, 10); # fixed position, if we're going to support resizing one day...
		self.picContainer.setSize(40, 40);
		self.pic.setSize(self.picContainer.getWidth() - 4, self.picContainer.getHeight() - 4);

		self.contactName.setPosition(self.picContainer.getWidth() + 20, self.picContainer.getY() - 2);
		self.contactStatus.setPosition(self.contactName.getX(), self.contactName.getHeight() + 12);

		self.div.setPosition(10, self.picContainer.getHeight() + 20);
		self.div.setSize( w - 25, h - self.div.getY() - 10);
		self.chatboxContainer.setSize( self.div.getWidth() - 2, self.div.getHeight() - 2);
		self.chatBox.setSize(self.chatboxContainer.getWidth(), self.chatboxContainer.getHeight());

		# Most important line:
		self.chatBox.resize();
		
		
class TabbedChatBox(glass.GlassTabbedArea):
	def __init__(self, w, h):
		glass.GlassTabbedArea.__init__(self);	

		self.currentTab = None;	

		self.chatTabs = {};		
		self.setSize(w, h);

		self.openConversation("System");		
		#self.setBackgroundColor(white);

	def openConversation(self, jid, conference=False):
		# 1. Create a new tab that contains all the information
		tab = ConversationTab(jid, isConference=conference);
		tab.setSize(self.getWidth(), self.getHeight());
		tab.setSize(self.getWidth(), self.getHeight() - 50);
		tab.resize();
		self.chatTabs[tab.jid] = tab;
		self.addTab(tab.jid, tab);		
		self.setSelectedTab(len(self.chatTabs) - 1);
		#tab.chatBox.activate();

	def joinMUC(self, room, password=False):
		pass;

	def deleteTab(self, jid):
		"""
		self.setSelectedTab(0)
		if jid not in self.chatTabs:
			logger.error("Trying to delete a tab that doesn't exist.");
		else:
			self.removeTab(self.chatTabs.pop(jid));
		"""
		pass; #buggy						

	def resize(self):
		pass;

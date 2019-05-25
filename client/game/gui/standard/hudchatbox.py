# (c) 2010 savagerebirth.com
# a class to handle the chat input box
from silverback import *;
import glass;
import hudchatcommands;
from ringbuffer import RingBuffer;

class ChatBox( glass.GlassContainer ):
	def __init__(self, scopeList):
		self.scopeList = scopeList;
		glass.GlassContainer.__init__(self);
		self.setOpaque(0);
		
		self.buffer = MessageBuffer( self.scopeList );
		for i in range(10):
			self.buffer.addRow(" ");
		self.buffer.setEditable(0);
		self.buffer.showTime(1);
			
		self.scroll = glass.GlassScrollArea(self.buffer);
		self.scroll.setScrollPolicy( glass.GlassScrollArea.SHOW_NEVER , glass.GlassScrollArea.SHOW_ALWAYS  );
		self.scroll.setAutoscroll(1);
		self.add(self.scroll);
		self.buffer.parentScroll = self.scroll;
		
		self.input = glass.GlassTextField();
		self.input.setForegroundColor( white );
		self.input.setBackgroundColor( glass.Color(0,0,0,128) );
		self.add( self.input);
		self.input.addKeyListener( self);
		
		self.bShowInput = 0;
		
	
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
			self.input.setVisible(1);
		self.bShowInput = x;
		
	def resize( self ):
		self.scroll.setSize( self.getWidth() , int(self.getHeight() - 0.4*inputLineHeight) );
		self.buffer.setSize( self.scroll.getWidth() , self.scroll.getHeight() );
		self.input.setSize(self.getWidth() , inputLineHeight);
		self.input.setPosition(0, self.getHeight() - inputLineHeight );
		
	def deactivate( self ):
		self.input.setText("");
		if self.bShowInput == 0:
			self.input.setVisible(0); #this also REMOVES the focus
	
	def activate( self ):
		self.input.setText("");
		self.input.setVisible(1);
		self.input.requestFocus();

class HUDChatBox( ChatBox, EventListener ):
	HISTORY_ON = 1
	HISTORY_OFF = 0
	def __init__( self ):
		ChatBox.__init__(self, ["msg_public", "msg_team", "msg_private", "msg_squad", "msg_clan", "_HCBinternal"]);
		self.buffer.showTime(1);
		self.buffer.setFadeTop(1);
		
		self.scroll.setVerticalScrollPolicy( glass.GlassScrollArea.SHOW_NEVER );
		
		self.input.setVisible(0);
		
		self.inputType = glass.GlassLabel("(squad)");
		self.inputType.setAlignment( glass.Graphics.RIGHT );
		self.add(self.inputType)
		
		self.history = RingBuffer(16);
		self.historyIndex = 0;
		self.chatType = "all";
		self.replyTarget = "";
		self.oldHeight = 0;
		
		self._historyShown = 0;
		self.showHistory(0);
		
	def onEvent (self, e):
		if e.scope == "msg_private":
			self.replyTarget = e.fromstr;
	
	def onKeyPress( self, e):
		if e.key == glass.Key.ESCAPE:
			self.deactivate();
		
		elif e.key == glass.Key.UP:
			histdata = self.history.get();
			if len(histdata) == 0: return;
			self.historyIndex = (self.historyIndex - 1) % len(histdata);
			self.input.setText( histdata[self.historyIndex] );
			self.input.setCaretPosition( len( self.input.getText() ) );
		elif e.key == glass.Key.DOWN:
			histdata = self.history.get();
			if len(histdata) == 0: return;
			self.input.setText( histdata[self.historyIndex] );
			self.input.setCaretPosition( len( self.input.getText() ) );
			self.historyIndex = (self.historyIndex + 1) % len(histdata);
		elif e.key == glass.Key.TAB:
			return;
			"""
			#tab complete
			#1. from the current position, move backwards until you find a space, or the start of the input text
			#2. call the string between the space/start and the current position STRING
			#3. create an empty list LIST
			#3. loop over each player
				#a. see if their name .startsWith STRING
					#i. if it does, append this name to LIST
			#4. if LIST is empty, don't do anything, just make sure a tab character isn't added
			#5. sort the elements of LIST alphabetically
			#6. replace the name in the input field

			# cache the startswith STRING to save searching through each player
			# cache the index of the filtered names so you can cycle through them
			"""
	
	def onKeyReleased(self, e):
		if e.key == glass.Key.ENTER:
			content = self.input.getText().rstrip();
			if content == "":
				self.deactivate();
				return;
			
			sh = self.history.get();
			if len(sh)==0 or (len(sh) != 0 and sh[-1] != content):
				self.history.append( content );
			
			if content.startswith("/") and not content.startswith("//"):
				#use one / for chat commands
				data = content.split();
				cmdname = data[0][1:];
				if hasattr( hudchatcommands, cmdname ):
					args = data[1:];
					try:
						cmdreturn = getattr( hudchatcommands, cmdname )( self, args);
					except Exception, ex:
						con_println("^rError: User tried to exec ^w/"+cmdname+" "+" ".join(args)+"\n");
						con_println("^rException: "+str(ex)+"\n");
						self.deactivate();
						return;
					if cmdreturn != None:
						cmdreturn = str(cmdreturn);
						gblEventHandler.notifyEvent( "_HCBinternal", "", cmdreturn );
					self.deactivate();
					return
			if content.startswith("/"):
				#// will directly execute python.
				#/ will execute python as long as no matching command is found.
				content = content.lstrip("/")
				try:
					exec content;
				except Exception, ex:
					con_println("^rError: User tried to exec ^w"+content+"\n");
					con_println("^rException: "+str(ex)+"\n");
				finally:
					self.deactivate();
					return;
			
			#if we haven't returned yet, then we're just chatting!
			content = content.replace('\\', '\\\\');
			content = content.replace('"', '\\"');
			
			CL_SendChat( content, self.chatType );
			if self.chatType == "comm":
				gblEventHandler.notifyEvent( "_HCBinternal","",commColorCode + "-> Comm " + content);
			Sound_PlaySound("/sound/gui/msg_send.ogg");
			self.deactivate();
	
	def onMouseWheelMovedUp( self, e):
		if self._historyShown:
			self.scroll.mouseWheelMovedUp();
			#is this even the right method to call?
	
	def onMouseWheelMovedDown( self, e):
		if self._historyShown:
			self.scroll.mouseWheelMovedDown();
	
	def activate( self, chatType = "all"):
		self.chatType = chatType; #"all" "team" "comm" "squad" "private" "clan"
		#don't use "private" here, use /w, /msg, /r and /re for that
		self.input.setText("");
		self.input.setVisible(1);
		self.input.requestFocus();
		
		self.inputType.setCaption( "^777(" + chatType +")" );
		self.inputType.setPosition(0, self.input.getY() + (self.input.getHeight() - self.inputType.getHeight())//2)
		self.input.setX( self.inputType.getWidth() + 2 );
		self.input.setWidth( self.getWidth() - self.inputType.getWidth() );

	def deactivate( self ):
		self.inputType.setCaption("");
		self.historyIndex = 0;
		self.input.setText("");
		if self.bShowInput == 0:
			self.input.setVisible(0); #this also REMOVES the focus

	def showHistory( self, status):
		if self._historyShown != status:
			if status == self.HISTORY_ON:
				self.scroll.setVerticalScrollPolicy( glass.GlassScrollArea.SHOW_ALWAYS );
				self.scroll.setAutoscroll(0);
				self.buffer.setFadeTop(0);
				self.oldHeight = self.getHeight();
				self.setHeight(self.oldHeight+300);
				self.setY(self.getY()-300);
				self.resize();
			else:
				self.scroll.setVerticalScrollPolicy( glass.GlassScrollArea.SHOW_NEVER );
				self.scroll.setAutoscroll(1);
				self.buffer.setFadeTop(1);
				self.setHeight(self.oldHeight);
				self.setY(self.getY()+300);
				self.resize();
		self._historyShown = status;

class IRCChatBox(ChatBox):
	def __init__(self):
		ChatBox.__init__(self, ["irc_msg","irc_join","irc_connect","irc_quit"]);
	
	def onKeyReleased(self, e):
		if e.key == glass.Key.ENTER:
			content = self.input.getText().rstrip();
			if content == "":
				self.deactivate();
				return;
				
			gblEventHandler.notifyEvent("irc_send_msg",gblIRCHandler.NICKNAME,content);
			gblEventHandler.notifyEvent("irc_msg",gblIRCHandler.NICKNAME,content);
			self.deactivate();
			return;

	def deactivate(self):
		self.input.setText("");

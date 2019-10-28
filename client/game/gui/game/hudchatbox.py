# (c) 2010 savagerebirth.com
# a class to handle the chat input box
from silverback import *;
import glass;
import hudchatcommands;
from ringbuffer import RingBuffer;


class HUDChatBox( ChatBox, EventListener ):
	HISTORY_ON = 1
	HISTORY_OFF = 0
	def __init__( self ):
		ChatBox.__init__(self, ["msg_public", "msg_team", "msg_private", "msg_squad", "msg_clan", "msg_server", "_HCBinternal"]);
		self.buffer.setFadeTop(True);

		#history messages
		self.historyBuffer = MessageBuffer(["msg_public", "msg_team", "msg_private", "msg_squad", "msg_clan", "msg_server", "_HCBinternal"]);
		self.historyBuffer.setEditable(False);
		scroll = glass.GlassScrollArea(self.historyBuffer);
		scroll.setScrollPolicy( glass.GlassScrollArea.SHOW_NEVER , glass.GlassScrollArea.SHOW_ALWAYS  );
		scroll.setAutoscroll(True);
		self.add(scroll);
		self.historyBuffer.parentScroll = scroll;
		scroll.setVisible(False);
		for i in range(40):
			self.historyBuffer.addRow(" ");
		
		self.scroll.setVerticalScrollPolicy( glass.GlassScrollArea.SHOW_NEVER );
		
		self.input.setVisible(False);
		
		self.inputType = glass.GlassLabel("(squad)");
		self.inputType.setAlignment( glass.Graphics.RIGHT );
		self.add(self.inputType)
		
		self.history = RingBuffer(16);
		self.historyIndex = 0;
		self.chatType = "all";
		self.replyTarget = "";
		self.oldHeight = 0;
		self.typing = False;
		
		self.fade = ActionSequence(savage.WaitAction(5000), savage.CheckAction(self.typing, False), FadeOutAction(self))
		self.showHistory(False);


	def resize( self ):
		self.scroll.setSize( self.getWidth() , int(self.getHeight()*0.5 - 0.4*inputLineHeight) );
		self.buffer.setSize( self.scroll.getWidth() , self.scroll.getHeight() );
		self.historyBuffer.parentScroll.setSize( self.getWidth() , int(self.getHeight() - 0.4*inputLineHeight));
		self.historyBuffer.setSize(self.historyBuffer.parentScroll.getWidth(), self.historyBuffer.parentScroll.getHeight());
		self.input.setSize(self.getWidth()-25 , inputLineHeight);
		self.scroll.setPosition(0, int(self.getHeight()*0.5));
		self.input.setPosition(0, self.getHeight() - inputLineHeight );

	def makeVisible(self, forever=False):
		self.fade.stop()
		self.setAlpha(255)
		self.setVisible(True)
		if not forever and not self.typing:
			self.fade = ActionSequence(savage.WaitAction(5000), savage.CheckAction(self.typing, False), FadeOutAction(self))
		
	def onEvent (self, e):
		self.makeVisible()
		if e.scope == "msg_private":
			self.replyTarget = e.fromstr;
	
	def onKeyPress( self, e):
		self.typing = True;
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
		if e.key == glass.Key.ENTER or e.key==10: #e.key == glass.Key.RETURN #Big: hacky fix because I forgot where the defines are...
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
					except Exception as ex:
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
					exec(content)
				except Exception as ex:
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
			self.historyBuffer.parentScroll.mouseWheelMovedUp();
			#is this even the right method to call?
	
	def onMouseWheelMovedDown( self, e):
		if self._historyShown:
			self.historyBuffer.parentScroll.mouseWheelMovedDown();
	
	def activate( self, chatType = "all"):
		self.typing = True
		self.makeVisible(True)
		self.chatType = chatType; #"all" "team" "comm" "squad" "private" "clan"
		#don't use "private" here, use /w, /msg, /r and /re for that
		self.input.setText("");
		self.input.setVisible(True);
		self.input.requestFocus();
		
		self.inputType.setCaption( "^777(" + chatType +")" );
		self.inputType.setPosition(0, self.input.getY() + (self.input.getHeight() - self.inputType.getHeight())//2)
		self.input.setX( self.inputType.getWidth() + 2 );
		self.input.setWidth( self.getWidth() - self.inputType.getWidth() );

	def deactivate( self ):
		self.makeVisible()
		self.inputType.setCaption("");
		self.historyIndex = 0;
		self.input.setText("");
		self.typing = False;
		if self.bShowInput == 0:
			self.input.setVisible(False); #this also REMOVES the focus

	def showHistory( self, status):
		vis = 0;
		if self.historyBuffer.parentScroll.isVisible():
			vis = 1;
		if vis != status:
			if status == self.HISTORY_ON:
				self.makeVisible(True)
				self.buffer.setVisible(False);
				self.historyBuffer.parentScroll.setVisible(True);
				self.historyBuffer.parentScroll.requestFocus();
			else:
				self.makeVisible()
				self.buffer.setVisible(True);
				self.historyBuffer.parentScroll.setVisible(False);

class CommChatBox( HUDChatBox ):
	def __init__(self):
		HUDChatBox.__init__(self);
		self.inputType.setCaption("");



# (c) 2010 savagerebirth.com
# a subclass that holds all the voice chat gui pieces

from silverback import *;
import glass;
import voicechatdata;

class VoiceChatBox( DefaultWindow ):
	def __init__( self ) :
		DefaultWindow.__init__( self );
		self.setBackgroundColor(glass.Color(0,0,0,128));
		self.setVisible(0);
		self.addKeyListener(self);
		self.setTitleBarHeight(0);
		self.setTitleVisible(0);
		
		self.table = DefaultTable();
		self.table.makeBlank();
		self.table.horizontalJustification = glass.Graphics.LEFT;
		self.table.autoAdjust = False;
		self.table.stretchWidgets = True;
		self.add( self.table );
		
		for i in range( 10 ):
			self.table.addRow(" ");
		
		self.status = self.INACTIVE;
		self.categoryNumber = -1;
		self.currentVoiceDict = "";
	
	def updateTable( self, nameList ):
		nameCount = len( nameList );
		for i in range( nameCount ):
			name = nameList[ i ];
			w = self.table.getWidget(i, 0, glass.GlassLabel);
			caption = str( ( i + 1) % 10) + ". " +name;
			w.setCaption( caption );
		
		#now make any remaining labels empty
		for i in range(i + 1, 10):
			w = self.table.getWidget(i, 0, glass.GlassLabel);
			w.setCaption(" ");
	
	def newVoiceChat( self ):
		player = savage.getLocalPlayer();
		if player.getTeam() == 0:
			self.currentVoiceDict = voicechatdata.human_player_male;
		else:
			team = savage.Team(player.getTeam());
			if player.isCommander():
				voiceType = "commander";
			else:
				voiceType = "player_male";
			self.currentVoiceDict = getattr( voicechatdata,team.getRace() + "_" + voiceType );
		
		self.setVisible(1);
		self.updateTable( self.currentVoiceDict.keys() );
		self.status = self.CATEGORY_LIST;
		self.requestModalFocus(); #to catch keys
		self.categoryNumber = -1;
	
	def voiceCategoryExists( self, categoryNumber ):
		try: 
			self.currentVoiceDict.values()[ (categoryNumber -1 )% 10];
		except IndexError:
			return False;
		return True;
	
	def voiceChatExists( self, messageNumber ):
		try: 
			category = self.currentVoiceDict.values()[ (self.categoryNumber -1 )% 10]
			message = category.values()[ (messageNumber -1 )% 10];
		except IndexError:
			return False;
		return True;
	
	def showVoiceCategory( self, categoryNumber ):
		self.categoryNumber = categoryNumber;
		category = self.currentVoiceDict.values()[ (self.categoryNumber -1 )% 10]; #zero-based index
		messageNameList = category.keys();
		
		self.updateTable( messageNameList );
		self.status = self.MESSAGE_LIST;
	
	
	def done( self ):
		self.releaseModalFocus();
		self.setVisible(0);
		self.status = self.INACTIVE;
		self.categoryNumber = -1;
	
	def sendVoiceChat( self, msgNumber ):
		CL_SendVoiceChat( self.categoryNumber, (msgNumber - 1)%10 );
		self.done();
	
	def onKeyPress( self, e ):
		if e.key == 1016: #"escape"
			self.done();
		
		elif 48 <= e.key <= 57:
			keyValue = e.key - 48;
			
			if self.status == self.CATEGORY_LIST and self.voiceCategoryExists( keyValue ):
				self.showVoiceCategory( keyValue );
			
			elif self.status == self.MESSAGE_LIST and self.voiceChatExists( keyValue ):
				self.sendVoiceChat ( keyValue );

	def onKeyReleased(self, e):
		pass;
	
	INACTIVE = 0;
	CATEGORY_LIST = 1;
	MESSAGE_LIST = 2;




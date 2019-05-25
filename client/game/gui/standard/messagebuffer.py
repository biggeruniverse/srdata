# (c) 2010 savagerebirth.com
# this file defines a multiple inheritance class for the chat buffers

import glass;

class MessageBuffer(glass.GlassTextBox, EventListener):
	def __init__(self, scopes = ["msg_public", "msg_team", "msg_private", "msg_squad", "notify", "notifyhide"] ):
		glass.GlassTextBox.__init__(self);
		self.setOpaque(0);
		
		self.scopesToAccept = scopes; #this way you can set scopes when you instantiate
		self.bShowTime = 1;
		global gblEventHandler;
		gblEventHandler.addNotifyListener(self);
		
		self.parentScroll = None;
		
		self.setLineWrap(1);
		self.setForegroundColor(white);
		self.setEditable(0);
		self.setFocusable(0);
		
	
	def onEvent(self, e):
		import savage;
		if e.scope in self.scopesToAccept:
			if e.scope in ("msg_public", "msg_team", "msg_private", "msg_squad"):
				e.clanIcon = "";
				fromp = e.fromstr;
				if fromp.startswith("^clan"):
					#names cannot contain carets
					e.clanIcon = fromp.rpartition("^")[0] + "^";
					fromp = fromp.rpartition("^")[2];
				e.source = savage.getPlayerByName( fromp );
				e.sourceName = fromp;
				
				msg = self.timeStr() + self.typeStr(e) + self.senderStr(e) + self.seperator(e) + e.string;

			elif e.scope == "irc_msg":
				msg = timeColorCode + cvar_get("host_time") + " " +e.fromstr + ":^w " + e.string;
			elif e.scope in ("irc_join","irc_quit", "irc_connect"):
				msg = "^777" + cvar_get("host_time") + " "+ e.string;
			else:
				msg = e.string;
			self.addRow(msg);
			if self.parentScroll != None:
				self.parentScroll.logic();


	def timeStr(self):
		policy = cvar_getvalue("gui_chatTimestamp");
		if self.bShowTime == 0 or policy == 0:
			return "";
		elif policy == 1: #game time
			gametime = getGameTimeString(cvar_getvalue("game_timeLimitSeconds"));
			if gametime != "":
				return timeColorCode + gametime + " ";
			else:
				return "";
		elif policy == 2:#local time
			return timeColorCode + cvar_get("host_time") + " ";
	
	def typeStr( self, e):
		if e.scope == "msg_team":
			if e.source.getTeam() == 0:
				return "^w[spec]";
			else: 
				return "^w[team]";
		elif e.scope == "msg_squad":
			return "^w[squad]";
		elif e.scope == "msg_private":
			return privColorCode;
		return "";
	
	def senderStr(self, e):
		returnstr = "";
		myteam = savage.getLocalPlayer().getTeam();
		sourceteam = e.source.getTeam();
		
		#refs and comms always have the tag added to the end of their name
		
		if e.source.isCommander(): returnstr = "[C]" + returnstr;
		elif e.source.isReferee(): returnstr = "[REF]" + returnstr;
		
		returnstr = e.sourceName + returnstr;
		
		#private messages don't respect colouring
		#spectators see all names as white
		#non-specs see enemies as red
		#ally comms are green
		#any other ally is blue
		#any spec-refs are gold
		#anyone else (specs) are white
		
		if e.scope == "msg_private":
			returnstr = privColorCode + returnstr;
		elif e.source.isReferee() and e.source.getTeam() == 0:
			returnstr = refColorCode + returnstr;
		elif sourceteam == myteam and e.source.isCommander():
			returnstr = commColorCode + returnstr;
		else: returnstr = e.source.getNameColorCode() + returnstr;
		
		returnstr = "^w" + e.clanIcon + returnstr;
		
		return returnstr;
	
	def seperator(self, e):
		if e.scope == "msg_private":
			return privColorCode + ": ";
		else:
			return "^w: ";

	def showTime(self,t):
		self.bShowTime = t;

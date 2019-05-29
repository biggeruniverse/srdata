# (c) 2010 savagerebirth.com
# this file defines a multiple inheritance class for the chat buffers

import glass;

class MessageBuffer(glass.GlassTextBox, EventListener):
	def __init__(self, scopes = ["msg_public", "msg_team", "msg_private", "msg_squad", "msg_server", "notify", "notifyhide"] ):
		glass.GlassTextBox.__init__(self);
		self.setOpaque(False);
		
		self.scopesToAccept = scopes; #this way you can set scopes when you instantiate
		self.bShowTime = True;
		global gblEventHandler;
		gblEventHandler.addNotifyListener(self);
		
		self.parentScroll = None;
		
		self.setLineWrap(True);
		self.setForegroundColor(white);
		self.setEditable(False);
		self.setFocusable(False);
		self.listeners = [];
	
	def addListener(self, l):
		self.listeners.append(l);

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

				if e.source is None:
					e.source = savage.Player(-1)
				
				msg = self.timeStr() + self.typeStr(e) + self.senderStr(e) + self.seperator(e) + e.string;

			elif e.scope == "chat_msg" or e.scope == "muc_msg":
				msg = timeColorCode + e.timeStamp + " " +e.fromstr + ":^w " + e.string;
			elif e.scope == "chat_send_msg" or e.scope == "muc_send_msg":
				msg = timeColorCode + e.timeStamp + " " +cvar_get("username") + ":^w " + e.string;
			elif e.scope == "chat_history_update":
				msg = e.string # As an event has only 3 attributes, the string has to be formatted beforehand.
			elif e.scope in ("chat_join", "chat_disconnect", "chat_quit", "chat_connect", "chat_establish"):
				msg = "^777" + e.timeStamp + " "+ e.string;
			elif e.scope == "msg_server":
				msg = "^y"+e.string;
			elif e.scope == "muc_presence":
				if e.string == "available":
					status = e.fromstr + " joined " + e.room + ".";
				elif e.string == "unavailable":
					status = e.fromstr + " left " + e.room + ".";
				else:
					return;
				msg = timeColorCode + cvar_get("host_time") + " " + status;
			else:
				msg = e.string;
			self.addRow(msg);
			if self.parentScroll != None:
				self.parentScroll.logic();
			for l in self.listeners:
				l.onEvent(e)


	def timeStr(self):
		policy = cvar_getvalue("gui_chatTimestamp");
		if self.bShowTime == False or policy == 0:
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
		returnstr = ""
		myteam = 0
		sourceteam = e.source.getTeam()
		try:
			myteam=savage.getLocalPlayer().getTeam()
		except:
			pass
		#refs and comms always have the tag added to the end of their name
		
		if e.source.isCommander(): returnstr = "[C]" + returnstr
		elif e.source.isReferee(): returnstr = "[REF]" + returnstr
		
		returnstr = e.sourceName + returnstr
		
		#private messages don't respect colouring
		#spectators see all names as white
		#non-specs see enemies as red
		#ally comms are green
		#any other ally is blue
		#any spec-refs are gold
		#anyone else (specs) are white
		
		if e.scope == "msg_private":
			returnstr = privColorCode + returnstr
		elif e.source.isReferee() and e.source.getTeam() == 0:
			returnstr = refColorCode + returnstr
		elif sourceteam == myteam and e.source.isCommander():
			returnstr = commColorCode + returnstr
		else: returnstr = e.source.getNameColorCode() + returnstr
		
		returnstr = "^w" + e.clanIcon + returnstr
		
		return returnstr
	
	def seperator(self, e):
		if e.scope == "msg_private":
			return privColorCode + ": "
		else:
			return "^w: "

	def showTime(self,t):
		self.bShowTime = t

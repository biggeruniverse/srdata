# copyright (c) 2011 savagerebirth.com
# this file handles the irc-handling mechanism

from silverback import *; #for IRC_SendMessage();
import re;

class IRCMessage():
	MESSAGE_PATTERN = re.compile(r"""
	(
		:(?P<prefix>[^ ]+)\ +
	)?
	(?P<command>[^ ]+)
	(?P<paramstr>[^\r\n]+)
	\r?\n
	""", re.VERBOSE);
	
	PREFIX_PATTERN = re.compile(r"""
	(?P<source>[^!@]+)
	(!(?P<user>[^!@]+))?
	(@(?P<host>[^!@]+))?
	""",re.VERBOSE);
	
	PARAM_MIDDLE_PATTERN = re.compile(r"""
	\ ([^ ]+)
	""",re.VERBOSE);

	PARAM_TRAILING_PATTERN = re.compile(r"""
	\ :(?P<trailing>.*)
	""",re.VERBOSE);
	
	"""
	if the message starts with a colon, everything after the colon and before the first space is <prefix> and <command> starts after the last space.
	if the message does not start with a colon, the start of the message is <command>
	<command> consists of alphanumeric characters only, and must be followed by a space.
	after this space comes zero or more <params>
	finally the message ends in CRLF (although some networks only use LF, just use rstrip()
	
	<prefix> must contain a <source>, which is either the <servername> or the <nickname>. If <source> represents a nickname, it may optionally be followed by either "!"<user> or "@"<host> or both (although !user comes before @host, always.

	<params> is a list of either <trailing> or <middle> strings.
	<trailing> strings may be empty. <trailing> strings are preceeded by a colon. <trailing> may not include CR, LF, or NUL.
	<middle> strings must be non-empty. <middle> strings may not include a space, CR, LF, or NUL.
	the last parameter must always be <trailing>. there may only be one <trailing> parameter. Parameters are seperated by a space.
	
	irc messages may not exceed a length of 512 characters.
	"""

	def __init__(self, rawmsg):
		self.rawmsg = rawmsg;
		data = re.match(self.MESSAGE_PATTERN,rawmsg).groupdict();
		prefix = data["prefix"];
		self.command = data["command"];
		paramstr = data["paramstr"];
		if prefix is not None:
			data = re.match(self.PREFIX_PATTERN,prefix).groupdict();
			self.source = data["source"] if data["source"] != None else "";
			self.user = data["user"] if data["user"] != None else "";
			self.host = data["host"] if data["host"] != None else "";
		else:
			self.source = self.user = self.host = "";

		#1. see if the trailing parameter is there. if it is, it will be at the end, so extract it.
        
		start = paramstr.find(" :");
		if start != -1:
			trailing = paramstr[start+2:];
		#2. consider only the substring from the start of paramstr to before the start of the trailing param
		paramstr = paramstr[:start];
       	 #3. split this substring by " " to obtain a list of parameters
		self.params = paramstr.split();
		#str.split(" ") will include empty strings in the list. calling it without an argument won't.
		#4. append the trailing param
		if start != -1:
			self.params.append(trailing);

	def __str__(self):
		return self.rawmsg;
	
	def __repr__(self):
		return repr(self.rawmsg);
	
	def __len__(self):
		return len(self.rawmsg);

#x = ["PING :uk.irc.newerth.com\r\n",":BEARD!BEARD@chattingaway-86E9B613.cable.virginmedia.com PRIVMSG #brdtest :hi\n",":uk.irc.newerth.com 366 BRDbot #brdtest :End of /NAMES list.\r\n"];

class IRCHandler:
	LEGAL_NICK_CHAR_PATTERN = re.compile(r"[a-zA-Z0-9\[\]\\`_^{|}\-]");
	"""irc nicknames begin with a letter. the rest of the characters must be alphanumeric or one of -[]\`^{}"""
	
	HOST = "localhost";
	CHANNEL = "#sr-users";
	def __init__(self):
		global gblEventHandler;
		gblEventHandler.addNotifyListener(self);
		
		self.NICKNAME = "";
		self.REALNAME = "";
		
	def onEvent(self,e):
		if e.scope == "chat_send_msg":
			IRC_SendMessage("PRIVMSG "+cvar_get("chat_channel")+" :"+e.string+"\r\n");
		elif e.scope == "chat_send_quit":
			IRC_SendMessage("QUIT :"+e.string+"\r\n");
			gblEventHandler.notifyEvent("chat_quit", "", "^777You left the chat." );
	
	def onMessage(self,rawmsg):
		m = IRCMessage(rawmsg);
		if hasattr(self, m.command) and callable(getattr(self, m.command)):
			getattr(self,m.command)(m);
		elif hasattr(self, "_"+m.command): #for numerical commands. You can't def 123(): but you can def _123():
			getattr(self,"_"+m.command)(m);
		
	def onConnected(self):
		for char in cvar_get("name"):
			self.NICKNAME += char if re.match(self.LEGAL_NICK_CHAR_PATTERN,char) != None else "_";
		self.REALNAME = cvar_get("username");
		IRC_SendMessage("USER SRClient "+self.HOST+" bla :"+self.REALNAME+"\r\n");
		IRC_SendMessage("NICK "+self.NICKNAME+"\r\n");
		IRC_SendMessage("JOIN "+self.CHANNEL+"\r\n");
	
	#handle incoming msgs
	def PING(self, m):
		IRC_SendMessage(m.rawmsg.replace("PING","PONG",1));
	
	def PRIVMSG(self,m):
		gblEventHandler.notifyEvent("chat_msg", m.source, m.params[-1] );
	
	def JOIN(self, m):
		if self.NICKNAME.startswith(m.source):
			gblEventHandler.notifyEvent("chat_connect", "", "You joined the chat." );
		else:
			gblEventHandler.notifyEvent("chat_join", m.source,  m.source +" entered the chat." );

	def PART(self, m):
		gblEventHandler.notifyEvent("chat_quit", m.source, m.source +" left the chat." );

	def _433(self, m):
		#ERR_NICKNAMEINUSE
		self.NICKNAME += "_";
		IRC_SendMessage("NICK "+self.NICKNAME+"\r\n");
		IRC_SendMessage("JOIN "+self.CHANNEL+"\r\n");

gblIRCHandler = IRCHandler();


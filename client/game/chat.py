#(c) 2012 savagerebirth.com

import silverback

import sleekxmpp
from sleekxmpp.savagexmpp import SharedXMPP
from sleekxmpp import Iq
from sleekxmpp.exceptions import IqError, IqTimeout, XMPPError
from sleekxmpp.xmlstream import register_stanza_plugin
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.matcher import StanzaPath, MatchXPath, MatchXMLMask
import logging
import threading
import stackless
import stacklesslib
# Fuck timezones:
import time
import datetime

# Chat related events:

class ChatEvent(NotifyEvent):
	def __init__(self, scope, timeStamp, fromstr, string):
		NotifyEvent.__init__(self, scope, fromstr, string);
		self.timeStamp = timeStamp;

class MUCEvent(ChatEvent):
	def __init__(self, scope, timeStamp, room, fromstr, string):
		ChatEvent.__init__(self, scope, timeStamp, fromstr, string);
		self.room = room;

class ChatNotificationEvent(ChatEvent):
	def __init__(self, notificationId, scope, timeStamp, title, msg, command, arg):
		ChatEvent.__init__(self, scope, timeStamp, "", msg);
		self.command = command;
		self.arg = arg; # Could extend that with *args, but no need for that right now.		
		self.notificationId = notificationId;
		self.title = title;

# Custom Stanza classes

class MatchInvite(sleekxmpp.xmlstream.ElementBase):

	"""
	A stanza class for XML content of the form:

	<matchinvite xmlns="savagerebirth.com">
	  <msg>X</msg>
	  <name>X</name>
	  <server>X</server>
	  <port>X</port>
	</matchinvite>
	"""
   
	#: The `name` field refers to the basic XML tag name of the
	#: stanza. Here, the tag name will be 'action'.
	name = 'matchinvite'

	#: The namespace of the main XML tag.
	namespace = 'savagerebirth.com'

	#: The `plugin_attrib` value is the name that can be used
	#: with a parent stanza to access this stanza. For example
	#: from an Iq stanza object, accessing:
	#: 
	#:     iq['action']
	#: 
	#: would reference an Action object, and will even create
	#: an Action object and append it to the Iq stanza if
	#: one doesn't already exist.
	plugin_attrib = 'matchinvite'

	#: Stanza objects expose dictionary-like interfaces for
	#: accessing and manipulating substanzas and other values.
	#: The set of interfaces defined here are the names of
	#: these dictionary-like interfaces provided by this stanza
	#: type. For example, an Action stanza object can use:
	#:
	#:     action['method'] = 'foo'
	#:     print(action['param'])
	#:     del action['status']
	#:
	#: to set, get, or remove its values.
	interfaces = set(('msg', 'name', 'server', 'port'))

	#: By default, values in the `interfaces` set are mapped to
	#: attribute values. This can be changed such that an interface
	#: maps to a subelement's text value by adding interfaces to
	#: the sub_interfaces set. For example, here all interfaces
	#: are marked as sub_interfaces, and so the XML produced will
	#: look like:
	#: 
	#:     <action xmlns="sleekxmpp:custom:actions">
	#:       <method>foo</method>
	#:     </action>
	sub_interfaces = interfaces


# The main (global) chat handler.
	

class XMPPHandler:
	logger = logging.getLogger("silverback.chat.xmpphandler");
	def __init__(self):

		self.xmpp = None;
		self.connected = False;

		self.eventHistory = deque();

		self.joiningFlags = {}; # {room: bool}

		self.chatListeners = [];
		self.eventQueue = channel();

		self.stop = threading.Event();
		self.queue_thread = threading.Thread("XMPP queue runner", self._run_queue);
		self.stop.clear();
		self.queue_thread.start();

		# Notification vars:

		self.notificationId = 0;
		# Keep track of active notification events in case a new listener gets added (=history);
		self.activeNotificationEvents = {}; # id:event


	############################ XMPP STUFF ##############################

	#########################
	## Connection handling ##
	#########################

	def connect(self):

		self.chatEvent("chat_establish", "System", "Trying to establish a connection to the chat server...");

		username = cvar_get("username") if cvar_get("username") != "" else "nouser";
		
		self.xmpp = SharedXMPP(username + "@savagerebirth.com", cvar_get("password"));
		# event handlers

		self.xmpp.add_event_handler("session_start", self.start);
		#self.xmpp.add_event_handler("connected", self.start);
		self.xmpp.add_event_handler("disconnected", self.disconnected);
		self.xmpp.add_event_handler("no_auth", self.failed_auth);

		self.xmpp.add_event_handler("stream_error", self.stream_error);
		self.xmpp.add_event_handler("socket_error", self.socket_error);

		self.xmpp.add_event_handler("roster_received", self.roster_received);
		self.xmpp.add_event_handler("changed_status", self.changed_status);
		self.xmpp.add_event_handler("roster_update", self.roster_update); 

		self.xmpp.add_event_handler("message", self.message);		

		# MUC
		self.xmpp.add_event_handler('groupchat_message', self.muc_message);
		self.xmpp.add_event_handler('groupchat_subject', self.muc_subject);

		# Presence will be handled later and room-specific handlers will be added
		#self.xmpp.add_event_handler('groupchat_presence', self.muc_presence);		
		#self.xmpp.add_event_handler('groupchat_direct_invite', self.groupchat_direct_invite);
		self.xmpp.add_event_handler('groupchat_invite', self.groupchat_invite_received);

		# Subscription
		self.xmpp.add_event_handler('presence_subscribed', self.subscribed);
		self.xmpp.add_event_handler('presence_subscribe', self.subscribe);
		self.xmpp.add_event_handler('presence_unsubscribed', self.unsubscribed);
		self.xmpp.add_event_handler('presence_unsubscribe', self.unsubscribe);
		#self.xmpp.add_event_handler('roster_subscription_request', self.new_subscription);

		self.xmpp.auto_authorize = None;
		#self.xmpp.auto_subscribe = False; # should be true, but w/e

		# Custom Stanzas:

		self.xmpp.registerHandler(
					 Callback('Match invite',
					 StanzaPath('iq@type=set/matchinvite'),
					 self._handle_matchinvite));

		self.xmpp.add_event_handler('match_invite', self.matchInvite);


		register_stanza_plugin(Iq, MatchInvite);

		self.xmpp.connect();
		self.connected = True;

	def disconnect(self):
		self.xmpp.disconnect();
		self.connected = False;
		self.eventHistory = deque();
		self.joiningFlags = {};

		self.chatEvent("chat_logged_out", "", "");
		# Clear history, activate overlays etc.

	def reconnect(self, answer=True):
		if answer:
			self.chatEvent("chat_establish", "System", "Trying to reconnect to the chat server...");
			self.xmpp.connect(reattempt=True);
			self.connected = True;

	def isConnected(self):
		return self.connected;

	def start(self, e):
		self.xmpp.start(e);
		self.chatEvent("chat_connect", "System", "You are connected to the chat service.");

		self.joinMUC('help@conference.savagerebirth.com', cvar_get('username'));

	def failed_auth(self, e):
		self.xmpp.failed_auth(e);
		self.chatEvent("chat_quit", "System", "Could not authenticate. Quitting chat service.");

	def disconnected(self, e):
		self.xmpp.disconnected(e);
		self.chatEvent("chat_disconnect", "System", "Chat service connection lost");

	def socket_error(self, obj):
		self.chatEvent("chat_quit", "System", "Socket error. Shutting down chat service. \nPlease contact the SR staff at savagerebirth.com.");

	def stream_error(self, error):
		self.chatEvent("chat_quit", "System", "Stream error. Shutting down chat service. \nPlease contact the SR staff at savagerebirth.com.");
		self.xmpp.disconnect();
		self.chatNotification("notify_chat_reconnect", "Stream Error", "A Stream Error occured. Do you want to reconnect?", self.reconnect)

	###########################
	## Subscription handling ##
	###########################

	def subscribeTo(self, name):
		# check if the name is valid first, TODO
		jid = name + "@savagerebirth.com";

		#self.xmpp.send_presence(pto=jid, ptype='subscribe');
		
		self.xmpp.update_roster(jid, name=name, groups=["Friends"]);
		self.xmpp.client_roster[jid].subscribe(); # works fine!

	def handleSubscripton(self, name, sub):
		jid = name + "@savagerebirth.com";
		if sub == "subscribe" or sub == True or sub == 1:
			self.xmpp.client_roster[jid].authorize();
			self.xmpp.client_roster[jid].subscribe();

		elif sub == "unsubscribe" or sub == False or sub == 0:
			self.xmpp.del_roster_item(jid);
			self.xmpp.client_roster[jid].unsubscribe();
			self.xmpp.client_roster[jid].unauthorize();
			self.roster_update(self.xmpp.client_roster);

	def subscribe(self, pres):
		"""
		# if we ever have a banlist:
		if presence['from'] in banlist:
			self.send_presence(pto=presence['from'], 
							   ptype='unsubscribed');
			return;
		"""
		
		name = str(pres['from'].bare).split('@', 1)[0];
		# Tell the user a request went in:
		if not self.xmpp.client_roster[pres['from']]['pending_out'] and not self.xmpp.client_roster[pres['from']]['subscription'] == "none":
			msg = name + " wants to be your new friend!";
			self.chatNotification("notify_friend_request", "Friend Request", msg, self.handleSubscripton, name);


	def subscribed(self, pres):		

		name = str(pres['from'].bare).split('@', 1)[0];

		self.xmpp.client_roster[pres['from']].authorize();
		self.xmpp.update_roster(pres['from'], name=name, groups=["Friends"]);

		msg = "You and " + name + " are now friends!"
		self.chatNotification("notify_friend_accept", "Friend Accepted", msg);
		#self.xmpp.update_roster(pres['from'].bare, name=jid, groups=["Friends"], subscription='both'); 

		self.xmpp.send_presence(pto=pres['from']);

	# Unsubscribe needs more testing, but chatserver is down
	def unsubscribe(self, pres):
		"""
		# TODO!
		self.xmpp.del_roster_item(pres['from'])
		self.xmpp.send_presence(pto=pres['from'], ptype='unsubscribed')
		#self.xmpp.client_roster[jid].unsubscribe();
		#self.xmpp.client_roster[jid].unauthorize();
		"""
		pass;

	def unsubscribed(self, pres):
		"""
		# TODO!
		self.xmpp.del_roster_item(pres['from'])
		self.xmpp.send_presence(pto=pres['from'], ptype='unsubscribe')
		self.xmpp.client_roster[pres['from']].unsubscribe();
		self.xmpp.client_roster[pres['from']].unauthorize();
		"""
		pass;

	######################
	## Message handling ##
	######################

	def message(self, msg):
		logger.debug("MSG: "+str(msg))
		if msg['type'] in ('chat', 'normal') and msg['type'] != 'groupchat':

		# Delay stuff:

			if StanzaPath("message/delay").match(msg):
				self.chatEvent("chat_msg", str(msg['from'].user), str(msg['body']),stamp=msg['delay']['stamp']);
			else:
				self.chatEvent("chat_msg", str(msg['from'].user), str(msg['body']));


	def sendMessageTo(self, to, msg):
		jid = to + "@savagerebirth.com"
		self.xmpp.send_message(mto=jid, mbody=msg, mtype='chat', mnick=cvar_get("username"));


	######################
	##  Custom stanzas  ##
	######################

	def sendInvite(self, to, msg, server='phoenix.savagerebirth.com', port='11236'):

		iq = self.xmpp.Iq()
		iq['to'] = to;
		iq['type'] = 'set';
		iq['matchinvite']['msg'] = msg;
		iq['matchinvite']['server'] = server;
		iq['matchinvite']['port'] = port;
		#iq['matchinvite']['name'] = name;
		try:
			resp = iq.send();
		except XMPPError:
			logger.error('There was an error sending a matchinvite stanza.');
			self.chatNotification("notify_error", "Match Invite Error", "Failed to invite " + to.split('@', 1)[0] + ".")


	def _handle_matchinvite(self, iq):
		"""
		They used two methods in the sleekxmpp example because of threading. 
		I'll just stick to it. 
		"""
		self.xmpp.event('match_invite', iq);

	def matchInvite(self, iq):
		"""
		We received a custom stanza: MatchInvite! We can now go home happily and 
		play with it all day long, until we decide to answer it. 
		"""
		name = str(iq['from'].bare).split('@', 1)[0];

		msg = str(iq['matchinvite']['msg']);
		serverAddress = str(iq['matchinvite']['server']);
		port = str(iq['matchinvite']['port']);

		#serverName = str(iq['matchinvite']['name']);

		iq.reply();
		iq.send();

		#text = name + " invited you to play on " + serverName;
		server = serverAddress + ":" + port;


		self.chatNotification("notify_match_invite", "Match Invite", msg, self.answerInvite, server);

	def answerInvite(self, server, answer):
		if answer:
			logger.debug("Invite accepted, connecting to: " + server);
			connect(server);

	########################
	## Groupchat handling ##
	########################

	def joinMUC(self, room, nick):
		self.xmpp.plugin['xep_0045'].joinMUC(room, nick, wait=True);

		self.joiningFlags[room] = False;

		# stuff for handling room-specific presence
		self.xmpp.add_event_handler("muc::" + room + "::got_online", self.muc_got_online);
		self.xmpp.add_event_handler("muc::" + room + "::got_offline", self.muc_got_offline);

	def muc_message(self, msg):
		if msg['type'] == 'groupchat':
			user = str(msg['mucnick']);
			room = str(msg['mucroom']).split('@', 1)[0];
			msg = str(msg['body'])
			self.chatEvent("muc_msg", user, msg, room);

	def sendMUCMessage(self, room, msg):
		jid = room + "@conference.savagerebirth.com";
		self.xmpp.send_message(mto=jid, mbody=msg, mtype='groupchat', mnick=cvar_get("username"));

	def muc_got_online(self, pres):
		if self.joiningFlags[str(pres['from'].bare)]:
			room = str(pres['from'].bare).split('@', 1)[0];
			user = str(pres['muc']['nick']);
			self.chatEvent("muc_presence", user, "available", room);

	def muc_got_offline(self, pres):
		user = str(pres['muc']['nick']);
		room = str(pres['from'].bare).split('@', 1)[0];
		self.chatEvent("muc_presence", user, "unavailable", room);

	def muc_subject(self, msg):
		if msg['type'] == 'groupchat':

			room = str(msg['mucroom']).split('@', 1)[0];

			if not self.joiningFlags[str(msg['from'].bare)]:
				self.joiningFlags[str(msg['from'].bare)] = True;
				# tell the gui that we joined the room:
				self.chatEvent("muc_presence", cvar_get('username'), "available", room);
				# Also, post a muc roster update:
				roster = self.xmpp.plugin['xep_0045'].getRoster(msg['mucroom']);
				for user in roster:
					self.chatEvent("muc_roster_update", str(user), "available", room);

			
			msg = str(msg['subject'])
			self.chatEvent("muc_subject", room, msg, room);
			
	# Stuff that lacks API documentation, will try to sort that out later:

	def groupchat_direct_invite_received(self, msg):
		pass

	def groupchat_invite_received(self, inv):
		name = str(inv['to'].bare).split('@', 1)[0];
		room = str(inv['from'].bare).split('@', 1)[0];
		msg = name + " invited you to the room " + e.room + "!"
		self.chatNotification("notify_muc_invite", "Chatroom Invite", msg, self.handleInvite, room);

	def handleInvite(self, join, roomName):
		if join:
			room = roomName + "@conference.savagerebirth.com"
			self.joinMUC(room, cvar_get('username'));

	def inviteToRoom(self, name, room, fromstr):
		jid = name + "@savagerebirth.com";
		roomJid = room + "@conference.savagerebirth.com"
		self.xmpp.plugin['xep_0045'].invite( roomJid, jid, reason='Hello, why don\'t you join ' + roomJid + "?", mfrom=fromstr);

	#####################
	## Roster handling ##
	#####################

	def changed_status(self, pres):
		# Here we keep track of the status changes.

		# If it's a MUC presence, we're going to ignore it. MUC presence stanzas are handled elswhere.
		if MatchXPath("{%s}presence/{%s}x" % (self.xmpp.default_ns, 'http://jabber.org/protocol/muc#user')).match(pres):
			return;

		if pres['from'].user == self.xmpp.boundjid.user:
			return;
		
		if pres['type'] == 'available':
			status = "Online";

		elif pres['type'] == 'xa' or pres['type'] == 'away' or pres['type'] == 'dnd':
			status = "Away";

		else: #elif pres['type'] == 'unavailable' or pres['type'] == 'error' or pres['type'] == 'probe':
			status = "Offline";

		if "savage" in self.xmpp.client_roster.presence( pres['from'].bare):
			status = "Ingame";
			
		self.chatEvent("chat_contact_update", pres['from'].user, status);

	def roster_received(self, roster):
		self.roster_update(roster);

	def roster_update(self, roster):
		self._roster_update(self.xmpp.client_roster);

	def _roster_update(self, roster, listener=None):

		# Reworking that, sometimes simple things are better:
		# 1. get the groups we're in
		groups = roster.groups();

		rosterDict = {};

		# Formatting the info in roster:
		for group in groups:
			if group == "":
				continue;

			rosterDict[group] = {};

			for jid in groups[group]:

				status = "Offline"

				name = roster[jid]['name'] 
				if name == None:
					logger.error("Bad things are happening in chat.py, _roster_update()");
				elif len(name) == 0:
					name = jid.split('@', 1)[0];

				if roster[jid]['subscription'] != 'both':
					status = "Pending";
					break;
				
				connections = roster.presence(jid);

				for res, pres in connections.items():

					online = ['available', 'online'];

					if res == "savage":
						status = "Ingame";
						break; # If we're ingame, ignore every other resource. SR > everything else.

					elif pres['status'].lower() in online or pres['show'] in online:
						status = "Online";
						break;

					# FU iChat!
					elif pres['status'] == "" and pres['show'] == "" and res == "iChat":
						status = "Online";
						break;

					elif pres['status'].lower() == "away" or pres['show'] == "away":
						status = "Away";

					else:
						status = "Away";					
									
				rosterDict[group][name] = status;

		# send the dict to the gui:

		if listener:
			e = ChatEvent("roster_update", cvar_get('host_time'), "", rosterDict);
			listener.onChatEvent(e);
		else:
			self.chatEvent("roster_update", "", rosterDict);

	def addToHistory(self, e):
		# I'm going to just add EVERY SINGLE EVENT! to the history. Makes things easier,
		# and I don't think that performance or memory will be issues. At least not for now.
		self.eventHistory.append(e);		


	#################################### EVENT STUFF ######################################


	def addListener(self, listener):

		if self.isConnected():
		
			# Whenever a new listener joins, check if it's a ChatBox and send him the history:
			if isinstance(listener, MenuChatBox):
				for e in self.eventHistory:
					listener.onChatEvent(e);

			# Whenever a new ChatRoster gets added, make sure to send it all roster info.
			if isinstance(listener, BuddyRoster):				
				for e in self.eventHistory:
					listener.onChatEvent(e);
				self._roster_update(self.xmpp.client_roster, listener);
			
			if isinstance(listener, JabberChatBox):
				for e in self.eventHistory:
					listener.onChatEvent(e);		

		self.chatListeners.append(listener);

	def _run_queue(self):
		#callback to all the listeners in the list
		while not self.stop.is_set():
			e = self.eventQueue.receive();
			for l in self.chatListeners:
				try:
					l.onChatEvent(e)
				except BaseException as ex:
					try:
						import traceback;
						self.logger.error( traceback.format_exc());
					except ImportError:
						self.logger.error("XMPPHandler caught exception: "+str(ex)+"\n");           

	def _process_chat_event(self, e):
		self.eventQueue.send(e);

		self.addToHistory(e);

		self.onChatEvent(e);

	def chatEvent(self, scope, fromstr, string, room=False, stamp=""):			
		if stamp != "":
			local = stamp - datetime.timedelta(seconds=time.timezone);
			timeStamp = str(local)[11:19];
		else:
			timeStamp = cvar_get('host_time');

		if room:			
			e = MUCEvent(scope, timeStamp, room, fromstr, string);
		else:
			e = ChatEvent(scope, timeStamp, fromstr, string);             
		# move any recieves down the stack away from the main tasklet (the core engine thread) 
		# so that we don't incur any Runtime or StopIteration exceptions
		task = stackless.tasklet(self._process_chat_event);
		task.setup(e);

	def chatNotification(self, scope, title, msg, command=None, arg=None):
		timeStamp = cvar_get('host_time');

		e = ChatNotificationEvent(self.notificationId, scope, timeStamp, title, msg, command, arg);
		self.notificationId += 1;

		task = stackless.tasklet(self._process_chat_event)
		task.setup(e)

	def onChatEvent(self, e):
		if e.scope == "chat_logout":
			self.disconnect();
		elif e.scope == "chat_send_msg":
			self.sendMessageTo(e.fromstr, e.string);
		elif e.scope == "muc_send_msg":
			self.sendMUCMessage(e.room, e.string);
		elif e.scope == "chat_roster_request":
			self.roster_update("");
		elif e.scope == "chat_subscribe":
			self.subscribeTo(e.string);
		elif e.scope == "muc_invite_sent":
			self.inviteToRoom(e.string, e.room, e.fromstr);
		elif e.scope == "chat_match_invite":
			server, port = e.room.split(":", 1);
			self.sendInvite(e.fromstr, e.string, server, port);


gblXMPPHandler = XMPPHandler();

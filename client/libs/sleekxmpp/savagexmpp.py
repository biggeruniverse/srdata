# -*- coding: utf-8 -*-
#(c) 2012 savagerebirth.com
# This file defines the abstract XMPP client that the website and the gameclient share.

from __future__ import absolute_import, unicode_literals

import sleekxmpp
import logging

from sleekxmpp.clientxmpp import ClientXMPP
from sleekxmpp.xmlstream import XMLStream, JID

class SharedXMPP(ClientXMPP):
	logger = logging.getLogger(__name__)
	def __init__(self, address, port, jid, password, resource, plugin_config={}):
		ClientXMPP.__init__(self, jid + '/' + resource, password)

		self.dns_service = None;

		#self.auto_reconnect = False;

		self.session_timeout = 90;

		self.address = address;
		self.port = port;

		# Plugins to register:
		self.register_plugin('xep_0030'); # Service Discovery
		self.register_plugin('xep_0004'); # Data Forms
		self.register_plugin('xep_0060'); # PubSub
		# Big added those three, no idea what for tho - comment out all for now, we cawhen other stuff is working
		self.register_plugin('xep_0045'); # MUC
		self.register_plugin('xep_0199'); # XMPP Ping - No idea if we need that one

		# Event handlers
		self.add_event_handler("session_start", self.start);
		self.add_event_handler("message", self.message);
		self.add_event_handler("groupchat_message", self.groupchat_message);
		self.add_event_handler("disconnected", self.disconnected);
		self.add_event_handler("no_auth", self.failed_auth);
		self.add_event_handler("connected", self.connected);
		self.add_event_handler("roster_received", self.roster_received);
	
	def connect(self, reattempt=False, use_tls=True, use_ssl=False):
		self.printDebug('Connecting to chat server (' + self.address + ':' + unicode(self.port) + ')...');
		if ClientXMPP.connect(self, (self.address, self.port), use_tls=use_tls, use_ssl=use_ssl,reattempt=reattempt):
			self.process(block=False);

	def connected(self, e):
		self.printDebug('Connected to chat server');

	# Authed, setup everything
	def start(self, e):
		self.get_roster();
		self.send_presence();		
		self.printDebug('Authenticated with chat server');

	# Failed auth, send message and done..
	def failed_auth(self, e):
		self.printDebug('Error: Username or password incorrect');

	def message(self, msg):
		pass;

	def disconnected(self, e):
		self.printDebug('Disconnected from chat server');

	def groupchat_message(self, msg): # probably wrong, nope, it's right
		pass;

	def roster_received(self, e):
		self.printDebug('Received Roster');

	def printDebug(self, msg):
		self.logger.debug(msg);

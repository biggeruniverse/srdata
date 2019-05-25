# (c) 2012 savagerebirth.com

class RequestManager(CommAbstractWidget):

	def create(self):
		self.setSizePct(0.125, 0.333);
		self.setPosition(screenWidth-(self.getWidth()+10), int(screenHeight*0.025+5));
		self.setOpaque(0);
		
		self.requestQueue = [];
		
		gblEventHandler.addGameListener(self);

	def rebuild(self):
		pass;

	def frame(self):
		y = 0;
		#we're iterating over a copy of the list, so don't worry about the remove()!
		for req in self.requestQueue[:]:
			if req.isExpired():
				req.expire();
				self.requestQueue.remove(req);
				self.remove(req);
				continue;
			req.setY(y);
			y += req.getHeight()+10;

	def onEvent(self, e):
		if e.eventType == "request_cancel" or e.eventType == "request_approved" or e.eventType == "request_denied":
			for req in self.requestQueue:
				if req.player == e.sourceId:
					self.requestQueue.remove(req);
					self.remove(req);
					break;
		elif e.eventType == "request_powerup" or e.eventType == "request_gold" or e.eventType == "request_promote":
			i = None;
			for req in self.requestQueue:
				if req.player == e.sourceId:
					i = req;
					i.rebuild(e.sourceId, e.eventType, e.parameter);
					self.requestQueue.remove(i); #end of the line with you!
					break;
			else:
				i = RequestItem(e.sourceId, e.eventType, e.parameter);
				self.add(i);
			#above code ensures one request from a player at any given time
			self.requestQueue.append(i);

class RequestItem(DefaultWindow):
	def __init__(self, who, what, p):
		DefaultWindow.__init__(self);
		self.player = who;
		self.reqtype = what;
		self.parameter = p;
		self.timestamp = savage.getGameTime();
		
		self.setSizePct(0.125, 0.0833);
		
		self.name = DefaultLabel();
		self.icon = DefaultLabel();
		
		self.rebuild(who, what, p);
		
		self.add(self.name);
		self.add(self.icon, self.getWidth()-33, 1);

		self.approvebtn = DefaultImageButton();
		self.approvebtn.setImage("yestr.s2g");
		self.approvebtn.setId("approve");
		self.approvebtn.setSize(32,32);
		self.approvebtn.addActionListener(self);
		self.add(self.approvebtn, 10, self.getHeight()-32);
		
		self.denybtn = DefaultImageButton();
		self.denybtn.setImage("canceltr.s2g");
		self.denybtn.setId("deny");
		self.denybtn.setSize(32,32);
		self.denybtn.addActionListener(self);
		self.add(self.denybtn, 20+32, self.getHeight()-32);
		
	def rebuild(self, who, what, p):
		self.player = who;
		self.reqtype = what;
		self.parameter = p;
		self.timestamp = savage.getGameTime();
		
		pl = savage.getGameObject(who);
		team = savage.Team(pl.getTeam());
		objtype = savage.getObjectType(p);

		self.name.setCaption(pl.getName());

		if what == "request_powerup":
			self.icon.setImage(objtype.getValue("icon"));
		elif what == "request_gold":
			self.icon.setImage("/gui/standard/icons/gold/gold_icon.s2g");
		elif what == "request_promote":
			self.icon.setImage("/models/"+team.getRace()+"/items/icons/officer1.tga");
		self.icon.setSize(32,32);

	def isExpired(self):
		if cvar_getvalue("cl_cmdr_requestPersistTime")*1000+self.timestamp < savage.getGameTime():
			return True;
		return False;

	def onAction(self, e):
		if e.widget.getId() == "approve":
			self.approve();
		else:
			self.decline();
		
	def expire(self):
		pass;
	def approve(self):
		if self.reqtype == "request_powerup":
			CL_RequestActivatePowerup(self.player, self.parameter);
		elif self.reqtype == "request_gold":
			CL_RequestGiveGold(self.player, self.parameter);
		elif self.reqtype == "request_promote":
			CL_RequestPromote(self.player);
		CL_ApproveRequest(self.player);
		gblEventHandler.requestEvent("request_approved", self.player, self.parameter);
	def decline(self):
		CL_DenyRequest(self.player);
		gblEventHandler.requestEvent("request_denied", self.player, self.parameter);

reqman = RequestManager();
commhud.addWidget('requests', reqman);

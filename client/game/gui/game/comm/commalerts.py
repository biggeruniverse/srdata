# (c) 2013 savagerebirth.com


# For now, put those notifications only on commhud, I'll write a class for 
# hud and maybe spechud too, and commhud is going to be a subclass of those
# that has additional request support. 

# We have a few different types of notifications:

# 1. General game notifications:
#	e.g. player joined, player left, ref stuff

# 2. Research notifications:
#	what is being researched?
#	when is the research finished?

# 3. Attack notifications:
#	what is under attack?
#	is the attack critical?
# 3.1 Stronghold/Lair is under attack.
# 	this one should always be on top
#	if the stronghold is damaged, don't make the notification bleed priority, it'll stay there until repaired

# 4. Request notifications
#	only for commhud
#	need a button to accept/deny the request

# General rules:
# A notification will be initialized with a specific priority value, every millisecond
# the notification "bleeds" and loses some "priority" (except for stronghold health).
# This is mostly for sorting notifications by the time they were active, but also allows
# add low-tier notifications that aren't very important (player joined etc). 
# They might not start on top of the notification list, but I guess that's okay. 

# You should be able to click the notification window to jump to the location of the
# source. (Only applies to comm)
# This is especially critical for attacks and requests, Research can be quite helpful too.

# Attack and Research notifications could have a progress bar that shows health/progress, 
# but I guess that would only lead to way too much notifications. We'll see how it turns out.

# I'm not sure what to do with kill messages, but I guess I'll put them somewhere else. 
# Waaay too much spam on a big server. 

from silverback import *
import savage
from savage import WaitAction, CallAction
import logging
import time;
import tools;

class CommAlert(DefaultContainer):

	def __init__(self, prio, d, msg):
		DefaultContainer.__init__(self);

		# prio is in seconds, we have 16 frames every second:
		self.maxPriority = self.priority = float(prio * 16);
		self.rate = d;
		self.pos = None;

		self.setBackgroundColor(transparency);
		self.setSize(180, 36);

		self.content = DefaultContainer();
		self.content.setSize(self.getWidth() - 4, self.getHeight() - 4); # Framestyles!
		self.content.setBackgroundColor(windowTop);
		self.add(self.content, 2, 2);

		self.pic = glass.GlassLabel("");
		self.pic.setImage("todo.png");
		self.pic.setSize(self.getHeight(), self.getHeight());
		self.content.add(self.pic);

		self.text = DefaultLabel(msg);
		self.content.add(self.text, "center", "center");

		self.btn = glass.ImageButton();
		self.btn.setId("jump");
		self.btn.setImage("gui/game/images/transparent.s2g");
		self.content.add(self.btn);
		self.btn.setSizePct(1,1);
		self.btn.addActionListener(self);

	def bleed(self):
		self.priority -= self.rate;
		self.content.setAlpha(int ((self.priority / self.maxPriority) * 200) );
		if self.priority < 1:
			return False;
		else:
			return True;

	def expire(self):
		self.priority = 0;
		self.setAlpha(0);

	def onAction(self, e):
		if e.widget.getId() == "jump":
			if self.pos != None:
				x = self.pos[0];
				y = self.pos[1];
				CL_CenterCamera(x,y);

class ConnectionAlert(CommAlert):
	PRIORITY = 10; # 
	RATE = 1.5; # Priority/Second - Rate
	def __init__(self, what, who, where):
		self.playerId = who;
		player = savage.getGameObject(who);
		team = savage.getTeamObject(player.getTeam());

		race = team.getRace() + "s";
		msg = player.getFormattedName() + " " + what + " the " + race;		
		CommAlert.__init__(self, self.PRIORITY, self.RATE, msg);
		self.text.setFont(fontSizeSmall);
		self.text.setX(5);

		self.pic.setVisible(False);

class AttackAlert(CommAlert):
	PRIORITY = 10; # Always on top!
	RATE = 1;	
	def __init__(self, what, where):
		CommAlert.__init__(self, self.PRIORITY, self.RATE, "We're under attack");

		building = savage.getGameObject(what);
		self.pos = where;
		if not set(self.pos) - set((0,0)):
			# Maybe something went wrong, double check:
			self.pos = (building.getPosition()[0], building.getPosition()[1]);

		self.buildingId = what;

		self.pic.setImage("../../../"+ building.getType().getValue("icon")+".s2g");
		self.pic.setSize(self.content.getHeight() , self.content.getHeight());


class ResearchAlert(CommAlert):
	PRIORITY = 10; #cvars?
	RATE = 1;
	def __init__(self, ot, source):
		self.objtype = ot;
		self.source = source;
		#msg = ot.getName() + " is now available."
		msg = "Completed!";
		CommAlert.__init__(self, self.PRIORITY, self.RATE, msg);
		self.pic.setImage("../../../"+ self.objtype.getValue("icon")+".s2g");
		self.pic.setSize(self.content.getHeight() , self.content.getHeight());

		self.pos = self.source.getPosition();


class HealthAlert(CommAlert):
	PRIORITY = 9999; # Always on top!
	RATE = 0;	
	def __init__(self):
		CommAlert.__init__(self, self.PRIORITY, self.RATE, "");

		self.setVisible(False);

		team = savage.getLocalTeam();	

		self.obj = team.getCommandCenter();
		self.pos = self.obj.getPosition();

		self.pic.setImage(self.obj.getType().getValue("icon")+".s2g");
		self.pic.setSize(self.content.getHeight() , self.content.getHeight());

		self.bar = glass.GlassProgressBar();
		self.bar.setBackgroundColor(white);
		#self.bar.setForegroundColor(glass.Color(255,21,22, 128));
		self.bar.setForegroundColor(tools.HSLColor(0.33,0.8,0.66));
		self.bar.setSize(self.content.getWidth() - self.pic.getWidth() - 13, self.content.getHeight() - 8);
		self.bar.setBackgroundImage("gui/base/images/progress_bg.tga");
		self.content.add(self.bar, self.pic.getWidth() + 5, 4);
		
		self.label = DefaultLabel();
		self.label.setCaption("00000");
		self.label.setForegroundColor(glass.Color(255,237,237, 128));
		#self.label.setFont(fontSizeLarge);
		self.content.add(self.label, (self.bar.getWidth() // 2 - self.label.getWidth() // 2) + self.pic.getWidth() + 5,  "center");

		# re-adding the btn to move it on top
		self.content.add(self.btn);

	def rebuild(self):
		team = savage.getLocalTeam();
		self.obj = team.getCommandCenter();
		self.pos = self.obj.getPosition();

		self.pic.setImage(self.obj.getType().getValue("icon")+".s2g");
		self.pic.setSize(self.content.getHeight() , self.content.getHeight());

		self.setVisible(True);

	def flash(self):
		self.setVisible(True);


	def bleed(self):
		#team = savage.getLocalTeam();
		#self.obj = self.team.getCommandCenter();

		k = self.obj.getHealthPct();

		if k == 1.0:
			self.setVisible(False);
			return True;

		hue = (k-0.1)/2.7 if k > 0.1 else 0;
		
		self.bar.setForegroundColor(tools.HSLColor(hue,0.8,0.66));
		self.label.setCaption(str(int(self.obj.getHealth())));
		self.bar.setProgress(self.obj.getHealthPct());
		#self.setVisible(True);
		return True;

class RequestAlert(CommAlert):
	PRIORITY = 20 # 30 for officers
	RATE = 1; 
	def __init__(self, who, what, p):		

		self.playerId = who;
		self.parameter = p;
		self.reqtype = what;

		self.player = savage.getGameObject(who);
		team = savage.Team(self.player.getTeam());
		objtype = savage.getObjectType(p);

		prio = self.PRIORITY if not self.player.isOfficer() else self.PRIORITY + 10;		
		CommAlert.__init__(self, prio, self.RATE, "");

		self.text.setX(self.pic.getWidth() + 2);

		self.pos = self.player.getPosition();

		self.approvebtn = DefaultImageButton();
		self.approvebtn.setImage("yestr.s2g");
		self.approvebtn.setId("approve");
		self.approvebtn.setSize(32,32);
		self.approvebtn.addActionListener(self);
		self.content.add(self.approvebtn, self.content.getWidth() - 70, "center");
		
		self.denybtn = DefaultImageButton();
		self.denybtn.setImage("canceltr.s2g");
		self.denybtn.setId("deny");
		self.denybtn.setSize(32,32);
		self.denybtn.addActionListener(self);
		self.content.add(self.denybtn, self.content.getWidth() - 35, "center");

		self.btn.setSize(self.content.getWidth() - (self.content.getWidth() - self.approvebtn.getX()), self.content.getHeight());

		self.text.setCaption(self.player.getName());

		if what == "request_powerup":
			self.pic.setImage(objtype.getValue("icon")+".s2g");
		elif what == "request_gold":
			self.pic.setImage("/gui/game/images/gold_icon.s2g");
		elif what == "request_promote":
			self.pic.setImage("/models/"+team.getRace()+"/items/icons/officer1.tga");
		self.pic.setSize(self.content.getHeight(),self.content.getHeight());

	def onAction(self, e):
		if e.widget.getId() == "approve":
			self.approve();
		elif e.widget.getId() == "deny":
			self.decline();
		elif e.widget.getId == "jump":
			# A player can move!
			x, y, z = self.player.getPosition();
			CL_CenterCamera(x,y);

	def approve(self):
		if self.reqtype == "request_powerup":
			CL_RequestActivatePowerup(self.playerId, self.parameter);
		elif self.reqtype == "request_gold":
			CL_RequestGiveGold(self.playerId, self.parameter);
		elif self.reqtype == "request_promote":
			CL_RequestPromote(self.playerId);
		CL_ApproveRequest(self.playerId);
		gblEventHandler.requestEvent("request_approved", self.playerId, self.parameter);
		self.expire();

	def decline(self):
		CL_DenyRequest(self.playerId);
		gblEventHandler.requestEvent("request_denied", self.playerId, self.parameter);
		self.expire();


class CommAlertHandler(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);
		self.setSize(180, 0);

		self.alertQueue = [];

		gblEventHandler.addGameListener(self);
		#gblEventHandler.addNotifyListener(self);
		#gblQueue.addListener(self);

		self.bleed_thread = ActionSequence(savage.WaitAction(62), savage.CallAction(self.processBleeding, tuple([])))
		self.bleed_thread.set_loop(True)
		#self.bleed_thread = threading.Thread(name="bleeder", target=self._runner);
		#self.bleed_thread.start();

		self.ccAlert = HealthAlert();
		self.insertAlert(self.ccAlert, 0);

	def onShow(self):
		self.ccAlert.rebuild();

	def _runner(self):
		while not self.stop.is_set():
			self.processBleeding()
			time.sleep(1/16)

	def processBleeding(self):
		y = 0;
		# sort the queue:
		self.alertQueue.sort(key = lambda alert: alert.priority, reverse=True);
		# According to a few people on stackoverflow, this is about 5-10 times faster
		# than using rich comparison. Don't know what to think about all that.

		for alert in self.alertQueue:
			if alert.bleed():
				# Still alive, still alive
				alert.setY(y);
				y+= alert.getHeight();
			else:
				# Goodnight, sweet prince 
				self.alertQueue.remove(alert);
				self.remove(alert);
				
	def insertAlert(self, alert, i=1):
		self.add(alert);
		self.alertQueue.insert(i, alert); # ccAlert is always at 0!

	def onEvent(self, e):
		#if isinstance(e, GameEvent):
			#con_println(str(e));
			#pass;
		# CommanderEvents

		if e.eventType == "under_attack":
			where = e.pos;
			what = e.sourceId;
			# Is it the CommandCenter?
			cc = savage.getLocalTeam().getCommandCenter();
			if cc.objectId == what:
				self.ccAlert.rebuild();
				self.ccAlert.flash();
				#Flash CommandCenter alert!
				return;

			for alert in self.alertQueue:
				if isinstance(alert, AttackAlert):
					if alert.buildingId == e.sourceId:
						alert.expire();

			alert = AttackAlert(what, where);
			self.insertAlert(alert);

		# GameEvents
		elif e.eventType == "research_complete":
			objtype = savage.ObjectType(e.objtype);
			source = savage.getGameObject(e.sourceId);
			alert = ResearchAlert(objtype, source);
			self.insertAlert(alert);

		elif e.eventType == "player_join" or e.eventType == "player_leave":
			for alert in self.alertQueue:
				if isinstance(alert, ConnectionAlert):
					if alert.playerId == e.sourceId:
						alert.expire();

			what = "joined" if e.eventType == "player_join" else "left";
			alert = ConnectionAlert(what, e.sourceId, e.targetId);
			self.insertAlert(alert);

		elif e.eventType == "request_powerup" or e.eventType == "request_gold" or e.eventType == "request_promote":
			for alert in self.alertQueue:
				if isinstance(alert, RequestAlert):
					if alert.playerId == e.sourceId:
						alert.expire();

			alert = RequestAlert(e.sourceId, e.eventType, e.parameter);
			self.insertAlert(alert);
		

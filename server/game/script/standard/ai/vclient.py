# (c) 2012 savagerebirth.com

from silverback import *;
from vectors import Vec3;
from strategies import *;

class VClient(savage.Mind):
	def __init__(self, oid):
		savage.Mind.__init__(self, oid);
		self.strategy = None;
		self.target = None;

		if savage.Team(self.getTeam()).getRace() == "human":
			self.strategy = strategies.humanStrategies["scout"];
		else:
			self.strategy = strategies.beastStrategies["scout"];

		#if not self.strategy.build.isBuildAvailable():
		#TODO: handle using another strategy until we find one we can build (no sense in picking a siege strategy if we don't have siege, etc)

	def update(self):
		#TODO: check on our status, change plan as necessary, use medkits etc
		self.strategy.plan(self);

		if self.target is None or not self.target.isActive():
			self.target = self.strategy.selectTarget(self, savage.getRadiusObjects(self.objectId, 200.0));

		self.reassessPriorities();

		#NOTE:
		# "thinking" is done here
		self.fsm.evaluate();

		self.lastCollisions = []

	def buyInventory(self, strat):
		#go thru our list in priority
		for i in strat.getInventory():
			if not silverback.SV_VClient_RequestGive(self.objectId, i):
				objtype = savage.getObjectType(i);
				if self.getGold() < objtype.getCost("gold") and strat.doesRequestGold():
					silverback.SV_VClient_RequestGrant(self.objectId, i);

	def checkTargetRange(self):
		if self.target is None:
			return;
		if not (self.target.isUnitType() or self.target.isSiegeType()):
			return;

		#TODO: check range to target, switch weapons if necessary
		pass;

	def spawnCloseTo(self, objtype):
		import operator;
		points = {};
		team = savage.Team(self.getTeam());
		cc = Vec3(team.getCommandCenter().getPosition());

		objs = savage.getActiveObjects();
		for obj in objs:
			points[obj] = Vec3(obj.getPosition()).distanceSqTo(cc);
		sp = sorted(points.iteritems(), key=operator.itemgetter(1))

		objpos = Vec3(sp[0][0].getPosition());

		#we have the closest object of objtype to our CC
		#now find the closest spawnpoint to that object
		objs = team.getSpawnPoints();
		for obj in objs:
			points[Vec3(obj.getPosition()).distanceSqTo(objpos)] = obj;
		sp = sorted(points.iteritems(), key=operator.itemgetter(0))

		silverback.SV_VClient_RequestSpawn(self.objectId, sp[0][1].objectId);	

	#spawnForward is a specialized spawnCloseTo, that's a little quicker because it's only looking at the enemy CC
	def spawnForward(self):
		import operator;
		points = {};
		team = savage.Team(self.getTeam());
		t = 1;
		if self.getTeam() == t:
			t = 2;
		enemyteam = savage.Team(t);

		cc = Vec3(enemyteam.getCommandCenter().getPosition());
		objs = team.getSpawnPoints();
		for obj in objs:
			points[Vec3(obj.getPosition()).distanceSqTo(cc)] = obj;
		sp = sorted(points.iteritems(), key=operator.itemgetter(0))
		silverback.SV_VClient_RequestSpawn(self.objectId, sp[0][1].objectId);	

	def useItem(self, slot):
		savage.player_invswitch(self.objectId, slot);
		if savage.player_getcurrentinventoryslotindex(self.objectId) == slot:
			silverback.SV_VClient_Input(B_ATTACK);

	def handleGoal(self):
		if self.goal == self.lastGoal:
			return;

		con_println("handling vclient goal"+str(self.goal)+"\n");
		if self.goal is None:
			return
		elif self.goal.state == savage.Goal.AIGOAL_CONSTRUCT:
			self.fsm.insertState(savage.ConstructState(self.goal.targetObject));
			self.fsm.insertState(savage.ChaseState(self.goal.targetObject, 100));
		elif self.goal.state == savage.Goal.AIGOAL_MINE:
			self.fsm.insertState(savage.MineState(self.goal.targetObject));
			self.fsm.insertState(savage.ChaseState(self.goal.targetObject, 100));
		else:
			savage.Mind.handleGoal(self);

	def getUID(self):
		return savage.player_getuid(self.objectId);

	def getClanID(self):
		return savage.player_getclanid(self.objectId);

	def getClanIcon( self, padding=False ):
		return "^clan " + str(self.getClanID()) + "^";

	def getGold(self):
		return savage.player_getgold(self.objectId);

	def getXp( self):
		return savage.player_getxp(self.objectId);

	def getKills(self):
		return savage.player_getkills(self.objectId);

	def getDeaths(self):
		return savage.player_getdeaths(self.objectId);

	def getAssists(self):
		return savage.player_getassists(self.objectId);

	def getLevel(self):
		return savage.player_getlevel(self.objectId);

	def getClanIconString( self ):
		cid = self.getClanID();
		if cid == 0:
			return "^icon transparent^";
		return "^clan " + str(cid) + "^";

	def getClanTag(self):
		return "^599BOT";

	def getFormattedName(self):
		return self.getClanTag() + "^w" + self.getClanIconString() + self.getName();

	def getPing(self):
		return 0;

	def isPlayer(self):
		return True;

	def isCommander(self):
		return False;

	def isOfficer(self):
		return savage.player_isofficer(self.objectId);

	def isReferee( self):
		return False;

	def onUnitSelect(self):
		#go thru and get everything we need
		con_dprintln("I'm buyin swag with my "+str(self.getGold())+"\n");
		cost = self.strategy.build.getTotalCost();
		if cost <= self.getGold():
			self.buyInventory(self.strategy);
			self.spawnForward();
		else:
			self.fsm.insertState(ReturnToBaseState());
			self.fsm.insertState(FarmState(cost));
			self.spawnCloseTo(savage.getObjectType("npc_monkit"));

	def onDeath(self, killer):
		silverback.SV_VClient_VoiceCommand(self.objectId, 7,6);
		self.setPrimaryAnimState(AnimStates.AS_DEATH_GENERIC);
		objs = savage.getRadiusObjects(self.objectId, 200.0);
		for obj in objs:
			if obj.getTeam() == self.getTeam() and obj.isActive() and obj.isPlayer():
				ot = obj.getType();
				if ot.getName() == "human_medic" or ot.getName() == "beast_medic":
					silverback.SV_VClient_VoiceCommand(self.objectId, 2,8);
					self.fsm.insertState(ReturnToBaseState());
					self.fsm.insertState(WaitState(30000));
					return;
		silverback.SV_VClient_RequestLoadout(self.objectId);


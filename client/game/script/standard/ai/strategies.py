# (c) 2012 savagerebirth.com

class Build:
	def __init__(self, inv):
		self.inventory = inv;

	def getTotalCost(self):
		inv = [None, None, None, None, None];
		#FIXME: this needs to be far more robust, it needs to fill up a virtual inventory (5 slots) with what is available, and then get the cost of that list
		total = 0;
		for i in self.inventory:
			ot = savage.getObjectType(i);
			total = total + ot.getCost("gold");
		return total;

	def isBuildAvailable(self):
		inv = [None, None, None, None, None];
		return False;

class Strategy:
	def __init__(self):
		import strategies;
		self.build = strategies.Build([]);		

	def doesRequestGold(self):
		return False;

	def getInventory(self):
		return self.build.inventory;

	def selectTarget(self, mind, objs):
		return None;

	def plan(self, mind):
		if mind.goal is None:
			mind.addGoal(savage.Goal(savage.Goal.AIGOAL_IDLE, 10000))

class ScoutStrategy(Strategy):
	def __init__(self):
		import strategies;
		strategies.Strategy.__init__(self);

	def selectTarget(self, mind, objs):
		target = None;
		#find a weak target, or a worker or something (we're only scouting)
		for obj in objs:
			if obj.getTeam() == mind.getTeam():
				continue;
			if obj.getHealth() < 200 or obj.getType().isWorkerType() or obj.getType().isNPCType():
				target = obj;
				break;
		return target;

	#def plan(self, mind):
	#	if mind.goal is None or mind.goal.state is savage.Goal.AIGOAL_IDLE:
			#just look around
	#		pass;
			

class HumanScoutStrategy(ScoutStrategy):
	def __init__(self):
		import strategies;
		strategies.ScoutStrategy.__init__(self);
		self.build = strategies.Build(["human_nomad", "human_fluxgun", "human_discharger", "human_scattergun", "human_crossbow", "human_motion_sensor", "human_medkit", "human_medkit"]);


class BeastScoutStrategy(ScoutStrategy):
	def __init__(self):
		import strategies;
		strategies.ScoutStrategy.__init__(self);
		self.build = strategies.Build(["beast_scavenger", "beast_strata2", "beast_strata1", "beast_fire1", "beast_fire_trap", "beast_frenzy"]);

beastStrategies = { "scout":BeastScoutStrategy()};
humanStrategies = { "scout":HumanScoutStrategy()};


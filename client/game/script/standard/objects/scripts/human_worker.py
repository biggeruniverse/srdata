# (c) 2011 savagerebirth.com

from silverback import *;
from savage import Mind;

class human_worker(Mind):
	def __init__(self, oid):
		savage.Mind.__init__(self, oid);

	def handleGoal(self):
		if self.goal == self.lastGoal:
			return;

		if self.goal.state == savage.Goal.AIGOAL_CONSTRUCT:
			self.fsm.insertState(savage.ConstructState(self.goal.targetObject));
			self.fsm.insertState(savage.ChaseState(self.goal.targetObject, 100));
		elif self.goal.state == savage.Goal.AIGOAL_MINE:
			self.fsm.insertState(savage.MineState(self.goal.targetObject));
		else:
			savage.Mind.handleGoal(self);

	def onDamaged(self, target, amt):
		con_dprintln("I'm running!\n");
		g = savage.Goal(savage.Goal.AIGOAL_EVADE, 10000);
		g.targetObject = target;
		self.addGoal(g);


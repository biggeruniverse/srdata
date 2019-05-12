#(c) 2011 savagerebirth.com

from vectors import Vec3;

class Goal:
	AIGOAL_IDLE = 0;
	AIGOAL_GOTO = 1;
	AIGOAL_FOLLOW = 2;
	AIGOAL_EVADE = 3;
	AIGOAL_CONSTRUCT = 4;	
	AIGOAL_MINE = 5;
	AIGOAL_ATTACK = 6;
	#the hardcode has some types here that we don't need
	AIGOAL_CHASE = 11;

	statenames = ["IDLE", "GOTO", "FOLLOW", "EVADE", "CONSTRUCT", "MINE", "ATTACK", "", "", "", "", "CHASE"];
	
	def __init__(self, s, p=0):
		self.state = s;
		self.priority = p;
		if s == 0:
			self.priorityDelta = 0;
		else:
			self.priorityDelta = -1;
		self.targetLocation = vectors.Vec3(0,0,0);
		self.targetObject = None;
		self.timeLimit = 0;
		self.timeRepath = 0;

	def __str__(self):
		return "id: "+savage.Goal.statenames[self.state]+" pri: "+str(self.priority);

	def __eq__(self, b):
		if isinstance(b, savage.Goal) and b.state == self.state and b.priority == self.priority:
			return True;
		return False;


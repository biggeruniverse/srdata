# (c) 2011 savagerebirth.com

class TripAction(silverback.Action):
	def __init__(self, obj, dist):
		self.obj = obj;
		self.dist = dist;
		self.done = False;
		return silverback.Action.__init__(self);

	def run(self):
		objs = savage.getRadiusObjects(self.obj.objectId, self.dist);

		for obj in objs:
			if obj.getTeam() != self.obj.getTeam() and obj.getType().isUnitType():
				self.done = True;

	def is_done(self):
		return self.done;

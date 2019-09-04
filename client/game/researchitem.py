# (c) 2011 savagerebirth.com

import savage;

class ResearchItem:
	def __init__(self, objtype, builder, startTime, pct):
		self.objtype = savage.ObjectType(objtype);
		self.builder = builder;
		self.startTime = startTime;
		self.percentComplete = pct;
	
	def getType(self):
		return self.objtype;
	
	def getBuilder(self):
		return savage.getGameObject(self.builder);
	
	def __eq__(self, b):
		if not isinstance(b, self.__class__):
			return False;
		if isinstance(b, savage.ObjectType):
			return b == self.objtype;
		return b.objtype == self.objtype and b.builder == self.builder;
		
	def areTechRequirementsMet(self):
		#so here is the hard part!
		team = savage.Team(savage.getLocalPlayer().getTeam());
		
		builderAvailable = False;
		
		value = self.objtype.getValue("builder1");
		if value != "":
			reqtype = savage.getObjectType(value);
			for builder in team.getBuildings():
				if builder.getType() == reqtype and not builder.isBeingBuilt():
					builderAvailable = True;
					break;
				elif builder.getType() == self.objtype or self.objtype.getValue("selfBuild") == 1:
					builderAvailable = True;
					break;
		if self.objtype.getValue("selfBuild") == 1:
			builderAvailable = True;
					
		if value == "human_worker" or value == "beast_worker":
			builderAvailable = True;
		
		if builderAvailable == False:
			value = self.objtype.getValue("builder2");
			if value != "":
				reqtype = savage.getObjectType(value);
				for builder in team.getBuildings():
					if builder.getType() == reqtype and not builder.isBeingBuilt():
						builderAvailable = True;
						break;
						
		reqbasepoints = self.objtype.getValue("needBasePoints");		
		basepoints = team.getCommandCenter().getType().getValue("basePointValue");		

		if basepoints < reqbasepoints:
			builderAvailable = False;
					
		if builderAvailable == False:
			return False;	
		
		teamObjects = team.getAvailableTech();
		for b in ("requirement1","requirement2"):
			value = self.objtype.getValue(b);
			if value != "":
				reqtype = savage.getObjectType(value);
				if reqtype not in teamObjects:
					return False;
				else:
					if reqtype.isBuildingType():
						builderAvailable = False;
						for builder in team.getBuildings():
							if builder.getType() == reqtype and not builder.isBeingBuilt():
								builderAvailable = True;
								break;
		
		#does this cover everything?
		return builderAvailable;
		
	def areResourceRequirementsMet(self):	
		team = savage.Team(savage.getLocalPlayer().getTeam());
		teamRes = team.getResources(); #a dictionary of integers
		
		#yarr be entering stubby code now laddie! only for the brave! acch! Get me some haggis!
		for key, value in teamRes.items():
			cost = self.objtype.getCost(key);
			if cost > value and value != -1:
				#for a human team, entropy is -1
				#which is probably a silly idea, in hindsight should be 0 :P
				return False;	
		return True;
		
	def areRequirementsMet(self):
		return self.areResourceRequirementsMet() and self.areTechRequirementsMet();

	def getBuildProgress(self):
		return self.builder.getBuildProgress();

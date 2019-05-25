# (c) 2010 savagerebirth.com

import savage;

class Team:
	TECH_COLUMNS_HUMAN = ['NULL', 'magnetic', 'electric', 'chemical'];
	TECH_COLUMNS_BEAST = ['NULL', 'entropy', 'strata', 'fire'];
	#TODO if we were reducing hardcode, this is defined in some config iirc
	
	def __init__(self, tid):
		self.teamId = tid;
	
	def __str__(self):
		return "Team Object "+str(self.teamId)+" ("+self.getRace()+")";

	def __eq__(self, b):
		if isinstance(b, self.__class__):
			return b.teamId == self.teamId;
		elif isinstance(b, int):
			return b == self.teamId;
		return False;

	def getPlayers(self):
		players = savage.getPlayers();
		ret = [];
		for p in players:
			if p.getTeam() == self.teamId:
				ret.append(p);
		return ret;
		
	def getTechTypes(self):
		if self.getRace() == "human":
			return self.TECH_COLUMNS_HUMAN;
		elif self.getRace() == "beast":
			return self.TECH_COLUMNS_BEAST;
		else:
			return [];
		
	def getResearch(self):
		#what is currently being researched?
		return savage.team_getresearch(self.teamId);
	
	"""
	beard- so, a context should show a resarch button if it's available, requirements met or not
	it should be hidden if it's researched
	and it should be disabled if you're researching it? 
	big- yes unless you can make multiple, like workers or buildings (not SH/lair)
	"""
	
	def getResearchStatus(self, objtype):
		#0. can you actually research this?
		if objtype.getRace() != self.getRace():
			return None;
		
		#1. if the thing is already available, return Researched
		if objtype.getValue("alwaysAvailable") == 1:
			return Researched;
		
		if objtype in self.getResearch():
			return Researching;
		
		if objtype not in self.getAvailableTech():
			return Available;
		
		return Researched;
	
	def getUnits(self):
		#which units have been researched or are available?
		return savage.team_getunits(self.teamId);

	def getWeapons(self):
		#which weapons have been researched or are available?
		return savage.team_getweapons(self.teamId);

	def getItems(self):
		#which items have been researched or are available?
		return savage.team_getitems(self.teamId);

	def getBuildings(self):
		#returns the GameObject of every placed building belonging to the team
		#NB includes duplicates
		#NB includes in-construction buildings
		return savage.team_getbuildings(self.teamId);

	def getUpgrades(self):
		return savage.team_getupgrades(self.teamId);
	
	def getAvailableTech(self):
		return self.getUnits() + self.getWeapons() + self.getItems() + [o.getType() for o in self.getBuildings()];

	def getObjectsByType(self, typename):
		typeId = savage.getObjectType(typename).typeId;
		objs = savage.getTypeObjects(typeId);
		return [go for go in objs if go.getTeam() == self.teamId];

	def getResearchable(self):
		return savage.team_getresearchable(self.teamId);

	def getResearchableUnits(self):
		researchable = savage.team_getresearchable(self.teamId);
		units = [ typeobj for typeobj in researchable if typeobj.isUnitType()];
		sublist = [];
		for unit in units:
			if unit.getValue("alwaysAvailable") == 0 and not unit.isWorkerType():
				sublist.append(unit);
		return sublist;
	
	def getResearchableWeapons(self):
		researchable = savage.team_getresearchable(self.teamId);
		weapons = [ typeobj for typeobj in researchable if typeobj.isWeaponType() or typeobj.isMeleeType()];
		sublist = [];
		weaponsByTech = [[],[],[],[]];
		types = self.getTechTypes();
		
		for weapon in weapons:
			if weapon.getValue("alwaysAvailable") == 0:
				sublist.append(weapon);
		for weapon in sublist:
			type = weapon.getTechType();
			if type in types:
				weaponsByTech[ types.index(type) ].append(weapon);
		return weaponsByTech;
	
	def getResearchableItems(self):
		researchable = savage.team_getresearchable(self.teamId);
		items = [ typeobj for typeobj in researchable if typeobj.isItemType()];

		sublist = [];
		itemsByTech = [[],[],[],[]];
		types = self.getTechTypes();

		for item in items:
			if item.getValue("alwaysAvailable") == 0:
				sublist.append(item);
		for item in sublist:
			type = item.getTechType();
			if type in types:
				itemsByTech[ types.index(type) ].append(item);
		return itemsByTech;
	
	def getSpawnPoints(self):
		objs = savage.getActiveObjects();
		ret = [];
		for o in objs:
			if o.isSpawnPoint() and o.getTeam() == self.teamId:
				ret.append(o);
		return ret;

	def getCommandCenter(self):
		return savage.team_getcommandcenter(self.teamId);

	def getWinStatus(self):
		return savage.team_getwinstatus(self.teamId);
	
	def getRace(self):
		return savage.team_getrace(self.teamId);
	
	def getArmy(self):
		return savage.team_getarmy(self.teamId);
	
	def getNameColorCode(self):
		"""determines how the local player will view the team (ally, netural, enemy) and returns the corresponding color code"""
		player = savage.getLocalPlayer();
		if player.getTeam() == 0 or self.teamId == 0:
			return "^w"; #specs are see evertything as white, and everything sees specs as white
		elif player.getTeam() == self.teamId:
			return allyColorCode;
		else:
			return enemyColorCode;
		
	def getResources(self):
		return savage.team_getresources(self.teamId);
		"""for a human team, {"magnetic": 100, "electric": 55, "chemical": 0,
			"strata": -1, "entropy", -1, "fire": -1,
			"stone" : 1234, "gold": 50000}
		"""
	
	def getWorkerInfo(self):
		return savage.team_getworkerinfo(self.teamId);

	def getIdleWorkers(self):
		return savage.team_getidleworkers(self.teamId);
		
	def atMaxWorkers(self):
		working, total, max = self.getWorkerInfo();
		return total == max;
		
	def getKills(self):
		return savage.team_getkills(self.teamId);
	
	def getDeaths(self):
		return savage.team_getdeaths(self.teamId);

	def getAssists(self):
		return savage.team_getassists(self.teamId);

	def getUnitsInUse(self):
		unitDict = dict();
		count = 0;
		allUnits = [];
		for unit in self.getUnits() + self.getResearchableUnits():
			if unit not in allUnits:
				allUnits.append(unit);
		for ot in allUnits:  
			if ot.isUnitType() and not ot.isWorkerType():
				count = 0;
				for player in savage.getPlayers():
					if player.getType() == ot and not player.isCommander():
						count += 1;					
			unitDict[ot.getName()]=count;
		return unitDict;
	
	def getDeployedCount(self, tid):
		return savage.team_getdeployedcount(self.teamId, tid);


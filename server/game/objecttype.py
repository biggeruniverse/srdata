# (c) 2010 savagerebirth.com

import savage;

objclassNames = ["none", "weapon", "building", "unit", "item", "upgrade", 
			"melee", "dynamic", ""];

class ObjectType:
	def __init__(self, tid):
		self.typeId = tid;
		
	def __str__(self):
		return "Object Type for " +self.getName()+" (ID "+str(self.typeId)+")";

	def __eq__(self, b):
		if isinstance(b, self.__class__):
			return b.typeId == self.typeId;
		elif isinstance(b, int):
			return b == self.typeId;
		elif hasattr(b, "getType"):
			return b.getType().typeId == self.typeId;
		return False;

	def getValue(self, prop):
		return savage.ot_getpropertyvalue(self.typeId, prop);

	def getAttackTypeValue(self, atkName, atkProp):
		return savage.ot_getattackvalue(self.typeId, atkName, atkProp);

	def getName(self):
		return self.getValue("name");

	def getTechType(self):
		return savage.resourceNames[ self.getValue("techType") ] if self.getValue("techType") < len(savage.resourceNames) else None;
		
	def getObjectClass(self):
		try:
			objc = int(self.getValue("objclass"));
		except:
			objc = 0;
		return savage.objclassNames[objc];

	def getCost(self, resource):
		return savage.ot_getcost(self.typeId, resource);

	def isResearched(self):
		return savage.ot_isresearched(self.typeId);

	def isItemType(self):
		if self.getObjectClass() == "item":
			return True;
		return False;
		
	def isWeaponType(self):
		if self.getObjectClass() == "weapon":
			return True;
		return False;
	
	def isBuildingType(self):
		if self.getObjectClass() == "building":
			return True;
		return False;

	def isUnitType(self):
		if self.getObjectClass() == "unit":
			return True;
		return False;

	def isMeleeType(self):
		if self.getObjectClass() == "melee":
			return True;
		return False;

	def isWorkerType(self):
		if self.isUnitType() == False:
			return False;

		return self.getValue("isWorker") == 1;

	def isCharacterType(self):
		if self.isUnitType() and self.getValue("isVehicle") != 1:
			return True;
		return False;

	def isWeaponType(self):
		if self.getObjectClass() == "weapon":
			return True;
		return False;
	
	def isManaWeapon(self):
		return self.isWeaponType() and self.getValue("useMana") == 1;

	def isSiegeType(self):
		if self.isUnitType() and self.getValue("isVehicle") == 1:
			return True;
		return False;

	def isNPCType(self):
		if self.isUnitType() and self.getName().find("npc_") == 0:
			return True;
		return False;

# (c) 2010 savagerebirth.com
# this is the client wrapper object to interact with clients

import savage;
import math;
from vectors import Vec3;

class Player(GameObject):
	def __init__(self, oid):
		savage.GameObject.__init__(self, oid);
		
	def __str__(self):
		return "Player Object for "+self.getName()+" (object Id "+str(self.objectId)+")";
		
	def getUID(self):
		return savage.player_getuid(self.objectId);

	def getClanID(self):
		return savage.player_getclanid(self.objectId);
	
	def getClanIcon( self, padding=False ):
		cid = self.getClanID();
		if cid == 0:
			return "^icon transparent^" if padding else "";
		return "^clan " + str(cid) + "^";
	
	def getClanTag(self): #^900DA for example
		return ""; #TODO
	
	def getFormattedName(self, padding=False):
		return self.getClanTag() + "^w" + self.getClanIcon(padding) + self.getName();
	
	def getStatusIcon(self, padding=False):
		if self.isCommander():
			return "^icon ../../gui/standard/icons/comm_crown.s2g";
		elif self.isOfficer():
			return "^icon ../../models/human/items/icons/officer1.s2g";
		elif padding:
			return "^icon transparent^";
		else:
			return "";
	
	def getMana(self):
		return savage.player_getmana(self.objectId);
	
	def getMaxMana(self):
		return self.getType().getValue("maxMana");
	
	def getStamina( self):
		return savage.player_getstamina(self.objectId);
	
	def getMaxStamina( self):
		return savage.player_getmaxstamina(self.objectId);
		
	def getStaminaPct(self):
		max = self.getMaxStamina();
		if max != 0:
			return self.getStamina() / float( self.getMaxStamina() );
		else:
			return 0;
	
	def getXp( self):
		return savage.player_getxp(self.objectId);

	def getLevel(self):
		return savage.player_getlevel(self.objectId);
		
	def getKills(self):
		return savage.player_getkills(self.objectId);

	def getDeaths(self):
		return savage.player_getdeaths(self.objectId);

	def getAssists(self):
		return savage.player_getassists(self.objectId);

	def getKillsPerWeapon(self):
		return savage.player_getkillsperweapon(self.objectId);

	def getDeathsPerWeapon(self):
		return savage.player_getdeathsperweapon(self.objectId);

	def getInventorySlot(self, slot):
		#returns an ObjectType or None
		return savage.player_getinventoryslot(self.objectId, slot);

	def getInventorySlotAmmo(self, slot):
		return savage.player_getinventoryslotcount(self.objectId, slot);

	def getCurrentInventorySlotIndex(self):
		return savage.player_getcurrentinventoryslotindex(self.objectId);
		
	def getStatus(self):
		return savage.player_getstatus(self.objectId);

	def getAmmoSlot(self, slot):
		#returns an integer or None if ammo isn't applicable
		return savage.player_getammo(self.objectId, slot);
	
	def getManaUsesSlot( self, slot, basedOnMax=False):
		#returns an integer representing the number of uses of the weapon remain
		#or None if mana isn't applicable
		#if max is true it's based on max mana, if max is false it's based on current mana
		slot_objType = self.getInventorySlot(slot);
		mana = self.getMana() if not basedOnMax else self.getMaxMana();
		cost = slot_objType.getValue("manaCost");
		if slot_objType.isManaWeapon() and cost != 0:
			return mana // cost;
		elif slot_objType.isManaWeapon() and cost == 0:
			return 999; #consider it an approximation to infinity :P
		else:
			return 0;

	def getGold( self):
		return savage.player_getgold(self.objectId);
		#can we make it return "" or None if we're a spectator who's not spectating anyone?

	def getLink(self):
		return savage.player_getlink(self.objectId);

	def getRespawnTime(self):
		return savage.player_getrespawntime(self.objectId);

	def isPlayer(self):
		return True;

	def isCommander(self):
		return savage.player_iscommander(self.objectId);

	def isOfficer(self):
		return savage.player_isofficer(self.objectId);
	
	def isReferee( self):
		return savage.player_isreferee(self.objectId);
	
	def getPing(self):
		return savage.player_getping(self.objectId);

	def getAccuracy(self, race=0):
		if race == 0:
			race = self.getType().getValue("race");
		return [savage.player_getfiredshots(self.objectId, race), savage.player_gethitshots(self.objectId, race), savage.player_getsiegehitshots(self.objectId, race)];

	def getWaypointDistance(self):
		return savage.player_getwaypointdistance(self.objectId);

	def getDuelingPhase(self):
		return savage.player_getduelphase(self.objectId);

	def getDueling(self):
		return savage.player_getdueling(self.objectId);

	def getIdleTime(self):
		return savage.player_getidletime(self.objectId);

	def getAutoApproved(self):
		return savage.player_getautoapprove(self.objectId);

	def getFocus(self):
		return savage.player_getfocus(self.objectId);

	def getSkin(self):
		return savage.player_getskin(self.objectId);

	### Manipulators ###
	
	def giveStamina(self, amount):
		pass;

	def giveMana(self, amount):
		pass;

	def giveAmmo(self, amount, basis):
		return savage.player_giveammo(self.objectId, amount, basis);

	def giveItem(self, itemtype, slot=-1):
		savage.player_giveitem(self.objectId, itemtype.typeId, slot);
		return itemtype;
	
	def stun(self, duration):
		return savage.player_stun(self.objectId, duration);

	def drop(self, objtype, angle, radius):
		#shouldn't this be in GameObject?
		ob = savage.go_spawn(objtype, self.objectId);

		f = self.getForwardVector();
		p = self.getPosition();
		forwardAngle = math.atan2( f[1] , f[0] );
		angle = math.radians( angle );
		angle += forwardAngle + math.pi/4.0;
		p += [ radius*math.cos(angle), radius*math.sin(angle), 5];
		ob.setPosition( p );
		savage.fallToCollide(ob.objectId);
		ob.onDrop();
		return ob;

	def toss(self, objtype, speed, gravity):
		ob = savage.go_spawn(objtype, self.objectId);

		f = Vec3(self.getForwardVector());
		f.normalise();
		f = f * speed;

		ob.setTrajectory(f.data);
		ob.setGravity(gravity);

		ob.onToss(self);
		return ob;

	def revive(self, health):
		return savage.player_revive(self.objectId, health);

	def switchInventorySlot(self, slot):
		return savage.player_invswitch(self.objectId, slot);

	def scrollInventorySlot(self, slot):
		return savage.player_invinc(self.objectId, slot);

	def teleport(self, to):
		p = self.getPosition(); # the fallback is to go nowhere
		if isinstance(to, Vec3):
			p = to;
		elif isinstance(to, savage.GameObject):
			p = to.getPosition();
			p = Vec3(silverback.SV_GetSpawnPointAroundObject(to.objectId, self.objectId));
		self.setPosition(p);

	def setLink(self, l):
		return savage.player_setlink(self.objectId, l.objectId);

	def makeOfficer(self):
		return savage.player_makeofficer(self.objectId);

	def demoteOfficer(self):
		return savage.player_demoteofficer(self.objectId);

	def makeCommander(self):
		return savage.player_makecommander(self.objectId, 1);

	def setDuelingPhase(self, i):
		return savage.player_setduelphase(self.objectId, i);

	def setDueling(self, t):
		return savage.player_setdueling(self.objectId, t);

	def clearInventory(self):
		return savage.player_clearinventory(self.objectId);

	def setAutoApprove(self, yes=1):
		return savage.player_setautoapprove(self.objectId, yes);

	### Callbacks ###
	def onUnitSelect(self):
		pass;

	def onSpawn(self,target):
		pass;

	def onLevelUp(self):
		pass;

	def onWounded(self, inflictor, amt):
		pass;


def getLocalPlayer():
	return savage.Player( savage.getLocalId() );

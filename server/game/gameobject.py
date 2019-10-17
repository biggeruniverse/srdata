# (c) 2010 savagerebirth.com

#A basic game object wrapper class

import savage;
import math;
from vectors import Vec3;

class GameObject:
	def __init__(self, oid):
		self.objectId = oid;
		
	def __str__(self):
		return "Game Object with ID " +str(self.objectId);

	def __eq__(self, b):
		if isinstance(b, self.__class__):
			return b.objectId == self.objectId;
		return False;

	def __hash__(self):
		return hash(self.objectId);

	def getType(self):
		return savage.go_gettype(self.objectId);
	
	def isActive(self):
		return savage.go_isactive(self.objectId);

	def isPlayer(self):
		return False;

	def isSelected(self):
		return savage.go_isselected(self.objectId);

	def getHealth(self):
		return savage.go_gethealth(self.objectId);

	def getMaxHealth(self):
		return savage.go_getmaxhealth(self.objectId);
	
	def getHealthPct(self):
		maxhp = self.getMaxHealth();
		if maxhp > 0:
			return self.getHealth() / float(maxhp);
		else:
			return 0;
	
	def isBeingBuilt(self):
		if self.getType().isBuildingType():
			return savage.go_isbeingbuilt(self.objectId);
		return False;
	
	#returns a float, 0 no construction, 1 full construction
	def getBuildProgress(self):
		return savage.go_getbuildprogress(self.objectId);
		
	def construct(self, who, amt):
		return savage.go_construct(who, self.objectId, amt);
		
	def getTeam(self):
		return savage.go_getteam(self.objectId);

	def getName(self):
		return savage.go_getname(self.objectId);

	def getNameColorCode(self):
		#determines how the local player will view the object (ally, netural, enemy) and returns the corresponding color code
		player = savage.getLocalPlayer();
		if player.getTeam() == 0 or self.getTeam() == 0:
			return "^w"; #specs are see evertything as white, and everything sees specs as white
		elif player.getTeam() == self.getTeam():
			return allyColorCode;
		else:
			return enemyColorCode;
		
	def getIcon(self):
		icon = self.getType().getValue("icon");
		return icon+".s2g";

	def getMapIcon(self):
		icon = self.getType().getValue("mapIcon");
		return icon;

	def getSelectionIcon(self):
		icon = self.getType().getValue("selectionIcon");
		return icon;

	def getPosition(self):
		return savage.go_getposition(self.objectId);

	def getScreenTopPosition(self):
		return savage.go_getscreentopposition(self.objectId);

	def getForwardVector(self):
		return savage.go_getforward(self.objectId);

	def isSpawnPoint(self):
		return savage.go_isspawn(self.objectId);

	def isComplete(self):
		return self.getBuildProgress() >= 1.0;

	def getState(self, slot):
		return savage.go_getstate(self.objectId, slot);

	def getStateList(self):
		return savage.go_getstates(self.objectId);

	def getOwner(self):
		return savage.getGameObject(savage.go_getowner(self.objectId));

	def getPrimaryAnimState(self):
		return savage.go_getanimstate(self.objectId, 1);

	def getSecondaryAnimState(self):
		return savage.go_getanimstate(self.objectId, 2);

	def getRadiusSq(self):
		return savage.go_getradiussq(self.objectId);

	def getRadius(self):
		import math;
		return math.sqrt(savage.go_getradiussq(self.objectId));

	def getCarryResource(self, r):
		return savage.go_getresource(self.objectId, r);

	def getMaxCarryResource(self, r):
		return savage.go_getmaxresource(self.objectId, r);

	def getCapacity(self, r):
		return savage.go_getcapacity(self.objectId, r);

	def getAzimuthTo(self, t):
		return savage.go_getazimuthto(self.objectId, t.objectId);

	### Manipulators ###
	def setType(self, n):
		return savage.go_settype(self.objectId, n);

	def setPosition(self, p):
		return savage.go_setposition(self.objectId, p[0], p[1], p[2]);

	def setTrajectory(self, t):
		return savage.go_settrajectory(self.objectId, t[0], t[1], t[2]);

	def setGravity(self, g):
		return savage.go_setgravity(self.objectId, g);

	def setHealth( self, h ):
		if self.getHealth() <= 0:
			return 0;
		#go_sethealth returns the amount that health actually changed
		return savage.go_sethealth(self.objectId, h);

	def setForwardVector(self, v):
		return savage.go_setforward(self.objectId, v[0], v[1], v[2]);

	def setTeam(self, t):
		return savage.go_setteam(self.objectId, t);

	def heal( self, h ):
		return self.setHealth( h );

	def healPct(self, p):
		return self.heal( int(p*self.getMaxHealth()) );
	
	def damage( self, target, d, flags=0 ):
		if target.getHealth() <= 0:
			return 0;
		amt = savage.go_damage(self.objectId, target.objectId, self.getType().typeId, d, flags);
		return amt;
	
	def damageFalloff( self, target, maxdamage, maxrange, flags=0):
		import math;
		v0 = Vec3( self.getPosition() );
		v1 = Vec3( target.getPosition() );
		x = max(0, v0.distanceTo( v1 )-target.getRadius());
		
		if x > maxrange: damage = 0;
		else: damage = maxdamage * math.cos( x*math.pi*0.5/maxrange );
		#since 0.5 is a float, python won't truncate the quotient
		self.damage( target, damage, flags|DAMAGE_SPLASH );
	
	def damagePct( self, target, p, flags=0 ):
		return self.damage( target, p*target.getMaxHealth(), flags );
		
	def die(self):
		return savage.go_die(self.objectId);
		
	def push(self, x, y, z):
		return savage.go_push(self.objectId, x, y, z);

	def addEvent(self, event):
		return savage.go_addevent(self.objectId, event);

	def addState(self, who, st_name, duration):
		whoid=self.objectId;
		if who != None:
			whoid = who.objectId
		return savage.go_givestate(whoid, self.objectId, st_name, duration);

	def setState(self, st_name):
		return savage.go_setstate(self.objectId, st_name);

	def addStateTime(self, name, secs):
		return savage.go_addstatetime(self.objectId, name, secs);

	def attach(self, attache):
		return savage.go_attach(self.objectId, attache.objectId);

	def setPrimaryAnimState(self, st):
		return savage.go_setanimstate(self.objectId, 1, st);

	def setSecondaryAnimState(self, st):
		return savage.go_setanimstate(self.objectId, 2, st);

	def select(self):
		if self.isSelected():
			return True;
		return CL_SelectObject(self.objectId);

	def unselect(self):
		return CL_UnselectObject(self.objectId);

	### Callbacks ###
	def onPickup(self, target):
		pass;

	def onDrop(self):
		pass;

	def onToss(self, tosser): #heh
		pass;

	def onDamaged(self, target, amt):
		pass;

	def onDeath(self, killer):
		pass;

	def onDestroy(self):
		pass;

	def onSpawn(self, target):
		pass;

	def onActivate(self, target):
		pass;

	def onIdle(self, target):
		pass;

	def onSleep(self, target):
		pass;

	def onUse(self, user, target):
		pass;

	def onImpact(self, target):
		pass;

	def onFuseEnd(self):
		pass;

	def onBackfire(self, owner):
		pass;

	def onAttach(self, to):
		pass;

	def onWounded(self, attacker, dmg):
		pass;

	def onPushed(self, whoby):
		pass;

	def commandPosition(self, whofrom, goal, x, y):
		pass;

	def commandTarget(self, whofrom, goal, obj):
		pass;


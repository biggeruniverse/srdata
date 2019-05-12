# (c) 2011 savagerebirth.com
from vectors import Vec3;

class AttackState(savage.FSMState):
	def __init__(self, o):
		savage.FSMState.__init__(self);
		self.attackTime = 0
		self.impactTime = 0
		self.impacted = False
		self.attackStarted = False
		self.targetObject = o;

	def isAttackAnim(self, attack):
                return (attack > 0 and attack < 11)

	def run(self):
		go = self.machine.mind;
		gotype = go.getType();
		attackName = "melee_1";

		go.setPrimaryAnimState(AnimStates.AS_IDLE)

                weapon = gotype.getValue("forceInventory0")
		isRanged = False
                if not weapon is None:
                        weaponType = savage.getObjectType(weapon)
                        if weaponType.getObjectClass() == "weapon":
                                isRanged = True

		isSuicide = M_Randnum(0, 100) < 100*gotype.getValue("attackSuicideChance");
		if isSuicide:
			attackName = "melee_1";

                if isRanged:
                        r = 400.0
                else:
                        r = gotype.getAttackTypeValue(attackName, "range");
                r2 = r ** 2
                p = Vec3(go.getPosition());
                o = Vec3(self.targetObject.getPosition());
		
                go.setForwardVector( o - p ); # always face target

                if not self.attackStarted:
                        if o.distanceSqTo(p) > r2:
                                go.fsm.insertState(savage.ChaseState(self.targetObject, r));
                                return
                        self.attackTime = savage.getGameTime() + gotype.getAttackTypeValue(attackName, "time")
                        self.impactTime = savage.getGameTime() + gotype.getAttackTypeValue(attackName, "impact")
			if isSuicide:
				go.setSecondaryAnimState(AnimStates.AS_SUICIDE);
			else:
                        	go.setSecondaryAnimState(AnimStates.AS_MELEE_1);
                        self.impacted = False
                        self.attackStarted = True

                if self.impactTime <= savage.getGameTime() and not self.impacted:
                        #make the attack
                        if isRanged:
				go.fireWeapon(o);
                                go.setSecondaryAnimState(AnimStates.AS_IDLE)
                        else:
				if isSuicide:
					go.addEvent(33);    #there's a whole lot of events, I'm not putting them all in defines.py
					objs = savage.getRadiusObjects(go.objectId, 150);
					for obj in objs:
						go.damageFalloff(obj, gotype.getValue("attackSuicideDamage"), gotype.getValue("attackSuicideRadius"));
					go.damage(go, go.getMaxHealth()+10);
				else:
                                	go.damage(self.targetObject, gotype.getAttackTypeValue(attackName, "damage"));
                        self.impacted = True

		if self.attackTime <= savage.getGameTime():
                        go.setSecondaryAnimState(AnimStates.AS_IDLE)
                        self.attackStarted = False

	def isComplete(self):
		go = self.machine.mind;
		if self.targetObject == None or self.targetObject.getHealth() <= 0 or not self.targetObject.isActive():
			go.setSecondaryAnimState(AnimStates.AS_IDLE);
			#con_println('^rwtf\n') # wtf?
			return True;
		return False;

	def canTransition(self, s):
		if isinstance(s, savage.IdleState):
			return True;
		if isinstance(s, savage.ChaseState):
			return True;

		if isinstance(s, savage.ReturnState):
			return True;
		#if isinstance(s, RoamState):
		#	return True;
		return False;


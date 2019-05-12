#(c) 2012 savagerebirth.com
from silverback import *;
import savage;

autoItem = { 'human' : ["human_medkit", "human_medkit", "human_medkit"], 'beast' : ["beast_rabid"]};

def handleDuelChallenge(c, t):
	target = None;
	challenger = savage.getGameObject(c);
	
	#Mode logic
	if t == -1:
		if challenger.getDuelingPhase() == DP_READY:
			challenger.setDuelingPhase(DP_NOTDUELING);
			silverback.SV_ClientEcho(c, "^gNow in FFA mode\n");
		elif challenger.getDuelingPhase() == DP_CHALLENGING:
			silverback.SV_ClientEcho(c, "^cYou have cancelled your challenge!\n");
			silverback.SV_ClientEcho(t, "^c"+challenger.getName()+" ^chas cancelled their challenge!\n");
			challenger.setDuelingPhase(DP_READY);
		elif challenger.getDuelingPhase() == DP_DUELING:
			pass; #TODO: forfiet!
		else:
			challenger.setDuelingPhase(DP_READY);
			silverback.SV_ClientEcho(c, "^gNow in DUEL mode\n");
			challenger.setDueling(-1);
		
		return;
	
	#now we can get our target, since we know we have one
	target = savage.getGameObject(t);
	
	if challenger.getDuelingPhase() == DP_NOTDUELING:
		silverback.SV_ClientEcho(c, "^cYou are currently in ^gFFA ^cmode.  Aim at the ground and use your officer command (default: ^yF^c)!\n");
		return;
	
	#Other guy is switched off
	if target.getDuelingPhase() == DP_NOTDUELING:
		silverback.SV_ClientEcho(c, "^rThis person is not in duel mode!\n");
		return;

	#reminders and cancel
	if challenger.getDueling() > -1:
		if challenger.getDueling() == t and challenger.getDuelingPhase() == DP_CHALLENGING:
			silverback.SV_ClientEcho(t, "^c"+challenger.getName()+" ^greminds you of his/her challenge!\n");
			silverback.SV_ClientEcho(c, "^gYou have reminded ^c"+target.getName()+" ^gof your challenge!\n");
			if cvar_getvalue("sv_duelwaypoints") > 0:
				challenger.targetObject(t, GOAL_ATTACK_OBJECT);
				
		elif challenger.getDuelingPhase() == DP_CHALLENGING and target.getDuelingPhase() != DP_DUELING:
			silverback.SV_ClientEcho(t, "^c"+challenger.getName()+" ^ghas cancelled the challenge.\n");
		return;

	#let's do this!
	if target.getDueling() > -1:
		if target.getDueling() == challenger.objectId:
			#CHALLENGE ACCEPTED!
			target.setDuelingPhase(DP_DUELING);
			challenger.setDueling(t);
			challenger.setDuelingPhase(DP_DUELING);
			silverback.SV_ClientEcho(t, "^c"+challenger.getName()+" ^ghas accepted your challenge!\n");
			silverback.SV_ClientEcho(c, "^gYou have accepted ^c"+target.getName()+"'s ^gchallenge!\n");
			
			if cvar_getvalue("sv_duelautoheal")>0:
				challenger.setHealth(challenger.getMaxHealth());
				target.setHealth(target.getMaxHealth());
			
			target.clearInventory();
			challenger.clearInventory();
			
			if cvar_getvalue("sv_duelautoitem")>0:
				team = savage.Team(target.getTeam());
				for typeName in duels.autoItem[team.getRace()]:
					obj = savage.getObjectType(typeName);
					if obj.isMeleeType():
						target.giveItem(obj, 0);
					else:
						target.giveItem(obj);

				team = savage.Team(challenger.getTeam());
				for typeName in duels.autoItem[team.getRace()]:
					obj = savage.getObjectType(typeName);
					if obj.isMeleeType():
						challenger.giveItem(obj, 0);
					else:
						challenger.giveItem(obj);
			return;
		elif target.getDualingPhase() > DP_READY:
			silverback.SV_ClientEcho(c, "^cThis player is already engaged in combat!\n");
			return;
	
	silverback.SV_ClientEcho(c, "^gYou have challenged ^c"+target.getName()+" ^gto a duel!\n");
	silverback.SV_ClientEcho(t, "^c"+challenger.getName()+" ^ghas challenged you to a duel!\n");
	challenger.setDuelingPhase(DP_CHALLENGING);
	challenger.setDueling(t);
	

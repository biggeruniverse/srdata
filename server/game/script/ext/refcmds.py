#(c) 2011 savagerebirth.com

from silverback import *;
import savage;

playerArgNote = "\nNote: <player> may be a player name or a client ID preceded by a #"
typeArgNote = "\nNote: <type> may be the name of any NPC, e.g. \"monkit\""

def getClientIDFromString(string):
	if len(string) == 0:
		return None
	ret = savage.getPlayerByName(string)
	if ret is None and string[0] == '#':
		try:
			ret = int(string[1:])
			ret = savage.getGameObject(ret)
		except:
			return None

	elif ret is None:
		ret = savage.getPlayerByName(string.lower());

	return ret

class RefereeCommandHandler(savage.CommandHandler):
	def __init__(self):
		self.description = "";
		self.cmd = "none";
		

	def handle(self, clientId, args):
		pass;

class RefKick(savage.RefereeCommandHandler):
	DESCRIPTION = "ref kick <player>";
	CMD = "kick";
	GROUPS = ["full"]
	def __init__(self):
		pass;

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, 'Usage: ' + self.DESCRIPTION + savage.playerArgNote)
			return
		slayed = savage.getClientIDFromString(args[0]);
		ref = savage.getGameObject(clientId);

		if slayed is None or not slayed.isActive():
			silverback.SV_ClientEcho(clientId, "Player not found")
		else:
			silverback.Server_KickClient(slayed.objectId, "refkick");

			silverback.SV_BroadcastNotice("^900Referee "+ref.getName()+" kicked "+slayed.getName());

class RefSlay(savage.RefereeCommandHandler):
	DESCRIPTION = "ref slay <player>";
	CMD = "slay";
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass;

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, 'Usage: ' + self.DESCRIPTION + savage.playerArgNote)
			return
		slayed = savage.getClientIDFromString(args[0]);
		ref = savage.getGameObject(clientId);

		if slayed is None or not slayed.isActive():
			silverback.SV_ClientEcho(clientId, "Player not found")
		else:
			slayed.die();

			silverback.SV_BroadcastNotice("^900Referee "+ref.getName()+" slayed "+slayed.getName());

class RefMorph(savage.RefereeCommandHandler):
	DESCRIPTION = "ref morph <player> <type>";
	CMD = "morph";
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass;
	
	def handle(self, clientId, args):
		if len(args) < 2:
			silverback.SV_ClientEcho(clientId, 'Usage: ' + self.DESCRIPTION + savage.playerArgNote + savage.typeArgNote)
			return
		typename = "npc_"+args[1];
		target = savage.getClientIDFromString(args[0]);
		typeobj = savage.getObjectType(typename);
		ref = savage.getGameObject(clientId);

		if target is not None and target.isActive() and typeobj is not None:
			target.setType(typename);
			target.giveItem(savage.getObjectType("beast_stalker_melee"), 0);
			silverback.SV_BroadcastNotice("^900Referee "+ref.getName()+" has turned "+target.getName()+" into a "+typeobj.getValue('description')+"!");

class RefWorld(savage.RefereeCommandHandler):
	DESCRIPTION = "ref changemap <worldname>";
	CMD = "changemap";
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass;
	
	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, 'Usage: ' + self.DESCRIPTION)
			return
		world = args[0];
		ref = savage.getGameObject(clientId);
		silverback.SV_BroadcastNotice("^900Referee "+ref.getName()+" changed map to "+world);
		silverback.cvar_set("sv_playerChosenMap", world);
		savage.setGameStatus(GAME_STATUS_PLAYERCHOSENMAP);

class RefNextMap(savage.RefereeCommandHandler):
	DESCRIPTION = "ref nextmap";
	CMD = "nextmap";
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass;
	
	def handle(self, clientId, args):
		ref = savage.getGameObject(clientId);
		silverback.SV_BroadcastNotice("^900Referee "+ref.getName()+" forced next map");
		savage.setGameStatus(GAME_STATUS_NEXTMAP);

class RefRestartMatch(savage.RefereeCommandHandler):
	DESCRIPTION = "ref restartmatch"
	CMD = "restartmatch"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		ref = savage.getGameObject(clientId)
		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has restarted the match!")
		silverback.SV_RestartMatch()

class RefStartMatch(savage.RefereeCommandHandler):
	DESCRIPTION = "ref startmatch"
	CMD = "startmatch"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if savage.getGameStatus() == GAME_STATUS_NORMAL:
			silverback.SV_ClientEcho(clientId, "^yThe match has already started!")
			return
		
		ref = savage.getGameObject(clientId)
		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has started the match!")
		silverback.SV_StartMatch()

class RefStopVote(savage.RefereeCommandHandler):
	DESCRIPTION = "ref stopvote"
	CMD = "stopvote"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		ref = savage.getGameObject(clientId)
		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has stopped a vote!")
		silverback.SV_StopVote()

class RefSetRace(savage.RefereeCommandHandler):
	DESCRIPTION = "ref setrace <team> <race>"
	CMD = "setrace"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) < 2:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION)
			return
		
		ref = savage.getGameObject(clientId)
		try:
			team = int(args[0])
		except:
			return
		
		if savage.Team(team).setRace(args[1]):
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has set team " + str(team) + " to ^g" + args[1] + "^900!")

class RefImpeach(savage.RefereeCommandHandler):
	DESCRIPTION = "ref impeach <team>"
	CMD = "impeach"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION)
			return

		ref = savage.getGameObject(clientId)
		try:
			team = int(args[0])
		except:
			return

		comm = savage.Team(team).getCommander()
		if comm is None:
			return
		
		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " ^gimpeached ^900" + comm.getName() + "!")
		savage.Team(team).impeachCommander()

class RefSetCommander(savage.RefereeCommandHandler):
	DESCRIPTION = "ref setcmdr <player>"
	CMD = "setcmdr"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION + savage.playerArgNote)
			return

		ref = savage.getGameObject(clientId)
		target = savage.getClientIDFromString(args[0])

		if target is None:
			silverback.SV_ClientEcho(clientId, "Player not found")
		elif target.makeCommander():
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " ^yhas made ^900" + target.getName() + " ^ythe commander of team " + str(target.getTeam()) + "!")

class RefPromote(savage.RefereeCommandHandler):
	DESCRIPTION = "ref promote <player>"
	CMD = "promote"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION + savage.playerArgNote)
			return

		ref = savage.getGameObject(clientId)
		target = savage.getClientIDFromString(args[0])

		if target is None:
			silverback.SV_ClientEcho(clientId, "Player not found")
		elif target.makeOfficer():
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " ^has made ^900" + target.getName() + " ^yan officer of team " + str(target.getTeam()) + "!")

class RefDemote(savage.RefereeCommandHandler):
	DESCRIPTION = "ref demote <player>"
	CMD = "demote"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION + savage.playerArgNote)
			return

		ref = savage.getGameObject(clientId)
		target = savage.getClientIDFromString(args[0])

		if target is None:
			silverback.SV_ClientEcho(clientId, "Player not found")
		elif target.isOfficer():
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " ^yhas demoted ^900" + target.getName() + " ^yas officer of team" + str(target.getTeam()) + "!")
			target.demoteOfficer()

class RefMute(savage.RefereeCommandHandler):
	DESCRIPTION = "ref mute <player>"
	CMD = "mute"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION + savage.playerArgNote)
			return

		ref = savage.getGameObject(clientId)
		target = savage.getClientIDFromString(args[0])

		if target is None:
			silverback.SV_ClientEcho(clientId, "Player not found")
		elif silverback.SV_Mute(target.objectId):
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " ^yhas muted ^900" + target.getName() + "^y!")

class RefUnMute(savage.RefereeCommandHandler):
	DESCRIPTION = "ref unmute <player>"
	CMD = "unmute"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION + savage.playerArgNote)
			return

		ref = savage.getGameObject(clientId)
		target = savage.getClientIDFromString(args[0])

		if target is None:
			silverback.SV_ClientEcho(clientId, "Player not found")
		elif silverback.SV_UnMute(target.objectId):
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " ^yhas unmuted ^900" + target.getName() + "^y!")

class RefPause(savage.RefereeCommandHandler):
	DESCRIPTION = "ref pause"
	CMD = "pause"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		ref = savage.getGameObject(clientId)
		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " paused the game!")
		silverback.SV_Pause()

class RefUnpause(savage.RefereeCommandHandler):
	DESCRIPTION = "ref unpause"
	CMD = "unpause"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		ref = savage.getGameObject(clientId)
		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " unpaused the game!")
		silverback.SV_Unpause()

class RefSwitchTeam(savage.RefereeCommandHandler):
	DESCRIPTION = "ref switchteam <toteam> <player>"
	CMD = "switchteam"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) < 2:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION + savage.playerArgNote)
			return
		
		ref = savage.getGameObject(clientId)
		try:
			team = int(args[0])
		except:
			return
		target = savage.getClientIDFromString(args[1])

		if target is None:
			silverback.SV_ClientEcho(clientId, "Player not found")
		else:
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " ^ymoved ^900" + target.getName() + " ^yto team " + str(team) + "!")
			target.setTeam(team)

class RefTime(savage.RefereeCommandHandler):
	DESCRIPTION = "ref time <milliseconds>"
	CMD = "time"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		ref = savage.getGameObject(clientId)
		time = 600000 # default 10 minutes
		if len(args) > 0:
			try:
				time = int(args[0])
			except:
				pass

		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has extended the time limit by " + str(float(time) / 1000.0) + " seconds!")
		silverback.SV_ExtendTime(time)

class RefSetTime(savage.RefereeCommandHandler):
	DESCRIPTION = "ref settime <milliseconds>"
	CMD = "settime"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		if len(args) == 0:
			silverback.SV_ClientEcho(clientId, "Usage: " + self.DESCRIPTION)
			return

		ref = savage.getGameObject(clientId)
		try:
			time = int(args[0])
		except:
			return

		silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has set the time limit to " + str(float(time) / 1000.0) + " seconds!")
		silverback.SV_SetTime(time)

class RefShuffle(savage.RefereeCommandHandler):
	DESCRIPTION = "ref shuffle"
	CMD = "shuffle"
	GROUPS = ["normal", "full"]
	def __init__(self):
		pass

	def handle(self, clientId, args):
		ref = savage.getGameObject(clientId)
		if savage.getGameStatus() <= GAME_STATUS_WARMUP:
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has shuffled the teams!")
		else:
			silverback.SV_BroadcastNotice("^900Referee " + ref.getName() + " has evened the teams!")

		silverback.SV_ShuffleTeams()

#register all handlers
savage.registerRefCommand(RefKick);
savage.registerRefCommand(RefSlay);
savage.registerRefCommand(RefMorph);
savage.registerRefCommand(RefWorld);
savage.registerRefCommand(RefNextMap);
savage.registerRefCommand(RefRestartMatch);
savage.registerRefCommand(RefStartMatch);
savage.registerRefCommand(RefStopVote);
savage.registerRefCommand(RefSetRace);
savage.registerRefCommand(RefImpeach);
savage.registerRefCommand(RefSetCommander);
savage.registerRefCommand(RefPromote);
savage.registerRefCommand(RefDemote);
savage.registerRefCommand(RefMute);
savage.registerRefCommand(RefUnMute);
savage.registerRefCommand(RefPause);
savage.registerRefCommand(RefUnpause);
savage.registerRefCommand(RefSwitchTeam);
savage.registerRefCommand(RefTime);
savage.registerRefCommand(RefSetTime);
savage.registerRefCommand(RefShuffle);

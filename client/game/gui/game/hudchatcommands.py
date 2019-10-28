# copyright (c) 2011 savagerebirth.com
# this file defines command shorthands for the HUDChatBox

from silverback import *;
import sys;

#define a function - its name will be the command name
#it must accept HCB and args, which represent the HUDChatBox instance and the command arguments, respectively
#if the command returns something other than None, then str(the return value) will be added to the HUDChatBox
#TODO modding 'api' to add commands without modifying this file

def _printToHCB( toPrint, console = False ):
	#for printing more than one thing at a time
	if toPrint == None:
		return;
	toPrint = str(toPrint);
	gblEventHandler.notifyEvent( "_HCBinternal", "", toPrint );
	if console:
		con_println( toPrint + "\n");

def w( HCB, args ):
	"""Send a private message
	
	/w target message
	target - name of the intended recipient
	message - message to send, can include spaces"""
	if len(args) < 2:
		return None;
	message = " ".join(args[1:]);
	CL_SendChat( message, "private", args[0]);
	Sound_PlaySound("/sound/gui/msg_send.ogg");
	return privColorCode + "-> " + args[0] + " " + message;

def msg( HCB, args):
	"""Send a private message
	
	/msg target message
	target - name of the intended recipient
	message - message to send, can include spaces"""
	return hudchatcommands.w(HCB, args);

def r(HCB, args):
	"""Send a private message to the person who last sent you a private message
	
	/r message
	message - message to send, can include spaces"""
	if len(args) < 1:
		return None;
	message = " ".join(args);
	CL_SendChat( message, "private", HCB.replyTarget);
	Sound_PlaySound("/sound/gui/msg_send.ogg");
	return privColorCode + "-> " + HCB.replyTarget + " " + message;

def re(HCB, args):
	"""Send a private message to the person who last sent you a private message
	
	/re message
	message - message to send, can include spaces"""
	return hudchatcommands.r(HCB, args);

def callvote(HCB, args):
	"""Attempts to call a vote. Exec /callvote for the list of votes available.
	
	/callvote type [params]
	"""
	if len(args) == 0:
		sys.modules[glass.GUI_CurrentScreen()].voteSelection.show();
			
	CL_CallVote(" ".join(args));

def set(HCB, args):
	"""Set a cvar to a given value
	
	/set cvar value
	cvar - name of the cvar. Names are case insensitive apart from the first character.
	value - value to set the cvar to. Can include spaces, but consecutive spaces are reduced to one space."""
	if len(args) < 2:
		return None;
	name, value = args[0], " ".join(args[1:]);
	cvar_set(name, value);

def get(HCB, args):
	"""Print the value of a cvar to the HUD Chat Box
	
	/get cvar
	cvar - name of the cvar. Names are case insensitive apart from the first character."""
	if len(args) < 1:
		return None;
	name = args[0];
	value = cvar_get(name);
	if value == "":
		value = '""'
	return "^444" + name + " is " + value;

def ref(HCB, args):
	"""Sends a ref command to the server. Exec /ref for a list of commands.
	
	/ref command [parameters]
	"""
	#TODO
	CL_SendRefCommand(" ".join(args));

def stat(HCB, args):
	"""Sends status to all players"""

	CL_SendChat(cvar_get("game_serverstatus"), "all")

def listcmds(HCB, args):
	import sys
	"""Prints the names of hudchatcommands to the HUD Chat Box
	
	/listcmds [min] [number]
	min - The index to start printing from. Defaults to 0.
	number - the number of command names to print. Defaults to 10.
	Commands are printed in alphabetical order."""
	import silverback;
	
	min = 0 if len(args) < 1 else int(args[0]);
	number = 10 if len(args) < 2 else int(args[1]);
	max = min + number;

	commands = dir(sys.modules["hudchatcommands"]);
	commands = [cmd for cmd in commands if not hasattr(silverback,cmd) and not cmd.startswith("_") and cmd not in ("sys")];
	commands.sort();

	for cmd in commands[min:max]:
		string = "%03d" % commands.index(cmd) + " " + cmd;
		hudchatcommands._printToHCB("^777"+string, console = True);

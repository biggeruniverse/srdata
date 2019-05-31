#(c) savagerebirth.com 2011
#imports
import stacklesslib.monkeypatch
#stacklesslib.monkeypatch.patch_all()

import logging;
from silverback import *;

#crank the logging level based on con_developer
if cvar_getvalue("con_developer") <= 0:
	logging.root.setLevel(logging.INFO);

import glass;
import tools;
import vectors;
from collections import OrderedDict;

#helper function that will pre-empt infinite loops or excessively long-running tasklets
def stackless_frame():
	#gblSequenceHandler.pump();
	stacklesslib.main.mainloop.pump()

#this will print any uncollectable objects to stdout (good for finding cyclical deps)
#import gc;
#gc.set_debug(gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS | gc.DEBUG_SAVEALL);

#globals and constants go here
screenDimensions = cvar_get("vid_currentMode").split("x");
screenHeight = int( screenDimensions[1] );
screenWidth = int( screenDimensions[0] );
del screenDimensions;

def screenWidthPct(pct):
	if Demo_IsPlaying() and cvar_getvalue("demo_makeMovie") == 1:
		return int(cvar_getvalue("demo_movieWidth")*pct);
	return int(screenWidth*pct);

def screenHeightPct(pct):
	if Demo_IsPlaying() and cvar_getvalue("demo_makeMovie") == 1:
		return int(cvar_getvalue("demo_movieHeight")*pct);
	return int(screenHeight*pct);

inputLineHeight = int(0.0275 * screenHeight);

def getGameTimeString(seconds):
	if seconds > 0:
		hours = seconds // 3600;
		minutes = (seconds // 60) % 60;
		return "%01d:%02d:%02d " % (hours,minutes,seconds%60);
	return "";

def printstr(*objs):
	"""Each object supplied is converted to a string (str()) , then printed to the console on its own line."""
	for i, obj in enumerate(objs):
		con_println( "^963%02d" % i + " ^w " + str(obj) +"\n" );

def printrepr(*objs):
	"""Each object supplied is converted to its string representation (repr()), then printed to the console on its own line."""
	for i, obj in enumerate(objs):
		con_println( "^963%02d" % i + " "+ repr(obj) +"\n" );

def clamp(x, min=0, max=1):
	if x > max:
		x = max;
	elif x < min:
		x = min;
	return x;

#Input-related constants
MOUSE_FREE = 0;
MOUSE_RECENTER = 1;
MOUSE_FREE_INPUT = 2; #human siege mouse state

MOUSE_LEFTBUTTON = 1;
MOUSE_RIGHTBUTTON = 2;
MOUSE_MIDDLEBUTTON = 3;

KEY_ALT   = 132
KEY_CTRL  = 133
KEY_SHIFT = 134
KEY_MOUSE_LEFTBUTTON=200
KEY_MOUSE_RIGHTBUTTON=201
KEY_MOUSE_MIDDLEBUTTON=202

#Context stati
Hidden = 0;
Disabled = 1;
Enabled = 2;

#Research Constants
Available = Enabled
Researched = Hidden
Researching = Disabled

#server stati
GAME_STATUS_EMPTY=0;
GAME_STATUS_SETUP=1;
GAME_STATUS_WARMUP=2;	#warming up
GAME_STATUS_NORMAL=3;	#normal play mode
GAME_STATUS_ENDED=4;	#game finished and stats screen is shown
GAME_STATUS_NEXTMAP=5;	#about to go to the next map
GAME_STATUS_PLAYERCHOSENMAP=6;	#about to go to a map that was voted in or that the referee chose
GAME_STATUS_RANDOMMAP=7;
GAME_STATUS_RESTARTING=8;

#player stati
PLAYER_STATUS_LOBBY=0;
PLAYER_STATUS_UNITSELECT=1; #loadout
PLAYER_STATUS_SPAWNPOINT_SELECT=2;
PLAYER_STATUS_COMMANDER=3;
PLAYER_STATUS_PLAYER=4;
PLAYER_STATUS_SPECTATE=5;
PLAYER_STATUS_ENDGAME=6;
PLAYER_STATUS_SHOPPING=7; #this was added to support MOBA-like shopping mode

#cvar flags   ex: flags = (CVAR_SAVECONFIG|CVAR_VALUERANGE)
CVAR_SAVECONFIG =1;
CVAR_READONLY   =4;
CVAR_WORLDCONFIG=512;
CVAR_CHEAT      =1024;
CVAR_TRANSMIT   =2048;
CVAR_VALUERANGE =8192;
CVAR_SERVERINFO =16384;

#gametypes
GAMETYPE_RTSS       =0;
GAMETYPE_DEATHMATCH =1;
GAMETYPE_DUEL       =2;
GAMETYPE_CTF        =3;

#window flags
WT_CLOSE	=1;
WT_HELP		=2;
WT_MINIMIZE	=4;
WT_MAXIMIZE	=8;
WT_PIN		=16;
WT_ALL		=255;

#commander modes
CMDR_PLACING_OBJECT   =1;
CMDR_PLACING_LINK     =2;
CMDR_PICKING_LOCATION =3;
CMDR_PICKING_UNIT     =4;

#dueling states
DP_NOTDUELING    =0;
DP_READY         =1;
DP_DUELING       =2;
DP_CHALLENGING   =3;

#damage flags
DAMAGE_NO_KNOCKBACK = 0x00000001
DAMAGE_NO_AIR_TARGETS	    = 0x00000002
DAMAGE_NO_GROUND_TARGETS    = 0x00000004
DAMAGE_UNBLOCKABLE  = 0x00000008
DAMAGE_SELF_NONE    = 0x00000010
DAMAGE_SELF_HALF    = 0x00000020
DAMAGE_NO_FALLOFF   = 0x00000040
DAMAGE_NO_STRUCTURES= 0x00000080
DAMAGE_QUAKE_EVENT  = 0x00000100
DAMAGE_NO_REACTION  = 0x00000200
DAMAGE_STRIP_STATES = 0x00000400
DAMAGE_EXPLOSIVE    = 0x00000800
#DAMAGE_PHYSICAL    = 0x00001000
#DAMAGE_MAGICAL	    = 0x00002000
DAMAGE_SPLASH       = 0x00004000
DAMAGE_FALL         = 0x00008000
DAMAGE_SILENT       = 0x00010000
DAMAGE_DELAYED      = 0x00020000

# ###################################################################
# Tango Colour Palette http://tango.freedesktop.org/static/cvs/tango-art-tools/palettes/Tango-Palette.png
# ###################################################################

tangoYellowLight = glass.Color(252, 201, 79);
tangoYellow = glass.Color(237, 212, 0);
tangoYellowDark = glass.Color(196, 160, 0);

tangoOrangeLight = glass.Color(252, 175, 62);
tangoOrange = glass.Color(245, 121, 0);
tangoOrangeDark = glass.Color(206, 92, 0);

tangoBrownLight = glass.Color(233, 185, 110);
tangoBrown = glass.Color(193, 125, 17);
tangoBrownDark = glass.Color(143, 89, 2);

tangoGreenLight = glass.Color(138, 226, 52);
tangoGreen = glass.Color(115, 210, 22);
tangoGreenDark = glass.Color(78, 154, 6);

tangoBlueLight = glass.Color(144, 159, 207);
tangoBlue = glass.Color(52, 101, 164);
tangoBlueDark = glass.Color(32, 74, 135);

tangoPurpleLight = glass.Color(173, 127, 168);
tangoPurple = glass.Color(117, 80, 123);
tangoPurpleDark = glass.Color(92, 53, 102);

tangoRedLight = glass.Color(239, 41, 41);
tangoRed = glass.Color(204, 0, 0);
tangoRedDark = glass.Color(164, 0, 0);

tangoGrey1 = glass.Color( 238, 238 , 236);
tangoGrey2 = glass.Color( 211, 215 , 207);
tangoGrey3 = glass.Color( 186, 189 , 182);
tangoGrey4 = glass.Color( 136, 138 , 133);
tangoGrey5 = glass.Color( 85, 87 , 83);
tangoGrey6 = glass.Color( 46, 52 , 54);

themeGold = glass.Color(248, 160,11);

#while I'm at it, some more frequently used colours

white = glass.Color( 255, 255,255);
black = glass.Color(0,0,0);
transparency = glass.Color( 0,0,0,0);
gold = glass.Color(249,219,107);

# colors used in Skope's wips:

windowBackground = glass.Color(22, 13, 10);
windowTop = glass.Color(85, 21, 11);
windowCommhud = glass.Color(34, 16, 14);
# For consistency, the following colours are global

allyColorCode = "^259";
commColorCode = "^492";
enemyColorCode = "^923";
timeColorCode = "^779";
refColorCode = "^y";
privColorCode = "^c";

allyColor = tools.savColorToGlass( allyColorCode );
commColor = tools.savColorToGlass( commColorCode );
enemyColor = tools.savColorToGlass( enemyColorCode );
timeColor = tools.savColorToGlass( timeColorCode );
refColor = tools.savColorToGlass( refColorCode );
privColor = tools.savColorToGlass( privColorCode );

## FONT SIZES

fontSizeSmall = glass.GUI_GetFont(12);
fontSizeMedium = glass.GUI_GetFont(16);
fontSizeLarge = glass.GUI_GetFont(20);

LOADING = "^icon loading/loading0000^Loading...";

AnimStates = tools.enum(
'AS_IDLE',

'AS_MELEE_1',
'AS_MELEE_2',
'AS_MELEE_3',
'AS_MELEE_4',
'AS_ALT_MELEE_1',
'AS_ALT_MELEE_2',
'AS_ALT_MELEE_3',
'AS_ALT_MELEE_4',
'AS_MELEE_CHARGE',
'AS_MELEE_RELEASE',

'AS_MELEE_MOVE_1',
'AS_MELEE_MOVE_2',
'AS_MELEE_MOVE_3',
'AS_MELEE_MOVE_4',
'AS_MELEE_MOVE_CHARGE',
'AS_MELEE_MOVE_RELEASE',

'AS_BLOCK',

'AS_WALK_LEFT',
'AS_WALK_RIGHT',
'AS_WALK_FWD',
'AS_WALK_BACK',

'AS_RUN_LEFT',
'AS_RUN_RIGHT',
'AS_RUN_FWD',
'AS_RUN_BACK',

'AS_SPRINT_LEFT',
'AS_SPRINT_RIGHT',
'AS_SPRINT_FWD',
'AS_SPRINT_BACK',

'AS_JUMP_START_LEFT',
'AS_JUMP_START_RIGHT',
'AS_JUMP_START_FWD',
'AS_JUMP_START_BACK',

'AS_JUMP_MID_LEFT',
'AS_JUMP_MID_RIGHT',
'AS_JUMP_MID_FWD',
'AS_JUMP_MID_BACK',

'AS_JUMP_END_LEFT',
'AS_JUMP_END_RIGHT',
'AS_JUMP_END_FWD',
'AS_JUMP_END_BACK',

'AS_JUMP_UP_START',
'AS_JUMP_UP_MID',
'AS_JUMP_UP_END',

'AS_JUMP_LAND',

'AS_DODGE_START_LEFT',
'AS_DODGE_START_RIGHT',
'AS_DODGE_START_FWD',
'AS_DODGE_START_BACK',

'AS_DODGE_MID_LEFT',
'AS_DODGE_MID_RIGHT',
'AS_DODGE_MID_FWD',
'AS_DODGE_MID_BACK',

'AS_DODGE_END_LEFT',
'AS_DODGE_END_RIGHT',
'AS_DODGE_END_FWD',
'AS_DODGE_END_BACK',

'AS_CROUCH_IDLE',

'AS_CROUCH_LEFT',
'AS_CROUCH_RIGHT',
'AS_CROUCH_FWD',
'AS_CROUCH_BACK',

'AS_WALK_WITH_BAG',

'AS_MINE',
'AS_REPAIR',
'AS_CONSTRUCT',

'AS_WOUNDED_LEFT',
'AS_WOUNDED_RIGHT',
'AS_WOUNDED_FWD',
'AS_WOUNDED_BACK',

'AS_DEATH_GENERIC',
'AS_DEATH_LEFT',
'AS_DEATH_RIGHT',
'AS_DEATH_FWD',
'AS_DEATH_BACK',

'AS_RESURRECTED',

'AS_WEAPON_IDLE_1',
'AS_WEAPON_IDLE_2',
'AS_WEAPON_IDLE_3',
'AS_WEAPON_IDLE_4',
'AS_WEAPON_IDLE_5',
'AS_WEAPON_IDLE_6',

'AS_WEAPON_CHARGE_1',
'AS_WEAPON_CHARGE_2',
'AS_WEAPON_CHARGE_3',
'AS_WEAPON_CHARGE_4',
'AS_WEAPON_CHARGE_5',
'AS_WEAPON_CHARGE_6',

'AS_WEAPON_FIRE_1',
'AS_WEAPON_FIRE_2',
'AS_WEAPON_FIRE_3',
'AS_WEAPON_FIRE_4',
'AS_WEAPON_FIRE_5',
'AS_WEAPON_FIRE_6',

'AS_WEAPON_RELOAD_1',
'AS_WEAPON_RELOAD_2',
'AS_WEAPON_RELOAD_3',
'AS_WEAPON_RELOAD_4',
'AS_WEAPON_RELOAD_5',
'AS_WEAPON_RELOAD_6',

'AS_WEAPON_SWITCH',

'AS_WPSTATE_IDLE',
'AS_WPSTATE_SWITCH',
'AS_WPSTATE_CHARGE',
'AS_WPSTATE_SPINUP',
'AS_WPSTATE_SPINDOWN',
'AS_WPSTATE_OVERHEAT',
'AS_WPSTATE_FIRE',
'AS_WPSTATE_BACKFIRE',

'AS_ITEM_SLEEP',
'AS_ITEM_ACTIVE',

'AS_CONSTRUCT_1',
'AS_CONSTRUCT_2',
'AS_CONSTRUCT_3',
'AS_CONSTRUCT_FINAL',

'AS_SUICIDE',

'AS_MINE2',
'AS_DEATH_SPECIAL');


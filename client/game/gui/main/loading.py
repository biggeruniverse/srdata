# (c) 2011 savagerebirth.com

from silverback import *;
import glass;
import tools;

def frame():
	#FIXME
	#players = savage.getPlayers();
	players = [];
	
	loading.serverName.setCaption(Client_GetStateString("svr_name"))
	loading.serverName.setPosition(450/2-loading.serverName.getWidth()/2, 22)
	loading.time.setCaption("GAME TIME: ^w" + Client_GetStateString("svr_time"))
	loading.players.setCaption("PLAYERS: ^w" + str(len(players)) + "/" + Client_GetStateString("svr_maxclients"))
	loading.type.setCaption("GAME TYPE: ^w" + str("RTSS"))
	loading.official.setCaption("OFFICIAL: ^w" + Client_GetStateString("svr_official"))

def onShow():
	import random;
	#no one will notice it here!
	tools.run_gc();
	loading.tip.setText(GUI_GetTip());

	bgs = ["/gui/loadingImages/nexus.jpg", "/gui/loadingImages/arcana.jpg"];
	loading.background.setImage(random.choice(bgs), False);
	ratio = loading.background.getWidth()/float(loading.background.getHeight());
	loading.background.setHeight(screenHeight);
	loading.background.setWidth(int(screenHeight*ratio));

def add(obj, x=None, y=None):    
	if x is not None:
		obj.setPosition(x, y);
	glass.GUI_ScreenAddWidget("loading", obj);   

def setWorld(world_name):
	Host_VerifyOverhead("world/"+world_name+"_overhead.jpg");
	loading.minimap.setImage("world/"+world_name+"_overhead.jpg", "none", 1);
	loading.minimap.setSize(145, 145);
	loading.mininame.setCaption(world_name);
	loading.mininame.setX(loading.info.getWidth() // 2 - loading.mininame.getWidth() // 2);

def updatePlayers():
	if hasattr(savage, 'getPlayers'):
		players = savage.getPlayers()
	else:
		players = []
	loading.players.setCaption("PLAYERS: ^w" + str(len(players)) + "/" + Client_GetStateString("svr_maxclients"))

glass.GUI_CreateScreen('loading');

black = DefaultContainer();
black.setBackgroundColor(glass.Color(208, 208, 208));
black.setSizePct(1, 1);
add(black);

# concept art bg
background = DefaultImage();
background.setImage("/gui/loadingImages/nexus.jpg", False);

ratio = background.getWidth()/float(background.getHeight());
background.setHeight(screenHeight);
background.setWidth(int(screenHeight*ratio));
add(background, screenWidth // 2 - background.getWidth() // 2, screenHeight // 2 - background.getHeight() // 2);

overlay = DefaultImage();
overlay.setImage("/gui/main/images/loading_overlay.png", False);
overlay.setSizePct(1.0,1.0);
add(overlay);

easierToReadThingy = DefaultContainer();
easierToReadThingy.setBackgroundColor(glass.Color(0, 0, 0, 50));
easierToReadThingy.setSizePct(1, 1);
add(easierToReadThingy);

connecting = DefaultLabel("Press 'ESC' to cancel the loading process.");
connecting.setFont(fontSizeSmall);
add(connecting, screenWidth // 2 - connecting.getWidth() // 2, 30);

info = DefaultContainer();
info.setBackgroundColor(glass.Color(30, 0, 0, 45));
info.setSize(450, 225);
infoback = DefaultImage();
infoback.setImage("/gui/main/images/loading_panel_bg.png", False);
info.add(infoback,0,0);
infoback.setSizePct(1,1);

connectingTo = DefaultLabel("Connecting to...");
connectingTo.setFont(fontSizeSmall);
connectingTo.setForegroundColor(glass.Color(193, 193, 193));
info.add(connectingTo, "center", 5);

serverName = DefaultLabel(cvar_get("svr_name"));
serverName.setFont(fontSizeSmall);
info.add(serverName, "center", 22);

left = DefaultWindow();
left.setOpaque(0);
left.setBackgroundColor(glass.Color(0, 0, 0, 0));
left.setSize(135, 143);
info.add(left, 10, 50);

bluey = glass.Color(216, 228, 240);

time = DefaultLabel("GAME TIME: ^w" + str("10:69"));
time.setForegroundColor(bluey);
time.setFont(fontSizeSmall);
left.add(time, 5, 3, "right");

players = DefaultLabel("PLAYERS: ^w" + str("0/20"));
players.setForegroundColor(bluey);
players.setFont(fontSizeSmall);
left.add(players, 5, 18, "right");

type = DefaultLabel("GAME TYPE: ^w" + str("RTSS"));
type.setForegroundColor(bluey);
type.setFont(fontSizeSmall);
left.add(type, 5, 33, "right");

official = DefaultLabel("OFFICIAL: ^w" + str("YES"));
official.setForegroundColor(bluey);
official.setFont(fontSizeSmall);
left.add(official, 5, 47, "right");

minimap = DefaultImage();
minimap.setImage(cvar_get("world_overhead"), "none", 1);
minimap.setSize(145, 145);
info.add(minimap, "center", 50);

mininame = DefaultLabel(str(cvar_get("world_name")));
info.add(mininame, "center", 200);

right = DefaultWindow();
right.setBackgroundColor(glass.Color(0, 0, 0, 0));
right.setSize(135, 143);
info.add(right, 10, 50, "right");

message = DefaultTextBox("WELCOME,\nEnjoy your time on our server and be sure to spread the word about Savage: Rebirth!");
message.setWidth(130);
message.setFont(fontSizeSmall);
message.setBackgroundColor(transparency);
message.setForegroundColor(bluey);
right.add(message, 5, 3);

add(info, screenWidth // 2 - info.getWidth() // 2, screenHeight // 2 - info.getHeight() // 2);

tips = DefaultWindow();
tips.setSize(450, int(screenHeight*0.12));
tips.setBackgroundColor(glass.Color(0,0,0,80));
add(tips, screenWidth // 2 - tips.getWidth() // 2, screenHeight-(screenHeight//10+tips.getHeight()));

tipstitle = DefaultLabel("^894SAVAGE TIPS");
tips.add(tipstitle, "center", 5);

tip = DefaultTextBox();
tip.setFont(fontSizeSmall);
tip.setBackgroundColor(transparency);
tip.setForegroundColor(bluey);
tip.setOpaque(0);
tips.add(tip, 0, tipstitle.getHeight()+5);
tip.setSize(tips.getWidth()-10,tips.getHeight()-25);

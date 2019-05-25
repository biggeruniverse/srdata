
from silverback import *;
import glass;
import savage;
import commcontexts;

glass.GUI_CreateScreen('commhud');

# windows and widgets are essentially the same but will seperate just incase we need them seperate in the future
windowStack = {};
widgetStack = {};
selection = CommSelection();
gblEventHandler.addGameListener(selection);

team = savage.Team(1);

initialized = False;
def onShow():
	GUI_ShowCursor("crosshair");
	commcontexts.buildContextsIfNeeded();
	commhud.toolBox.onShow();
	commhud.contextmenu.setVisible(0);
	commhud.contextmenu.close();
	
	commhud.resourcesPanel.onShow();
	commhud.resourcesPanel.update();
	commhud.buffPool.rebuild();

	commhud.miniMap.rebuild();

	commhud.chatBox.deactivate();

	commhud.alerts.onShow();

	if commhud.topBar.isVisible():
		commhud.topBar.setVisible(0);
	
	"""
	# What is that? Looks like old me wrote this, but I'm not sure what for...	
	curTeam = savage.Team(savage.getLocalPlayer().getTeam());
	
	#if curTeam.teamId != commhud.team.teamId:
	commhud.team = curTeam;
	"""

def frame():
	
	commhud.resourcesPanel.update();
	commhud.buffPool.update();
	
	#commhud.hudinfo.update();
	#commhud.researchManager.update();
	commhud.voteWindow.frame();
	commhud.timer.frame();
	commhud.fps.frame();
	commhud.contextmenu.update();
	commhud.updateMouseInfo();
			
def add(obj, x=None, y=None):    
	if x is not None:		
		if x == "left":
			obj.setX(5);
		elif x == "right":
			obj.setX(screenWidth - obj.getWidth() - 5);
		elif x == "center":
			obj.setX(screenWidthPct(0.5) - obj.getWidth() // 2);

		else:
			obj.setX(x);

		if y == "top":
			obj.setY(5);
		elif y == "bottom":
			obj.setY(screenHeight - obj.getHeight() - 5);
		elif y == "center":
			obj.setY(screenHeightPct(0.5) - obj.getHeight() // 2);
		else:
			obj.setY(y);

	glass.GUI_ScreenAddWidget("commhud", obj);
	
def defaultAction(x, y):
	obj = savage.getObjectUnder(x,y);
	if obj == None:
		CL_CommanderLeftClick(); #send it thru to the hardcode to see if something is doing
	elif commhud.selection.empty():
		commhud.selection.selectObject(obj, False)
	commhud.selection.send(savage.getLocalTeam().teamId)
	if obj == None:
		CL_OrderWaypoint(x,y);
	else:
		CL_OrderWaypoint(x,y,obj.objectId);

def handleHotkey(action):
	con_println("handling key "+str(action)+"\n");

	if commhud.contextmenu.isVisible():
		try:
			button = commhud.contextmenu.context.getButtonAction(action);
		except KeyError:
			return; #Import logging!
	elif commhud.toolBox.tabContainer.getSelectedTab() == "Build":
		try:
			button = commhud.toolBox.buildMenu.context.getButtonAction(action);
		except KeyError:
			return; #Import logging!
	elif commhud.toolBox.tabContainer.getSelectedTab() == "Cmd":
		try:
			button = commhud.toolBox.commandsMenu.context.getButtonAction(action);
		except KeyError:
			return; #Import logging! 		
	button.activate()

def getActiveContextMenu(ctx):
	# 3 different contextmenus ftw!
	for cm in [commhud.contextmenu, commhud.toolBox.buildMenu, commhud.toolBox.commandsMenu]:
		if cm.context == ctx:
			return cm;

	return commhud.toolBox.buildMenu if commhud.toolBox.tabContainer.getSelectedTab() == "Build" else commhud.toolBox.commandsMenu;

def updateMouseInfo():
	x, y = Input_GetMouseXY();
	obj = savage.getObjectUnder(x, y);
	if obj == None or commhud.contextmenu.getAlpha() == 255:
		commhud.mouseInfoLabel.setVisible(0);
		return;

	ot = obj.getType();
	if obj.isPlayer():
		name = obj.getFormattedName();
	else:
		name = obj.getNameColorCode() + ot.getValue("description");

	commhud.mouseInfoLabel.setCaption(name);
	commhud.mouseInfoLabel.setPosition(x - commhud.mouseInfoLabel.getWidth() // 2, y + 10);
	commhud.mouseInfoLabel.setVisible(1);

## HUD INFO OVERLAY ##
"""	
hudinfo = CommHudInfo();
add(hudinfo);
"""

# Build the contexts on screen init, not in onShow()
#commcontexts.buildContextsIfNeeded();


## CANVAS ##
#everything before this point will not be interactable

canvas = glass.GlassCanvas();
canvas.setSizePct(1,1);
canvas.setBackgroundColor(transparency);
canvas.setPosition(0,0);
add(canvas);

## INPUT HANDLER ##

commInput = CommInputHandler();
canvas.addMouseListener(commInput);

# The green selection rect
# Moved that to the top so it doesn't draw over other widgets
selectionRect = DefaultContainer();
selectionRect.setBaseColor(glass.Color(138, 226, 52));
selectionRect.setBackgroundColor(glass.Color(138, 226, 52, 64));
selectionRect.setFrameSize(1);
selectionRect.setVisible(0);
canvas.add(selectionRect);

## RESOURCES/INFO PANEL ##		

resourcesPanel = CenterResourceContainer();
add(resourcesPanel, "center", "top");

buffPool = BuffPoolContainer();
add(buffPool, "left", "top");

## VOTES ##

voteWindow = VoteInfoBox();
add(voteWindow, "center", -voteWindow.getHeight());

voteSelection = VoteSelectionWindow();
add(voteSelection, "center", screenHeightPct(0.5));

## FPS ##

fps = CommFPS();
add(fps, "left", "center");

## CHAT ##

# Chat needs serious love
chatBox = CommChatBox()#(resourcesPanel.getHeight());
add(chatBox, "left", "top");
chatBox.setSizePct(0.4,0.32);
chatBox.setWidth(resourcesPanel.getX() - 10);
chatBox.resize();
#chatBox.showHistory(0);

## VOICE CHAT ##

voiceChat = VoiceChatBox();
voiceChat.setSizePct(0.3,0.35);
voiceChat.table.adjustSizeToPct(1,1);
add(voiceChat, "center", "center");
voiceChat.centerWindow();
voiceChat.setY(screenHeight/2+40);

## MINIMAP ##

miniMap = CommMiniMap();
add(miniMap, "left", "bottom");

## TIMER ##

timer = CommTimer();
add(timer, "left", miniMap.getY() - timer.getHeight() - 5);

## TOOLBOX ##

toolBox = ToolBox();
selection.addListener(toolBox);
add(toolBox, "right", "bottom");

## TEMPORARY RESIGN ##

resign = DefaultButton(" >> ");
resign.setForegroundColor(tangoYellow)
resign.setClickAction("CL_RequestResign()");
resign.setAlpha(200);
add(resign, "right","top");

## SELECTION INFO ##

selectionInfo = SelectionInfo();
selection.addListener(selectionInfo);
add(selectionInfo, screenWidth - toolBox.getWidth() - selectionInfo.getWidth() - 10, "bottom");

## ROSTER ##

rosterWindow = CommRosterWindow();
#add(rosterWindow, 200, 200);

## RADIAL CONTEXTMENU ##
# The radial contextmenu is used to display research options 
# and actions when selecting a building. 

contextmenu = RadialContextMenu();
selection.addListener(contextmenu);
add(contextmenu);

mouseInfoLabel = DefaultLabel("");
mouseInfoLabel.setFont(fontSizeSmall);
add(mouseInfoLabel, "center", "center");

## Comm Alerts ##

alerts = CommAlertHandler();
add(alerts, "right", 200);

## The ingame topbar ##

topBar = GameTopBar();
add(topBar);
topBar.setVisible(0);


# (c) 2010 savagerebirth.com
# this file creates the heads-up display

from silverback import *;
import savage;
import glass;
from vectors import Vec3;

def frame():
	gametime = getGameTimeString(cvar_getvalue("game_timeLimitSeconds"));
	if gametime != "":
		if cvar_getvalue("game_timeLimitSeconds") < 45:
			gametime = "^900"+gametime;
		hud.timer.setCaption("^icon ../../gui/standard/icons/timer^%s" %(gametime));
		hud.timer.adjustSize();
	else:
		hud.timer.setCaption("");
	
	player = savage.getLocalPlayer();
	
	hud.teamStatus.update();
	hud.updateGold();
	hud.hpDisplay.update();
	hud.stamina.update();
	hud.levelDisplay.update();
	hud.inventory.updateAmmo();
	hud.stateContainer.update();
	hud.updateCrosshairLimits();
	hud.minimap.setAlpha(int(cvar_getvalue('cl_minimap_brightness')*255));
	hud.waypoint.update();
	hud.killtarget.update();
	hud.hitIndicator.update();
	hud.focusReticle.update();
	hud.updateGameStatus();
	hud.crosshair.update();
	hud.voteWindow.frame();
	if hud.scoreboard.isVisible(): 
		hud.scoreboard.update();
	
	hud.fpswindow.update();

def onShow():
	hud.chatBox.deactivate();
	hud.minimap.setMap(cvar_get("world_overhead"));
	hud.scoreboard.arrange();
	hud.scoreboard.update(); #remove the placeholders in scoreboard
	hud.crosshair.reset();
	hud.voteWindow.reset();
	hud.timer.setCaption("");
	hud.killtarget.setVisible(False);
	hud.inventory.buildInventory();
	if hud.topBar.isVisible():
		hud.topBar.setVisible(False);
	
	hud.frame(); #remove any other placeholders

glass.GUI_CreateScreen('hud');

## ORDER/WAYPOINT ##
waypoint = Waypoint();
waypoint.setVisible(False);
glass.GUI_ScreenAddWidget("hud", waypoint);
gblEventHandler.addGameListener(waypoint);

## HIT INDICATOR ##
hitIndicator = DirectionalIndicator();
glass.GUI_ScreenAddWidget("hud", hitIndicator);
hitIndicator.setPosition(screenWidth//2-hitIndicator.getWidth()//2, screenHeight//2-hitIndicator.getWidth()//2);

## FOCUS RETICLE ##
focusReticle = FocusIndicator();
glass.GUI_ScreenAddWidget("hud", focusReticle);

## KILLER TARGET ##
killtarget = Waypoint();
killtarget.setVisible(False);
killtarget.setImage("/gui/standard/icons/1_nl_way_killer.tga");
killtarget.showDistance(False);
glass.GUI_ScreenAddWidget("hud", killtarget);

class KillHandler:
	def __init__(self):
		pass;

	def onEvent(self, e):
		if e.eventType == "obituary":
			if e.targetId == savage.getLocalPlayer().objectId and e.sourceId != savage.getLocalPlayer().objectId:
				hud.killtarget.setVisible(True);
				hud.killtarget.setObject(savage.getGameObject(e.sourceId));
		elif e.eventType == "resurrection":
			if e.targetId == savage.getLocalPlayer().objectId:
				hud.killtarget.setVisible(False);

		elif e.eventType == "player_wounded":
			hud.hitIndicator.setTarget(savage.getGameObject(e.sourceId));
		elif e.eventType == "spectate":
			hud.killtarget.setVisible(False)

gblEventHandler.addGameListener(KillHandler());

class StaminaDisplay(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);
		
		self.setOpaque(False);
		self.setSizePct(0.17, 0.03);
		if self.getHeight() % 2 != 0:
			self.setHeight(self.getHeight() + 1);
		
		self.bar = glass.GlassProgressBar();
		self.bar.setBackgroundColor(glass.Color(255, 255, 255, 128));
		self.bar.setForegroundColor(glass.Color(20,255,248, 128));
		self.bar.setSize(int(self.getWidth()),int(self.getHeight()));		
		self.bar.setBackgroundImage("gui/base/images/progress_bg.tga");
		self.add(self.bar, 0, 0, "center", "center");
		
		self.label = DefaultLabel();
		self.label.setCaption("000");
		self.label.setForegroundColor(glass.Color(220,255,248, 128));
		#self.label.setFont(fontSizeLarge);
		self.add(self.label, 0, 0, "center", "center");
		#self.pct = DefaultLabel();
		#self.pct.setCaption("%");
		#self.pct.setForegroundColor(glass.Color(220,255,248));
		#self.pct.setFont(fontSizeSmall);
		#self.add(self.pct, self.label.getWidth(), 0, "left", "bottom");
		
	def update(self):
		player = savage.getLocalPlayer();
		
		self.label.setCaption(str(int(player.getStaminaPct()*100)) + " %");
		self.bar.setProgress(player.getStaminaPct());

class HealthDisplay(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);

		self.setOpaque(False);
		self.setSizePct(0.17, 0.03);
		if self.getHeight() % 2 != 0:
			self.setHeight(self.getHeight() + 1);
		
		self.bar = glass.GlassProgressBar();
		self.bar.setBackgroundColor(white);
		self.bar.setForegroundColor(glass.Color(255,21,22, 128));
		self.bar.setSize(int(self.getWidth()),int(self.getHeight()));
		self.bar.setBackgroundImage("gui/base/images/progress_bg.tga");
		self.bar.setReversed(True);
		self.add(self.bar, 0, 0, "center", "center");
		
		self.label = DefaultLabel();
		self.label.setCaption("000");
		self.label.setForegroundColor(glass.Color(255,237,237, 128));
		#self.label.setFont(fontSizeLarge);
		self.add(self.label, 0, 0, "center", "center");
		
	def update(self):
		player = savage.getLocalPlayer();
		
		self.label.setCaption(str(int(player.getHealth())));
		self.bar.setProgress(player.getHealthPct());

class LevelDisplay(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);

		#self.setOpaque(True);
		self.setBackgroundColor(transparency);
		self.setSize(screenHeightPct(0.06), screenHeightPct(0.06));

		bg = glass.GlassLabel("");
		bg.setImage("gui/game/images/halfcircle.png");
		bg.setSize(screenHeightPct(0.06), screenHeightPct(0.03));
		self.add(bg, 0, 0);

		#bot = DefaultContainer();
		#bot.setBackgroundColor(glass.Color(0,0,0,128));
		#bot.setSize(screenHeightPct(0.06), screenHeightPct(0.03));
		#self.add(bot, 0, screenHeightPct(0.03));

		self.progress = glass.GlassProgressDisc();
		self.progress.setSize(self.getHeight() - 7,self.getHeight() - 7);
		self.progress.setImage("gui/game/images/purple_ring.png");
		#self.progress.setProgress(1);
		self.add(self.progress, "center", "center");
		

		self.level = DefaultLabel("1");
		#self.level.setFont(fontSizeSmall);
		self.level.setForegroundColor(tangoPurple);
		self.add(self.level, "center", "center");

	def update(self):
		player = savage.getLocalPlayer();
		team = savage.getTeamObject(player.getTeam());
		currentXp = savage.getXPForLevel(team.getRace(), player.getLevel())
	
		self.level.setCaption(str(player.getLevel()));
		self.progress.setProgress((player.getXp()-currentXp)/float(savage.getXPForLevel(team.getRace(), player.getLevel()+1)));
		



#starting from the gold to the right of the minimap and proceeding anti clockwise

## MAP and surrounding things ##

mmWindow = DefaultWindow();
mmWindow.setFrameStyle("Shadow");
mmWindow.setSize(int(0.208*screenHeight),int(0.208*screenHeight));
mmWindow.setBackgroundColor(transparency);

minimap = glass.GlassMiniMap();
#minimap.setX(10);
minimap.setSize(int(0.208*screenHeight),int(0.208*screenHeight));
#same number of pixels so it's square
#well assuming the pixel aspect ratio is 1:1
mmWindow.add(minimap);
glass.GUI_ScreenAddWidget("hud",mmWindow);
mmWindow.setPosition(5,5);

player_money = glass.GlassLabel("_ABCDE ");
player_money.setForegroundColor(gold);
player_money.setPosition( int(minimap.getWidth() + 10 + screenWidth*0.01875), int(screenHeight*0.025));
glass.GUI_ScreenAddWidget("hud", player_money);

timer = glass.GlassLabel("_AB:CD ");
timer.setFont(glass.GUI_GetFont(20));
timer.setPositionPct(0.01875, 0.025+0.208);
glass.GUI_ScreenAddWidget("hud", timer);

## TEAM STATUS ##

teamStatus = ResourcePanel();
teamStatus.setVisible(False);
glass.GUI_ScreenAddWidget("hud", teamStatus);

## CHAT ##

chatBox = HUDChatBox();
glass.GUI_ScreenAddWidget("hud", chatBox);

chatBox.setPositionPct(0,0.415);
chatBox.setX(10);
chatBox.setSizePct(0.4,0.42);
chatBox.resize();

## HEALTH AND STAMINA DISPLAY ##

hpDisplay = HealthDisplay();
stamina = StaminaDisplay();

plus = DefaultLabel("+");
plus.setForegroundColor(tangoRed);
plus.setFont(fontSizeLarge);
plus.setSize(0,0); # todo

#staminaImage = DefaultImage();
staminaImage = DefaultLabel("+");
staminaImage.setForegroundColor(tangoBlue);
staminaImage.setFont(fontSizeLarge);
staminaImage.setSize(plus.getWidth(), plus.getWidth());

levelDisplay = LevelDisplay();

conditionContainer = DefaultWindow();
conditionContainer.setFrameStyle("SmallEight");
conditionContainer.setBackgroundColor(glass.Color(0,0,0,128));
glass.GUI_ScreenAddWidget("hud", conditionContainer);

conditionContainer.setSize(levelDisplay.getWidth() + hpDisplay.getWidth() * 2 + plus.getWidth()*2 + 20, hpDisplay.getHeight());
conditionContainer.setPosition(screenWidthPct(.5) - conditionContainer.getWidth() // 2, screenHeightPct(1)-conditionContainer.getHeight() - 10);

#conditionContainer.add(levelDisplay, "center", "center");

conditionContainer.add(hpDisplay, plus.getWidth() + 4, "center");
conditionContainer.add(stamina, conditionContainer.getWidth() - stamina.getWidth() - staminaImage.getWidth() - 4 , "center");

conditionContainer.add(plus, 2, "center");
conditionContainer.add(staminaImage, conditionContainer.getWidth() - staminaImage.getWidth() - 2 , "center");

glass.GUI_ScreenAddWidget("hud",levelDisplay);
levelDisplay.setPosition(screenWidthPct(.5) - levelDisplay.getWidth() // 2, conditionContainer.getY() - levelDisplay.getHeight() // 2 - 4);

## STATE EFFECT DISPLAY ##

stateContainer = StateDisplay();
#stateContainer.setOpaque(True)
#stateContainer.setBackgroundColor(black);
#stateContainer.setX( healthValue.getX() + healthValue.getWidth() + 15 );
stateContainer.setX( levelDisplay.getWidth() + levelDisplay.getX() + 5);
stateContainer.setY( conditionContainer.getY() - stateContainer.getHeight() - 5 );
stateContainer.setSize(conditionContainer.getWidth() // 2 - 20, screenHeightPct(0.06));
glass.GUI_ScreenAddWidget("hud",stateContainer);

## VOICE CHAT ##

voiceChat = VoiceChatBox();
voiceChat.setSizePct(0.3,0.35);
voiceChat.table.adjustSizeToPct(1,1);
glass.GUI_ScreenAddWidget("hud",voiceChat);
voiceChat.centerWindow();
voiceChat.setY(screenHeight//2+40);

## INVENTORY ##

inventory = InventoryWindow();
inventory.setPosition( screenWidthPct(1) - (inventory.getWidth()+5) , screenHeightPct(1)  - inventory.getHeight()-5);
glass.GUI_ScreenAddWidget("hud", inventory);

## NOTIFICATIONS ##
scroll = glass.GlassScrollArea();
scroll.setAutoscroll(True);
scroll.setSizePct(0.32,0.16);
scroll.setPosition(screenWidth-scroll.getWidth() - 10,10);
scroll.setScrollPolicy(1,1); #SHOW_NEVER
glass.GUI_ScreenAddWidget("hud", scroll);

notifyBuffer = MessageBuffer(["notify"]); #TODO notify_generalhide too?
scroll.setContent(notifyBuffer);
notifyBuffer.setSize(scroll.getWidth(), scroll.getHeight());
notifyBuffer.setFadeTop(True);
notifyBuffer.setFadeBottom(False);
notifyBuffer.showTime(False);
for i in range(10):
	notifyBuffer.addRow(" ");

## VOTES ##

voteWindow = VoteInfoBox();
glass.GUI_ScreenAddWidget("hud", voteWindow);
voteWindow.setPosition( minimap.getWidth() + minimap.getX() + 10, -voteWindow.getHeight());

# Finally objects in the screen's center, proceeding from the top downward

## GAME STATUS ##

gamestatusWindow = DefaultWindow();
gamestatusWindow.setFrameStyle("SmallEight");
gamestatusWindow.setPositionPct(.5,.35);
gamestatusWindow.setBackgroundColor(glass.Color(0,0,0,50));
glass.GUI_ScreenAddWidget("hud",gamestatusWindow);

gamestatus = glass.GlassLabel();
gamestatus.setForegroundColor(glass.Color(255,255,255));
gamestatusWindow.add(gamestatus,0,0);


## CROSSHAIR ##

crosshair = HUDCrossHair();
glass.GUI_ScreenAddWidget("hud",crosshair);

crosshairLimits = glass.GlassLabel("");
crosshairLimits.setBaseColor( white );
crosshairLimits.setSize(0,0);
crosshairLimits.setFrameSize(4);
glass.GUI_ScreenAddWidget("hud",crosshairLimits);

crosshairLimitsPadding = crosshair.crosshair.getWidth()//2;

### SCOREBAORD ##

scoreboard = TeamScore();
glass.GUI_ScreenAddWidget("hud",scoreboard);

## FPS WINDOW ##

fpswindow = FpsWindow();
fpswindow.setPositionPct(0, 0.5);
glass.GUI_ScreenAddWidget("hud",fpswindow);

## Graphics Panel ##

#graphicspanel = GraphicsPanel();
#graphicspanel.setPosition(screenWidth - graphicspanel.getWidth() - 30, screenHeightPct(0.1));
#glass.GUI_ScreenAddWidget("hud",graphicspanel);

## Vote Selection Window ##

voteSelection = VoteSelectionWindow();
glass.GUI_ScreenAddWidget("hud",voteSelection);
voteSelection.setPosition(screenWidth // 2 - voteSelection.getWidth() // 2, screenHeight//2);

## The ingame topbar ##

topBar = GameTopBar();
glass.GUI_ScreenAddWidget("hud",topBar);
topBar.setVisible(False);

def updateGold():
	player = savage.getLocalPlayer();
	gold = player.getGold();
	if gold != None:
		hud.player_money.setCaption("^icon ../../gui/standard/icons/gold/gold_icon^" + str(gold));
	else: hud.player_money.setCaption("");

def updateHealth():
	player = savage.getLocalPlayer();
	healthProportion = player.getHealthPct()
	
	hud.healthValue.setCaption( str(player.getHealth() ));
	hud.healthForeground.setHeight( int( hud.healthBackground.getHeight()*healthProportion ) );
	hud.healthForeground.setY( hud.healthBackground.getHeight() + hud.healthBackground.getY() - hud.healthForeground.getHeight() );

def updateGameStatus():
	status = cvar_get("game_serverStatus")
	if len(status)>0:
		hud.gamestatus.setCaption(" %s " % (status))
		hud.gamestatusWindow.setVisible(True);
	else:
		hud.gamestatus.setCaption("");
		hud.gamestatusWindow.setVisible(False);
	hud.gamestatus.adjustSize()
	hud.gamestatusWindow.setSize(hud.gamestatus.getWidth(), hud.gamestatus.getHeight());
	hud.gamestatusWindow.setPosition(screenWidthPct(0.5)-hud.gamestatusWindow.getWidth()//2, hud.gamestatusWindow.getY())

def updateCrosshairLimits():
	player = savage.getLocalPlayer();
	player_objType = player.getType();
	xmin = player_objType.getValue("minAimX");
	xmax = player_objType.getValue("maxAimX");
	ymin = player_objType.getValue("minAimY");
	ymax = player_objType.getValue("maxAimY");
	
	hud.crosshairLimits.setPosition(int( screenWidth * xmin) - hud.crosshairLimitsPadding , int( screenHeight * ymin) - hud.crosshairLimitsPadding );
	hud.crosshairLimits.setWidth(int( screenWidth * (xmax-xmin)) + 2*hud.crosshairLimitsPadding);
	hud.crosshairLimits.setHeight(int( screenHeight * (ymax-ymin))+ 2*hud.crosshairLimitsPadding);

nonSpecWidgets = [ hpDisplay , stamina, inventory, stateContainer, player_money, crosshairLimits ];

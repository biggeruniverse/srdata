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
		hud.timer.setCaption("^icon ../../gui/standard/icons/timer^" + gametime);
		hud.timer.adjustSize();
	else:
		hud.timer.setCaption("");
	
	player = savage.getLocalPlayer();
	
	hud.teamStatus.update();
	hud.updateGold();
	hud.updateHealth();
	hud.updateStamina();
	hud.updateInventory();
	hud.stateContainer.update();
	hud.updateCrosshairLimits();
	hud.minimap.setAlpha(int(cvar_getvalue('cl_minimap_brightness')*255));
	hud.updateWaypoint();
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
	
	hud.frame(); #remove any other placeholders

glass.GUI_CreateScreen('hud');

## ORDER/WAYPOINT ##
waypoint = glass.GlassLabel();
waypoint.setImage("null.s2g");
waypoint.setVisible(0);
waypoint.setSize(48,48);
glass.GUI_ScreenAddWidget("hud", waypoint);
waypointObject = None;

class WaypointHandler:
	def onEvent(self, e):
		if isinstance(e, WaypointEvent):
			if e.eventType == 'waypoint_complete' or e.eventType == 'waypoint_cancel' or e.eventType == 'waypoint_destroy':
				hud.waypoint.setVisible(0);
			else:
				hud.waypoint.setImage(CL_GetWaypointImage());
				hud.waypoint.setSize(48,48);
				hud.waypoint.setVisible(1);
				if e.targetId != -1:
					hud.waypointObject = savage.getGameObject(e.targetId);
				else:
					hud.waypointObject = None;

gblEventHandler.addGameListener(WaypointHandler());


#starting from the gold to the right of the minimap and proceeding anti clockwise

## MAP and surrounding things ##

minimap = glass.GlassMiniMap();
minimap.setPositionPct(0,0.025)
minimap.setX(10);
minimap.setSize(int(0.208*screenHeight),int(0.208*screenHeight));
#same number of pixels so it's square
#well assuming the pixel aspect ratio is 1:1
glass.GUI_ScreenAddWidget("hud",minimap);

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
teamStatus.setVisible(0);
glass.GUI_ScreenAddWidget("hud", teamStatus);

## CHAT ##

chatBox = HUDChatBox();
glass.GUI_ScreenAddWidget("hud", chatBox);

chatBox.setPositionPct(0,0.625);
chatBox.setX(10);
chatBox.setSizePct(0.4,0.21);
chatBox.resize();


## HEALTH DISPLAY ##

healthBackground = glass.GlassLabel();
healthBackground.setBackgroundColor( glass.Color(133,11,10) );
healthBackground.setOpaque(1);
healthBackground.setSizePct(0.012,0.13);
healthBackground.setPosition( 10, screenHeight - 10 - healthBackground.getHeight());
glass.GUI_ScreenAddWidget("hud",healthBackground);

healthForeground = glass.GlassLabel();
healthForeground.setOpaque(1);
healthForeground.setBackgroundColor( glass.Color(255,21,22) );
healthForeground.setSizePct(0.012,0.13);
healthForeground.setPosition( healthBackground.getX(), healthBackground.getY());
glass.GUI_ScreenAddWidget("hud",healthForeground);

healthValue = glass.GlassLabel("00000");
healthValue.setFont(glass.GUI_GetFont(20));
healthValue.setForegroundColor( glass.Color(255,137,137) );
healthValue.setPosition( 20 + healthBackground.getWidth() , screenHeight - 10 - healthValue.getHeight(), );
glass.GUI_ScreenAddWidget("hud",healthValue);

## STATE EFFECT DISPLAY ##

stateContainer = StateDisplay();
#stateContainer.setX( healthValue.getX() + healthValue.getWidth() + 15 );
stateContainer.setX( (screenWidth - stateContainer.getWidth() )//2 );
stateContainer.setY( screenHeight - 10 - stateContainer.getHeight() );
glass.GUI_ScreenAddWidget("hud",stateContainer);

## VOICE CHAT ##

voiceChat = VoiceChatBox();
voiceChat.setSizePct(0.3,0.35);
voiceChat.table.adjustSizeToPct(1,1);
glass.GUI_ScreenAddWidget("hud",voiceChat);
voiceChat.centerWindow();
voiceChat.setY(screenHeight/2+40);

## STAMINA DISPLAY ##

staminaBackground = glass.GlassLabel();
staminaBackground.setBackgroundColor( glass.Color(10,115,110) );
staminaBackground.setOpaque(1);
staminaBackground.setSizePct(0.012,0.13);
staminaBackground.setPosition( screenWidth - staminaBackground.getWidth() - 10, healthBackground.getY() );
glass.GUI_ScreenAddWidget("hud",staminaBackground);

staminaForeground = glass.GlassLabel();
staminaForeground.setOpaque(1);
staminaForeground.setBackgroundColor( glass.Color(20,255,248) );
staminaForeground.setSizePct(0.012,0.13);
staminaForeground.setPosition( staminaBackground.getX(), staminaBackground.getY());
glass.GUI_ScreenAddWidget("hud",staminaForeground);

## INVENTORY ##

inventory = glass.GlassContainer();
inventory.setSize(int( 0.26*screenHeight ), int( 0.052*screenHeight ) );
inventory.setPosition( staminaBackground.getX() - 10 - inventory.getWidth() , screenHeight - 10 - inventory.getHeight());
inventory.setOpaque(0);
glass.GUI_ScreenAddWidget("hud", inventory);

inventorySlots = [];
inventoryAmmos = [];
for i in range(5):
	slot = glass.GlassLabel();
	slot.setSize( int( 0.052*screenHeight ) , int( 0.052*screenHeight ) );
	slot.setPosition( i*slot.getWidth(), 0);
	slot.setOpaque(1);
	slot.setBackgroundColor( black );
	inventorySlots.append(slot);
	inventory.add(slot);
	
	ammo = glass.GlassLabel("999");
	ammo.setForegroundColor(white);
	ammo.setAlignment(2);
	ammo.setPosition( slot.getX() + slot.getWidth() - ammo.getWidth() - 1 , slot.getY() + slot.getHeight() - ammo.getHeight() - 1);
	
	inventoryAmmos.append(ammo);
	inventory.add(ammo);

slot = inventorySlots[0];
invselected = glass.GlassLabel();
invselected.setImage("/gui/standard/icons/inventory_selected.s2g")
invselected.setSize( slot.getWidth() , slot.getHeight());
invselected.setPosition( slot.getX(), slot.getY() );
inventory.add(invselected);

## RANGED AMMO ##

ammoGraphic = glass.GlassLabel();
ammoGraphic.setImage("/gui/standard/icons/comm_crown.s2g");
ammoGraphic.setSize( int( 0.60*slot.getHeight() ) , int( 0.60*slot.getHeight() ));
ammoGraphic.setPosition( inventory.getX() - 10 - ammoGraphic.getWidth() , screenHeight - ammoGraphic.getHeight()- 10);
ammoGraphic.setOpaque(1);
glass.GUI_ScreenAddWidget("hud", ammoGraphic);

ammoValue = glass.GlassLabel("999");
ammoValue.setForegroundColor( white );
ammoValue.setAlignment(2);
ammoValue.setPosition( ammoGraphic.getX() - 2 - ammoValue.getWidth(),  screenHeight - ammoValue.getHeight() - 10 );
glass.GUI_ScreenAddWidget("hud", ammoValue);

## NOTIFICATIONS ##
scroll = glass.GlassScrollArea();
scroll.setAutoscroll(1);
scroll.setSizePct(0.32,0.16);
scroll.setPosition(screenWidth-scroll.getWidth() - 10,10);
scroll.setPosition(screenWidth-360, 10);
scroll.setScrollPolicy(1,1); #SHOW_NEVER
glass.GUI_ScreenAddWidget("hud", scroll);

notifyBuffer = MessageBuffer(["notify"]); #TODO notify_generalhide too?
scroll.setContent(notifyBuffer);
notifyBuffer.setSize(scroll.getWidth(), scroll.getHeight());
notifyBuffer.setFadeTop(1);
notifyBuffer.setFadeBottom(0);
notifyBuffer.showTime(0);
for i in range(10):
	notifyBuffer.addRow(" ");

## VOTES ##

voteWindow = VoteInfoBox();
glass.GUI_ScreenAddWidget("hud", voteWindow);
voteWindow.setPosition( minimap.getWidth() + minimap.getX() + 10, -voteWindow.getHeight());

# Finally objects in the screen's center, proceeding from the top downward

## GAME STATUS ##

gamestatus = glass.GlassLabel()
gamestatus.setPositionPct(.5,.35)
gamestatus.setBackgroundColor(glass.Color(0,0,0,50))
gamestatus.setForegroundColor(glass.Color(255,255,255))
gamestatus.setOpaque(1)
glass.GUI_ScreenAddWidget("hud",gamestatus);

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

graphicspanel = GraphicsPanel();
graphicspanel.setPositionPct(0.4,0.1);
glass.GUI_ScreenAddWidget("hud",graphicspanel);

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

def updateStamina():
	player = savage.getLocalPlayer();
	staminaProportion = player.getStaminaPct();
	
	hud.staminaForeground.setHeight( int( hud.staminaBackground.getHeight()*staminaProportion) );
	hud.staminaForeground.setY( hud.staminaBackground.getHeight() + hud.staminaBackground.getY() - hud.staminaForeground.getHeight() );

def updateInventory():
	#see also loadout's updateInventory, it's similar
	player = savage.getLocalPlayer();
	primaryRanged = None;
	
	for i in range(5):
		slot_objType = player.getInventorySlot( i );
		slot = hud.inventorySlots[i];
		w, h = slot.getWidth() , slot.getHeight();
		ammo = hud.inventoryAmmos[i];
		ammoCount = "";
		
		if slot_objType != None:
			slot.setImage(slot_objType.getValue("icon")+".s2g");
			
			if slot_objType.isManaWeapon():
				ammoCount = str(player.getManaUsesSlot(i));
			else: ammoCount = str(player.getAmmoSlot(i));
			if ammoCount == "None":
				ammoCount = "";

			if primaryRanged == None and slot_objType.isWeaponType() :
				primaryRanged = i;
				primaryAmmo = ammoCount;
		
		else: #empty slot
			slot.setImage("/textures/black.s2g");
		
		ammo.setCaption( ammoCount );
		slot.setSize( w, h);
	
	currentSlotIndex = player.getCurrentInventorySlotIndex();
	slotWidget = hud.inventorySlots[ currentSlotIndex ];
	hud.invselected.setPosition( slotWidget.getX(), slotWidget.getY() );
	
	if primaryRanged != None:
		slot_objType = player.getInventorySlot(primaryRanged);
		w, h = hud.ammoGraphic.getWidth(), hud.ammoGraphic.getHeight();
		hud.ammoValue.setCaption( primaryAmmo );
		if slot_objType.isManaWeapon():
			pass;
			#hud.ammoGraphic.setImage( glorious mana icon );
		else: #it must use ammo
			pass;
			#hud.ammoGraphic.setImage( glorious ammunition icon );
		hud.ammoGraphic.setSize( w, h);
		hud.ammoValue.setVisible(1);
		hud.ammoGraphic.setVisible(1);
	else:
		hud.ammoValue.setVisible(0);
		hud.ammoGraphic.setVisible(0);

def updateWaypoint():
	x,y = 0,0;
	if hud.waypointObject == None:
		x,y = CL_GetWaypointPosition();
	else:
		x,y = savage.go_getscreenposition(hud.waypointObject.objectId);

	hud.waypoint.setPosition(int(x-24), int(y-24));

def updateGameStatus():
	status = cvar_get("game_serverStatus")
	if len(status)>0:
		hud.gamestatus.setCaption(" "+status+" ")
		hud.gamestatus.setVisible(1);
	else:
		hud.gamestatus.setCaption("");
		hud.gamestatus.setVisible(0);
	hud.gamestatus.adjustSize()
	hud.gamestatus.setPosition(screenWidth/2-hud.gamestatus.getWidth()/2, hud.gamestatus.getY())

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

nonSpecWidgets = [ healthForeground, healthBackground , healthValue , staminaBackground, staminaForeground , inventory , invselected, stateContainer, ammoGraphic, ammoValue, player_money, crosshairLimits ];

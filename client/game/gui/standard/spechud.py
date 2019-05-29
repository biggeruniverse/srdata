# (c) 2010 savagerebirth.com
# this file creates the heads-up display

from silverback import *;
import savage;
import glass;

def frame():
	gametime = getGameTimeString(cvar_getvalue("game_timeLimitSeconds"));
	if gametime != "":
		if cvar_getvalue("game_timeLimitSeconds") < 45:
			gametime = "^900"+gametime;
		spechud.timer.setCaption("^icon ../../gui/standard/icons/timer^" + gametime);
		spechud.timer.adjustSize();
	else:
		spechud.timer.setCaption("");
	
	player = savage.getLocalPlayer();
	 #when spectating someone bu has said this will represent the spectee and not the spectator
	 #I hope it does
	if player.getTeam() != 0:
		for widget in spechud.nonSpecWidgets:
			widget.setVisible(True);
		spechud.teamStatus.update();
		spechud.updateGold();
		spechud.updateHealth();
		spechud.updateStamina();
		spechud.updateInventory();
		spechud.stateContainer.update();
		spechud.updateCrosshairLimits();
		spechud.researchinfowindow1.setVisible(False);
		spechud.researchinfowindow2.setVisible(False);
		spechud.unitinfowindow1.setVisible(False);
		spechud.unitinfowindow2.setVisible(False);
		spechud.teamStats.setVisible(False);
		
	else:
		for widget in spechud.nonSpecWidgets:
			widget.setVisible(False);
		spechud.teamStatus.setVisible(False);
		spechud.compass.setVisible(False);
		if spechud.researchinfowindow1.isVisible():
			spechud.researchinfowindow1.updateResearch();
		if spechud.researchinfowindow2.isVisible():
			spechud.researchinfowindow2.updateResearch();
		spechud.unitinfowindow1.updateUnitInfo();
		spechud.unitinfowindow2.updateUnitInfo();
		
	spechud.updateTeamStats();
	spechud.updateGameStatus();
	spechud.crosshair.update();
	spechud.voteWindow.frame();
	if spechud.scoreboard.isVisible(): 
		spechud.scoreboard.update();
	spechud.compass.update();
	spechud.fpswindow.update();
	

def onShow():
	spechud.chatBox.deactivate();
	spechud.minimap.setMap(cvar_get("world_overhead"));
	spechud.scoreboard.arrange();
	spechud.scoreboard.update(); #remove the placeholders in scoreboard
	spechud.crosshair.reset();
	spechud.researchinfowindow1.rebuildResearchable(spechud.team1);
	spechud.researchinfowindow2.rebuildResearchable(spechud.team2);
	spechud.unitinfowindow1.buildUnitInfo(spechud.team1);
	spechud.unitinfowindow2.buildUnitInfo(spechud.team2);
	
	spechud.frame(); #remove any other placeholders

glass.GUI_CreateScreen('spechud');

## Defining both teams here as they should not change
team1 = savage.Team(1);
team2 = savage.Team(2);

#starting from the gold to the right of the minimap and proceeding anti clockwise

## MAP and surrounding things ##

minimap = glass.GlassMiniMap();
minimap.setPositionPct(0,0.025)
minimap.setX(10);
minimap.setSize(int(0.208*screenHeight),int(0.208*screenHeight));
#same number of pixels so it's square
#well assuming the pixel aspect ratio is 1:1
glass.GUI_ScreenAddWidget("spechud",minimap);

player_money = glass.GlassLabel("_ABCDE ");
player_money.setForegroundColor(gold);
player_money.setPosition( int(minimap.getWidth() + 10 + screenWidth*0.01875), int(screenHeight*0.025));
glass.GUI_ScreenAddWidget("spechud", player_money);

timer = glass.GlassLabel("_AB:CD ");
timer.setFont(glass.GUI_GetFont(20));
timer.setPosition(10, minimap.getHeight() + 20);
glass.GUI_ScreenAddWidget("spechud", timer);

## TEAM STATUS ##

teamStatus = ResourcePanel();
teamStatus.setVisible(False);
glass.GUI_ScreenAddWidget("spechud", teamStatus);

## TEAM STATS ##

teamStats = glass.GlassContainer();
teamStats.setBackgroundColor( glass.Color(0,0,0,128));
teamStats.setSizePct( 1 , 0.025);
teamStats.setPosition(0,0);
glass.GUI_ScreenAddWidget("spechud", teamStats);

team1healthBackground = glass.GlassLabel(" ");
teamStats.add(team1healthBackground);
team1healthBackground.setPositionPct(0.025,0.05);
team1healthBackground.setSizePct(0.2,0.9);
team1healthBackground.setBackgroundColor(tangoRedDark);
team1healthBackground.setOpaque(1);
		
team1healthForeground = glass.GlassLabel(" ")
teamStats.add(team1healthForeground);
team1healthForeground.setPositionPct(0.025,0.05);
team1healthForeground.setSizePct(0.2,0.9);
team1healthForeground.setBackgroundColor(tangoBlue);
team1healthForeground.setOpaque(1);
	
team1cc = glass.GlassLabel("");
teamStats.add(team1cc);
team1cc.setSizePct(0,1);
team1cc.setWidth(team1cc.getHeight());
team1cc.setX( team1healthBackground.getX() - team1cc.getWidth() );

team2healthBackground = glass.GlassLabel(" ");
teamStats.add(team2healthBackground);
team2healthBackground.setPositionPct(0.775,0.05);
team2healthBackground.setSizePct(0.2,0.9);
team2healthBackground.setBackgroundColor(tangoRedDark);
team2healthBackground.setOpaque(1);
		
team2healthForeground = glass.GlassLabel(" ")
teamStats.add(team2healthForeground);
team2healthForeground.setPositionPct(0.775,0.05);
team2healthForeground.setSizePct(0.2,0.9);
team2healthForeground.setBackgroundColor(tangoBlue);
team2healthForeground.setOpaque(1);
	
team2cc = glass.GlassLabel("");
teamStats.add(team2cc);
team2cc.setSizePct(0,1);
team2cc.setWidth(team2cc.getHeight());
team2cc.setX( team2healthBackground.getX() + team2healthBackground.getWidth() );

team1Gold = glass.GlassLabel("_12345 ");
team1Gold.setForegroundColor(gold);
teamStats.add(team1Gold);
team1Gold.setPositionPct(0.25,0);
team1Gold.setSizePct(0.1,1);

team1Stone = glass.GlassLabel("_12345__");
team1Stone.setForegroundColor( tangoRedLight);
teamStats.add(team1Stone);
team1Stone.setPositionPct(0.325,0);
team1Stone.setSizePct(0.1,1);

team2Gold = glass.GlassLabel("_12345 ");
team2Gold.setForegroundColor(gold);
teamStats.add(team2Gold);
team2Gold.setPositionPct(0.675,0);
team2Gold.setSizePct(0.1,1);

team2Stone = glass.GlassLabel("_12345__");
team2Stone.setForegroundColor( tangoRedLight);
teamStats.add(team2Stone);
team2Stone.setPositionPct(0.6,0);
team2Stone.setSizePct(0.1,1);

teamScore = glass.GlassLabel("_1234/_1234 vs _1234/_1234");
teamScore.setAlignment(glass.Graphics.CENTER);
teamStats.add(teamScore);
teamScore.setSizePct(0.2,1);
teamScore.setPositionPct(0.4,0);

## CHAT ##

chatBox = HUDChatBox();
glass.GUI_ScreenAddWidget("spechud", chatBox);

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
glass.GUI_ScreenAddWidget("spechud",healthBackground);

healthForeground = glass.GlassLabel();
healthForeground.setOpaque(1);
healthForeground.setBackgroundColor( glass.Color(255,21,22) );
healthForeground.setSizePct(0.012,0.13);
healthForeground.setPosition( healthBackground.getX(), healthBackground.getY());
glass.GUI_ScreenAddWidget("spechud",healthForeground);

healthValue = glass.GlassLabel("00000");
healthValue.setFont(glass.GUI_GetFont(20));
healthValue.setForegroundColor( glass.Color(255,137,137) );
healthValue.setPosition( 20 + healthBackground.getWidth() , screenHeight - 10 - healthValue.getHeight(), );
glass.GUI_ScreenAddWidget("spechud",healthValue);

## STATE EFFECT DISPLAY ##

stateContainer = StateDisplay();
#stateContainer.setX( healthValue.getX() + healthValue.getWidth() + 15 );
stateContainer.setX( (screenWidth - stateContainer.getWidth() )//2 );
stateContainer.setY( screenHeight - 10 - stateContainer.getHeight() );
glass.GUI_ScreenAddWidget("spechud",stateContainer);

## VOICE CHAT ##

voiceChat = VoiceChatBox();
voiceChat.setSizePct(0.3,0.35);
voiceChat.table.adjustSizeToPct(1,1);
glass.GUI_ScreenAddWidget("spechud",voiceChat);
voiceChat.centerWindow();
voiceChat.setY(screenHeight/2+40);

## STAMINA DISPLAY ##

staminaBackground = glass.GlassLabel();
staminaBackground.setBackgroundColor( glass.Color(10,115,110) );
staminaBackground.setOpaque(1);
staminaBackground.setSizePct(0.012,0.13);
staminaBackground.setPosition( screenWidth - staminaBackground.getWidth() - 10, healthBackground.getY() );
glass.GUI_ScreenAddWidget("spechud",staminaBackground);

staminaForeground = glass.GlassLabel();
staminaForeground.setOpaque(1);
staminaForeground.setBackgroundColor( glass.Color(20,255,248) );
staminaForeground.setSizePct(0.012,0.13);
staminaForeground.setPosition( staminaBackground.getX(), staminaBackground.getY());
glass.GUI_ScreenAddWidget("spechud",staminaForeground);

## INVENTORY ##

inventory = glass.GlassContainer();
inventory.setSize(int( 0.26*screenHeight ), int( 0.052*screenHeight ) );
inventory.setPosition( staminaBackground.getX() - 10 - inventory.getWidth() , screenHeight - 10 - inventory.getHeight());
inventory.setOpaque(0);
glass.GUI_ScreenAddWidget("spechud", inventory);

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
glass.GUI_ScreenAddWidget("spechud", ammoGraphic);

ammoValue = glass.GlassLabel("999");
ammoValue.setForegroundColor( white );
ammoValue.setAlignment(2);
ammoValue.setPosition( ammoGraphic.getX() - 2 - ammoValue.getWidth(),  screenHeight - ammoValue.getHeight() - 10 );
glass.GUI_ScreenAddWidget("spechud", ammoValue);

## NOTIFICATIONS ##
scroll = glass.GlassScrollArea();
scroll.setAutoscroll(1);
scroll.setSizePct(0.32,0.16);
scroll.setPosition(screenWidth-scroll.getWidth() - 10,10);
scroll.setPosition(screenWidth-360, 10);
scroll.setScrollPolicy(1,1); #SHOW_NEVER
glass.GUI_ScreenAddWidget("spechud", scroll);

notifyBuffer = MessageBuffer(["notify", "notifyhide"]); #notify_generalhide too?
scroll.setContent(notifyBuffer);
notifyBuffer.setSize(scroll.getWidth(), scroll.getHeight());
notifyBuffer.setFadeTop(1);
notifyBuffer.setFadeBottom(0);
notifyBuffer.showTime(0);
for i in range(10):
	notifyBuffer.addRow(" ");

## COMPASS ##

compass = HUDCompass();
compass.setPosition( (screenWidth - compass.getWidth() )/2, 0);
glass.GUI_ScreenAddWidget("spechud", compass);

## ORDER/WAYPOINT ##

## VOTES ##

voteWindow = VoteInfoBox();
glass.GUI_ScreenAddWidget("spechud", voteWindow);
voteWindow.setPosition( minimap.getWidth() + minimap.getX() + 10, -voteWindow.getHeight());

# Finally objects in the screen's center, proceeding from the top downward

## GAME STATUS ##

gamestatus = glass.GlassLabel()
gamestatus.setPositionPct(.5,.35)
gamestatus.setBackgroundColor(glass.Color(0,0,0,50))
gamestatus.setForegroundColor(glass.Color(255,255,255))
gamestatus.setOpaque(1)
glass.GUI_ScreenAddWidget("spechud",gamestatus);


## CROSSHAIR ##

crosshair = HUDCrossHair();
glass.GUI_ScreenAddWidget("spechud",crosshair);

crosshairLimits = glass.GlassLabel("");
crosshairLimits.setBaseColor( white );
crosshairLimits.setSize(0,0);
crosshairLimits.setFrameSize(4);
glass.GUI_ScreenAddWidget("spechud",crosshairLimits);

crosshairLimitsPadding = crosshair.crosshair.getWidth()//2;

### SCOREBAORD ##

scoreboard = TeamScore();
glass.GUI_ScreenAddWidget("spechud",scoreboard);

## FPS WINDOW ##

fpswindow = FpsWindow();
fpswindow.setPositionPct(0, 0.5);
glass.GUI_ScreenAddWidget("spechud",fpswindow);

## Graphics Panel ##

graphicspanel = GraphicsPanel();
graphicspanel.setPositionPct(0.4,0.1);
glass.GUI_ScreenAddWidget("spechud",graphicspanel);

## Show Research and Units of both teams ##

researchinfowindow1 = ResearchInfoWindow(); # Show research for team 1 here
glass.GUI_ScreenAddWidget("spechud",researchinfowindow1);
researchinfowindow1.setPositionPct(0.02,0.4);

researchinfowindow2 = ResearchInfoWindow(); # Show research for team 2 here
glass.GUI_ScreenAddWidget("spechud",researchinfowindow2);
researchinfowindow2.setPositionPct(0.7,0.4);

unitinfowindow1 = UnitInfoWindow();
glass.GUI_ScreenAddWidget("spechud",unitinfowindow1);
unitinfowindow1.setPosition(minimap.getX(), timer.getY()+timer.getHeight() + 10);

unitinfowindow2 = UnitInfoWindow();
glass.GUI_ScreenAddWidget("spechud",unitinfowindow2);
unitinfowindow2.setPosition(researchinfowindow2.getX(), unitinfowindow1.getY());

def updateGold():
	player = savage.getLocalPlayer();
	gold = player.getGold();
	if gold != None:
		spechud.player_money.setCaption("^icon ../../gui/standard/icons/gold/gold_icon^" + str(gold));
	else: spechud.player_money.setCaption("");

def updateHealth():
	player = savage.getLocalPlayer();
	healthProportion = player.getHealthPct()
	
	spechud.healthValue.setCaption( str(player.getHealth() ));
	spechud.healthForeground.setHeight( int( spechud.healthBackground.getHeight()*healthProportion ) );
	spechud.healthForeground.setY( spechud.healthBackground.getHeight() + spechud.healthBackground.getY() - spechud.healthForeground.getHeight() );

def updateStamina():
	player = savage.getLocalPlayer();
	staminaProportion = player.getStaminaPct();
	
	spechud.staminaForeground.setHeight( int( spechud.staminaBackground.getHeight()*staminaProportion) );
	spechud.staminaForeground.setY( spechud.staminaBackground.getHeight() + spechud.staminaBackground.getY() - spechud.staminaForeground.getHeight() );

def updateInventory():
	#see also loadout's updateInventory, it's similar
	player = savage.getLocalPlayer();
	primaryRanged = None;
	
	for i in range(5):
		slot_objType = player.getInventorySlot( i );
		slot = spechud.inventorySlots[i];
		w, h = slot.getWidth() , slot.getHeight();
		ammo = spechud.inventoryAmmos[i];
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
	slotWidget = spechud.inventorySlots[ currentSlotIndex ];
	spechud.invselected.setPosition( slotWidget.getX(), slotWidget.getY() );
	
	if primaryRanged != None:
		slot_objType = player.getInventorySlot(primaryRanged);
		w, h = spechud.ammoGraphic.getWidth(), spechud.ammoGraphic.getHeight();
		spechud.ammoValue.setCaption( primaryAmmo );
		if slot_objType.isManaWeapon():
			pass;
			#spechud.ammoGraphic.setImage( glorious mana icon );
		else: #it must use ammo
			pass;
			#spechud.ammoGraphic.setImage( glorious ammunition icon );
		spechud.ammoGraphic.setSize( w, h);
		spechud.ammoValue.setVisible(True);
		spechud.ammoGraphic.setVisible(True);
	else:
		spechud.ammoValue.setVisible(False);
		spechud.ammoGraphic.setVisible(False);


def updateGameStatus():
	status = cvar_get("game_serverStatus")
	if len(status)>0:
		spechud.gamestatus.setCaption(" "+status+" ")
		spechud.gamestatus.setVisible(True);
	else:
		spechud.gamestatus.setCaption("");
		spechud.gamestatus.setVisible(False);
	spechud.gamestatus.adjustSize()
	spechud.gamestatus.setPosition(screenWidth/2-spechud.gamestatus.getWidth()/2, spechud.gamestatus.getY())

def updateCrosshairLimits():
	player = savage.getLocalPlayer();
	player_objType = player.getType();
	xmin = player_objType.getValue("minAimX");
	xmax = player_objType.getValue("maxAimX");
	ymin = player_objType.getValue("minAimY");
	ymax = player_objType.getValue("maxAimY");
	
	spechud.crosshairLimits.setPosition(int( screenWidth * xmin) - spechud.crosshairLimitsPadding , int( screenHeight * ymin) - spechud.crosshairLimitsPadding );
	spechud.crosshairLimits.setWidth(int( screenWidth * (xmax-xmin)) + 2*spechud.crosshairLimitsPadding);
	spechud.crosshairLimits.setHeight(int( screenHeight * (ymax-ymin))+ 2*spechud.crosshairLimitsPadding);
	
def updateTeamStats():		
		
	resources1 = spechud.team1.getResources();
	resources2 = spechud.team2.getResources();	
	team1kills = str(spechud.team1.getKills());
	team1deaths = str(spechud.team1.getDeaths());
	team2kills = str(spechud.team2.getKills());
	team2deaths = str(spechud.team2.getDeaths());
	
	spechud.teamScore.setCaption("^g" + team1kills + "^w/^r" + team1deaths + " ^wvs ^g" + team2kills + "^w/^r" + team2deaths);
	
	spechud.team1Gold.setCaption("^icon ../../gui/standard/icons/gold/gold_icon^ "+str(resources1["gold"]));
	spechud.team1Stone.setCaption("^icon ../../gui/standard/icons/redstone^ "+str(resources1["stone"]));	
	spechud.team2Gold.setCaption("^icon ../../gui/standard/icons/gold/gold_icon^ "+str(resources2["gold"]));
	spechud.team2Stone.setCaption("^icon ../../gui/standard/icons/redstone^ "+str(resources2["stone"]));
	
	cc1 = spechud.team1.getCommandCenter();
	k1 = cc1.getHealthPct();
	cc2 = spechud.team2.getCommandCenter();
	k2 = cc2.getHealthPct();	
	hue1 = (k1-0.1)/2.7 if k1 > 0.1 else 0;
	hue2 = (k2-0.1)/2.7 if k2 > 0.1 else 0;
	
	spechud.team1healthForeground.setWidth(int(k1*spechud.team1healthBackground.getWidth()));
	spechud.team1healthForeground.setBackgroundColor(tools.HSLColor(hue1,0.8,0.66));
	w1,h1 = spechud.team1cc.getWidth(), spechud.team1cc.getHeight();
	spechud.team1cc.setImage(cc1.getType().getValue("mapIcon"));
	spechud.team1cc.setSize(w1,h1);	
	spechud.team2healthForeground.setWidth(int(k2*spechud.team2healthBackground.getWidth()));
	spechud.team2healthForeground.setBackgroundColor(tools.HSLColor(hue2,0.8,0.66));
	w2,h2 = spechud.team2cc.getWidth(), spechud.team2cc.getHeight();
	spechud.team2cc.setImage(cc2.getType().getValue("mapIcon"));
	spechud.team2cc.setSize(w2,h2);
	
nonSpecWidgets = [ healthForeground, healthBackground , healthValue , staminaBackground, staminaForeground , inventory , invselected, stateContainer, ammoGraphic, ammoValue, player_money, crosshairLimits ];

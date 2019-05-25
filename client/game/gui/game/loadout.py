# (c) 2012 savagerebirth.com
# it's called loadout in the code :P

from silverback import *;
import glass;
import savage;

def frame():
	player = savage.getLocalPlayer();
	team = savage.getTeamObject(player.getTeam());
	
	if team.getRace() == "human":
		loadout.activeWindow = loadout.humanLoadout;
		loadout.beastLoadout.setVisible(0);
	else:
		loadout.activeWindow = loadout.beastLoadout;
		loadout.humanLoadout.setVisible(0);
	
	gblPresetManager.setY( loadout.activeWindow.presetsY+loadout.activeWindow.getY());
	gblPresetManager.setX( loadout.activeWindow.getX()+10);
	#gblPresetManager.requestMoveToTop();
		
	loadout.activeWindow.setVisible(1);
	loadout.activeWindow.update();
	loadout.expWindow.update();

def onShow():
	GUI_ShowCursor("arrow");

	gblPresetManager.reloadPresets();
	gblPresetManager.execute();
	
	loadout.frame();

	loadout.mapWindow.setAlpha(0);
	loadout.mapWindow.setVisible(0);
	
## CLASS DEFINITIONS ##
class SpawnSelectHandler:
	def onEvent(self, e):
		if(e.eventType == 'spawnselect'):
			loadout.mapWindow.show();

class LoadoutTechButton(DefaultContainer):
	def __init__(self, t):
		DefaultContainer.__init__(self);
		import loadout;
		self.objtype = savage.getObjectType(t);

		self.setSize(int(screenHeight*0.0625), int(screenHeight*0.09375));
		
		#self.image = glass.GlassProgressDisc();
		self.image = DefaultImage();
		self.image.setImage("../../../"+ self.objtype.getValue("icon")+".s2g");
		self.image.setSize(int(screenHeight*0.0625), int(screenHeight*0.0625));
		self.add(self.image);
		
		self.request = DefaultImageButton();
		self.request.setImage("request.s2g");
		self.request.setSize(int(screenHeight*0.0625), int(screenHeight*0.0625));
		self.request.setVisible(0);
		self.add(self.request);

		self.maxDeployment = DefaultLabel();
		self.maxDeployment.setCaption("00");
		self.maxDeployment.setForegroundColor(tangoGreen);
		self.add(self.maxDeployment,"right", "top");
		
		self.price = DefaultLabel();
		p = str(self.objtype.getValue("playerCost"));
		if p == "0":
			p = "FREE";
		else:
			p = p + "^w^icon ../../gui/standard/icons/gold/gold_icon^";

		self.price.setCaption("^l" + p);
		self.price.setFont(fontSizeSmall);
		self.add(self.price, "center", int(screenHeight*0.0625));

		button = glass.ImageButton("textures/econs/transparent.s2g");
		self.add( button );
		button.setSizePct(1,1);
		
		button.addActionListener(self);

	def update(self):
		player = savage.getLocalPlayer();
		team = savage.getTeamObject(player.getTeam());
		
		self.setAlpha(255);
		self.image.setAlpha(255);
		self.request.setVisible(0);
		
		if not self.objtype.isResearched():
			self.setVisible(0);
		else:
			self.setVisible(1);
			
		#self.image.setProgress(1.0);
		if self.objtype in team.getResearch():
			self.setVisible(1);
			for r in team.getResearch():
				if r == self.objtype:
					con_println("progressing \n")
					self.image.setProgress(r.getBuildProgress());
					break;
			
		if player.getGold() < self.objtype.getValue("playerCost"):
			self.request.setVisible(1);
			if self.objtype.isWeaponType():
				obj1 = player.getInventorySlot(1);
				if obj1 is not None and player.getGold() + obj1.getValue("playerCost") >= self.objtype.getValue("playerCost"):
					self.request.setVisible(0);

		self.maxDeployment.setCaption("");
		if self.objtype.getValue("maxDeployment") > 0:
			md = self.objtype.getValue("maxDeployment")-team.getDeployedCount(self.objtype.typeId);
			self.maxDeployment.setCaption(str(md).rjust(2));

	def onAction(self, e):
		refund = 0;
		player = savage.getLocalPlayer();
		
		if not self.objtype.isResearched():
			return;
			
		if self.objtype.isWeaponType():
			obj1 = player.getInventorySlot(1);
			if obj1 is not None:
				refund += obj1.getValue("playerCost");
			CL_RequestGiveback(0);
			CL_RequestGiveback(1);
			
		if player.getGold()+refund < self.objtype.getValue("playerCost"):
			CL_RequestGrant(self.objtype.getName());
		else:
			CL_RequestGive(self.objtype.getName());

class LoadoutInventoryButton(DefaultContainer):
	def __init__(self, slot):
		DefaultContainer.__init__(self);
		
		self.setSize(screenWidthPct(0.0625), screenWidthPct(0.0625));
		self.setBackgroundColor(glass.Color(0,0,0,128));
		
		self.slot = slot;
		self.image = DefaultImageButton();
		self.add(self.image);
		self.image.setSizePct(1,1);

		self.ammo = DefaultLabel();
		self.ammo.setForegroundColor(tangoGreen);
		self.add(self.ammo);
		
		button = glass.ImageButton("textures/econs/transparent.s2g");
		self.add( button );
		button.setSizePct(1,1);
		
		button.addActionListener(self);

	def update(self):
		player = savage.getLocalPlayer();
		objType = player.getInventorySlot(self.slot);
		
		if objType is not None:
			self.image.setVisible(1);
			self.image.setImage( "../../../"+ objType.getValue("icon")+".s2g" );
			self.image.setSizePct(1, 1);
			
			if objType.isManaWeapon():
				ammoCount = str(player.getManaUsesSlot(self.slot, True));
			else: ammoCount = str(player.getAmmoSlot(self.slot));
			
			if ammoCount == "None":
				ammoCount = "";

			self.ammo.setCaption( str( ammoCount ) );
			self.ammo.setPosition(self.getWidth() - self.ammo.getWidth(), self.getHeight() - self.ammo.getHeight());
		else:
			self.image.setVisible(0);
			self.ammo.setCaption("");
			
	def onAction(self, e):
		CL_RequestGiveback(self.slot);

class LoadoutUnitButton(DefaultContainer):
	def __init__(self, t):
		DefaultContainer.__init__(self);
		import loadout;
		self.objtype = savage.getObjectType(t);
		
		self.setSize(int(screenHeight*0.0625), int(screenHeight*0.09375));
		
		self.viewer = glass.GlassViewer();
		self.viewer.setModel(self.objtype.getValue("model"));
		self.viewer.setOpaque(0);
		self.viewer.setSize(self.getWidth(), self.getWidth());
		self.add( self.viewer, 0, 0 );
		self.viewer.rotateModel(160);
		self.viewer.setCameraPosition(-3,-1,12);
		self.viewer.setCameraTarget(-3,0,12);
		self.viewer.setCameraFOV(22.5);
		self.viewer.setAnimation("idle");
		
		self.request = DefaultImageButton();
		self.request.setImage("request.s2g");
		self.request.setSize(self.getWidth(), self.getWidth());
		self.request.setVisible(0);
		self.add(self.request);
		
		button = glass.ImageButton("textures/econs/transparent.s2g");
		#Create clickable, invisible button over the viewer.
		button.addActionListener(self);
		button.setClickAction( "CL_RequestUnit('" + t + "');" );
		self.add( button );
		button.setSizePct(1,1);
		
		name = DefaultLabel(self.objtype.getValue("description"));
		name.setFont(fontSizeSmall);
		
		self.price = DefaultLabel();

		p = str(self.objtype.getValue("playerCost"));
		if p == "0":
			p = "FREE";
		else:
			p = p + "^w^icon ../../gui/standard/icons/gold/gold_icon^";

		self.price.setCaption("^l" + p);
		self.price.setFont(fontSizeSmall);
		self.add(self.price, "center", int(screenHeight*0.0625));
	
	def update(self):
		player = savage.getLocalPlayer();
		refund = player.getType().getValue("playerCost");
		
		self.request.setVisible(0);
		
		if player.getGold()+refund < self.objtype.getValue("playerCost"):
			self.request.setVisible(1);
		
		if not self.objtype.isResearched():
			self.setVisible(0);
		else:
			self.setVisible(1);
		#this is because the model loading might be delayed
		self.viewer.fitCameraToModel(30);
	
	def onAction(self, e):
		player = savage.getLocalPlayer();
		refund = player.getType().getValue("playerCost");
		
		if player.getGold()+refund < self.objtype.getValue("playerCost"):
			CL_RequestGrant(self.objtype.getName());
		else:
			CL_RequestUnit(self.objtype.getName());
		
class LoadoutWindow(DefaultWindow):
	def __init__(self, race):
		DefaultWindow.__init__(self);

		self.presetsY = 0;
		
		import loadout;
		if race == "human":
			techTypes = ['NULL', 'magnetic', 'electric', 'chemical'];
		else:
			techTypes = ['NULL', 'entropy', 'strata', 'fire'];

		self.techButtons = [];
		self.inventory = [];
		self.units = [];
		
		self.setSize(screenWidthPct(0.75), screenHeightPct(0.75));
		self.setBackgroundColor(glass.Color(0,0,0,128));
		
		self.unitViewer = glass.GlassViewer();
		self.unitViewer.setOpaque(0);
		self.unitViewer.setCameraFOV(22.5);
		self.unitViewer.setCameraPosition(-3,-1,12);
		self.unitViewer.setCameraTarget(-3,0,12);
		#self.unitViewer.setCameraDistance(22);
		self.unitViewer.rotateModel(160);
		self.unitViewer.setAnimation("idle");
		self.unitViewer.setSize(screenHeightPct(0.65), screenHeightPct(0.65));
		self.add(self.unitViewer, self.getWidth()-self.unitViewer.getWidth(), "center");
		
		unitselbg = DefaultLabel();
		unitselbg.setImage("/gui/game/images/unit_selection_bg.tga");
		unitselbg.setSize(screenWidthPct(0.2475), screenHeightPct(0.08333));
		unitselbg.setOpaque(0);
		unitselbg.setForegroundColor(white);
		self.add(unitselbg, self.getWidth()-screenWidthPct(0.375), self.unitViewer.getHeight()-unitselbg.getHeight()-screenHeightPct(0.0833));
		
		types = savage.getRaceTypes(race);
		
		#build unit selection
		unitseloffset = self.getWidth()-int(screenWidth*0.375)-int(screenWidth*0.0625);
		x = unitseloffset;
		y=self.unitViewer.getHeight()-unitselbg.getHeight()-int(screenHeight*0.0833);
		for t in types:
			if t.isUnitType() and t.getValue("playerCost")>=0:
				b = loadout.LoadoutUnitButton(t.getName());
				self.units.append(b);
				self.add(b, x, y);
				x+=b.getWidth()+10;
	
		self.skinSelect = DefaultDropDown();
		for t in CL_GetSkinList():
			sid, name = t;
			self.skinSelect.addOption(name,sid);

		self.add(self.skinSelect, unitseloffset, y+unitselbg.getHeight());
	
		#build tech buttons based on race
		x=10;
		for tech in techTypes:
			y=self.unitViewer.getY();
			for t in types:
				if t.getValue("playerCost") < 0:
					continue;

				if t.getTechType() == tech and (t.isWeaponType() or t.isMeleeType()):
					b = loadout.LoadoutTechButton(t.getName());
					self.techButtons.append(b);
					self.add(b, x, y);
					y+=screenHeightPct(.0625)+24;

			x+=screenHeightPct(.0625)+10;

		weapons = DefaultLabel("WEAPONS");
		weapons.setFont(fontSizeLarge);
		self.add(weapons);
		weapons.setPosition(x-weapons.getWidth(), self.unitViewer.getY() - weapons.getHeight()-1);
		
		self.presetsY = y+10;
			
		x=10;
		for tech in techTypes:
			y=self.unitViewer.getY()+(screenHeightPct(.0625)+24)*4;
			for t in types:
				if t.getValue("playerCost") < 0:
					continue;

				if t.getTechType() == tech and (t.isItemType()):
					b = loadout.LoadoutTechButton(t.getName());
					self.techButtons.append(b);
					self.add(b, x, y);
					y+=screenHeightPct(.0625)+24;

			x+=screenHeightPct(.0625)+10;
		
		items = DefaultLabel("ITEMS");
		items.setFont(fontSizeLarge);
		self.add(items);
		items.setPosition(x-items.getWidth(), (self.unitViewer.getY()+(screenHeightPct(.0625)+24)*4) - items.getHeight()-1);
			
		#inventory buttons
		inv = loadout.LoadoutInventoryButton(0);
		self.inventory.append(inv);
		self.add(inv, (self.getWidth()-screenWidthPct(0.375)) - inv.getWidth() - 15, self.unitViewer.getY());
		
		inv = loadout.LoadoutInventoryButton(1);
		self.inventory.append(inv);
		self.add(inv, (self.getWidth()-screenWidthPct(0.375)) - inv.getWidth() - 15, self.unitViewer.getY()+(inv.getHeight()+10)*2);
		
		for i in range(3):
			inv = loadout.LoadoutInventoryButton(i+2);
			self.inventory.append(inv);
			self.add(inv, (self.getWidth()-screenWidthPct(0.375))+ (screenWidthPct(0.2475)) + 15, self.unitViewer.getY()+(inv.getHeight()+10)*i);
			
		#a special hack for humans
		if race == "human":
			inv = loadout.LoadoutInventoryButton(2);
			healButton = DefaultImageButton();
			healButton.setImage("/gui/game/images/healuse.s2g", "none");
			healButton.setSize(screenWidthPct(0.0625), screenWidthPct(0.0625));
			healButton.setClickAction("CL_RequestGiveUse('human_medkit')");
			self.add(healButton, self.getWidth()-screenWidthPct(0.375)+ (screenWidthPct(0.2475)) + 15,self.unitViewer.getY()+(inv.getHeight()+10)*3);
			
		#other buttons
		self.spawn = DefaultButton("PLAY");
		self.spawn.addActionListener(self);
		#self.spawn.setClickAction("CL_RequestSpawn(-1)");
		self.add(self.spawn);
		self.spawn.setPositionPct(.8, .92);
		
		comm = DefaultButton("COMMAND");
		comm.setClickAction("""import savage;CL_RequestSpawn(savage.Team(savage.getLocalPlayer().getTeam()).getCommandCenter().objectId);CL_CallVote('elect '+savage.getLocalPlayer().getName());""");
		self.add(comm);
		comm.setPositionPct(.45,.92);
		
		back = DefaultButton("LOBBY");
		back.setClickAction("CL_RequestLobby()");
		self.add(back);
		back.setPositionPct(.1,.92);
		
		#self.setOpaque(0);
		self.setPosition(screenWidthPct(1)//2 - self.getWidth()//2, screenHeightPct(.2));

	def onAction(self, e):
		if e.widget.getCaption() == "PLAY":
			if savage.getLocalPlayer().isCommander():
				CL_RequestResign();
			CL_RequestSkin(self.skinSelect.getSelectedValue());
			CL_RequestSpawn(-1);
		
	def update(self):
		player = savage.getLocalPlayer();
		self.unitViewer.setModel( player.getType().getValue("model") );
		self.unitViewer.fitCameraToModel(40);
		
		for b in self.techButtons:
			b.update();
			
		for b in self.inventory:
			b.update();

		for b in self.units:
			b.update();

		if player.getRespawnTime() > savage.getGameTime():
			self.spawn.setCaption(str(int(math.ceil((player.getRespawnTime() - savage.getGameTime())/1000.0))));
			self.spawn.setClickAction("");
		else:
			self.spawn.setCaption("PLAY");
			self.spawn.setClickAction("CL_RequestSpawn(-1)");

class MapWindow(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		
		self.setTitleVisible(0);
		self.setSizePct(1,1);
		self.setBackgroundColor(glass.Color(0,0,0,128));
		self.setVisible(0);
		
		self.minimap = glass.GlassMiniMap();
		self.minimap.setSize(screenHeightPct(0.667),screenHeightPct(0.667));
		self.add(self.minimap, "center", "center");

		self.buttons = glass.GlassContainer();
		self.buttons.setSize(self.minimap.getWidth(), self.minimap.getHeight());
		self.add(self.buttons, "center", "center");
		
		back = DefaultButton("BACK");
		back.setClickAction("loadout.mapWindow.hide();CL_RequestLoadout()");
		self.add(back);
		back.setX(self.minimap.getX() + self.minimap.getWidth()-back.getWidth());
		back.setY(self.minimap.getY() + self.minimap.getHeight() +5 );
		
	def update(self):
		gobjs = savage.getActiveObjects();
		myteam = savage.getLocalPlayer().getTeam();
		self.buttons.erase();
		
		for go in gobjs:
			if go.isSpawnPoint() and ((cvar_getvalue("sv_allowWarmupAllSpawnLocs") == 1 and savage.getGameStatus()<=GAME_STATUS_WARMUP) or go.getTeam() == myteam):
				pos = go.getPosition();
				#create a button with the appropriate color and image
				button = glass.ImageButton();
				#and place it in the correct position
				button.setImage(go.getMapIcon());
				button.setSize(screenWidthPct(0.025),screenWidthPct(0.025));
				if go.getTeam() == myteam:
					button.setForegroundColor(white);
					if go.isComplete() == False:
						button.setForegroundColor(glass.Color(0,255,0));
					else:
						button.setClickAction("CL_RequestSpawn("+str(go.objectId)+")");
				else:
					if cvar_getvalue("sv_allowWarmupAllSpawnLocs") == 1 and savage.getGameStatus()<=GAME_STATUS_WARMUP:
						button.setClickAction("CL_RequestSpawn("+str(go.objectId)+")");
					else:
						button.setForegroundColor(glass.Color(255,0,0));
				scale = float(World_GetGridSize()*100.0);
				button.setX(int( self.minimap.getWidth()* pos[0]/scale - button.getWidth()/2  ));
				button.setY(int( self.minimap.getHeight()*(1-pos[1]/scale) - button.getHeight()/2 ));
				self.buttons.add(button);

	def show(self):
		self.requestMoveToTop();
		self.minimap.setMap(cvar_get("world_overhead"));
		a = FadeInAction(self, 50);
		ActionSequence(a);
		self.update();

	def hide(self):
		a = FadeOutAction(self, 50);
		ActionSequence(a);

class LoadoutStatsWindow(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		
		self.setTitleVisible(0);
		self.setBackgroundColor(transparency);
		self.setSize(int(screenWidth*0.75), int(screenHeight*0.041667));
		
		container = DefaultContainer();
		container.setSize(int(screenWidth*0.65), int(screenHeight*0.03125));
		#experience/level
		self.level = glass.GlassProgressBar();
		self.level.setSize(int(screenWidth*0.65), int(screenHeight*0.03125));
		self.level.setForegroundColor(glass.Color(52, 101, 164, 128));
		self.level.setBackgroundColor(white);
		self.level.setBackgroundImage("gui/base/images/progress_bg.tga");
		container.add(self.level);
		self.levelLabel = DefaultLabel("LEVEL: 000");
		container.add(self.levelLabel, "center", "center");
		self.add(container);
		
		#kills/losses
		self.kills = DefaultLabel("000");
		self.kills.setFont(fontSizeLarge);
		self.add(self.kills);
		self.kills.setX(self.level.getWidth()+24);
		self.losses = DefaultLabel();
		self.losses.setFont(fontSizeSmall);
		self.add(self.losses);
		self.losses.setX(self.kills.getX()+self.kills.getWidth());
		
	def update(self):
		player = savage.getLocalPlayer();
		team = savage.getTeamObject(player.getTeam());
		
		self.kills.setCaption("^g"+("% 3d"%player.getKills()));
		self.losses.setCaption("^900"+str(player.getDeaths()));
		
		self.levelLabel.setCaption("LEVEL: "+("% 3d"%player.getLevel()));
		self.level.setProgress(player.getXp()/float(savage.getXPForLevel(team.getRace(), player.getLevel()+1)));
		
gblEventHandler.addGameListener(SpawnSelectHandler());

## CREATE SCREEN ##
glass.GUI_CreateScreen("loadout");

overlay = DefaultImage();
overlay.setImage("/gui/main/images/loading_overlay.png", False);
overlay.setSizePct(1.0,1.0);
glass.GUI_ScreenAddWidget("loadout", overlay);

activeWindow = None;
humanLoadout = LoadoutWindow("human");
glass.GUI_ScreenAddWidget("loadout", humanLoadout);
beastLoadout = LoadoutWindow("beast");
glass.GUI_ScreenAddWidget("loadout", beastLoadout);

#well, here's a fine hack.
#glass.GUI_ScreenAddWidget("loadout", gblPresetManager);

#stats that are interesting while in loadout
expWindow = LoadoutStatsWindow();
expWindow.setPosition(humanLoadout.getX(), int(screenHeight*.0976563));
glass.GUI_ScreenAddWidget("loadout", expWindow);

#teh mep
mapWindow = MapWindow();
glass.GUI_ScreenAddWidget("loadout", mapWindow);

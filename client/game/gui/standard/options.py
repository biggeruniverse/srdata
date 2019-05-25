# (c) 2011 savagerebirth.com
# this file creates the options
from silverback import *;
import glass;
import tools;
import default_bindactions;

# THERE IS A PLAN FOR LAYING OUT THE OPTIONS
# http://dl.dropbox.com/u/257331/SR%20Options.html
# PLEASE BEAR THIS IN MIND!

bindFields = [[],[],[]];#one list for each profile

def makePretty(action, profile):
	bound = "";
	actions = getKeyForAction(action, profile);
	if actions != None and len(actions) > 0:
		bound = actions[0].capitalize();
		for k in actions[1:]:
			bound = bound + ", " +  k.capitalize();
	else:
		bound = "-";
	return bound;
	

class BindHandler:
	def __init__(self, profile):
		self.action = "";
		self.controlwidget = None;
		self.profile = profile;

	def onMousePress(self, e):
		self.onMouseClick(e);

	def onMouseReleased(self, e):
		pass;

	def onMouseClick(self, e):
		if isinstance(e.widget, glass.GlassWindow):
			w = glass.GUI_GetWindow("mainmenu:binder");
			w.erase();
			w.close();
			bindKeyAction(e.button+199, self.action, self.profile); #ain't I a stinker?
			self.controlwidget.setText(makePretty(self.action, self.profile));
			
		else:
			self.action = e.widget.getId();
			self.controlwidget = e.widget;
			w = glass.GlassWindow('binder');
			glass.GUI_ScreenAddWidget("mainmenu", w);
			label = glass.GlassLabel("Press a key to bind...");
			label.setForegroundColor(glass.Color(255,255,255));
			w.add(label);
			w.addMouseListener(self);
			w.addKeyListener(self);
			w.setTitleVisible(0);
			w.setBackgroundColor(glass.Color(0,0,0,50));
			w.setSizePct(.25,.1);
			w.requestModalFocus();
			w.centerWindow();

	def onMouseScroll(self, e):
		if isinstance(e.widget, glass.GlassWindow):
			w = glass.GUI_GetWindow("mainmenu:binder");
			w.erase();
			w.close();
			bindKeyAction(e.button+199, self.action, self.profile); #ain't I a stinker?
			self.controlwidget.setText(makePretty(self.action, self.profile));

	def onKeyPress(self, e):
		e.widget.erase();
		e.widget.close();
		bindKeyAction(e.key, self.action, self.profile);
		self.controlwidget.setText(makePretty(self.action, self.profile));

	def onKeyReleased(self, e):
		pass;
	

class RestartChangeHandler:
	def onValueChanged(self, e):
		w = glass.GUI_GetWidget("mainmenu:Restart");
		w.setVisible(1);
		w.requestMoveToTop();

reshandler = RestartChangeHandler();

def clearBinds(t, profile):
	field = bindFields[profile][t];
	keys = field.getText().split(', ');
	for key in keys:
		unbindKeyAction(key,profile);
	field.setText("-");

def defaultBinds(t,profile):
	clearBinds(t, profile);
	field = bindFields[profile][t];
	dict = default_bindactions.maps[profile];
	action = field.getId();
	if action not in dict:
		con_println("No default keys assigned\n");
		return;
	keynums = dict[action];
	for num in keynums:
		bindKeyAction(num, action, profile);
	field.setText(makePretty(action, profile));

def defaultBindProfile(profile):
	for i in range(len(bindFields[profile])):
		defaultBinds(i, profile);

class OptionsWindow(glass.GlassWindow):
	def __init__(self):
		glass.GlassWindow.__init__(self, 'Options');
		self.first=True;
		#build the restart window
		w = glass.GlassWindow('Restart');
		glass.GUI_ScreenAddWidget("mainmenu", w);
		w.setSizePct(.4, .15);
		w.centerWindow();
		w.setBackgroundColor(glass.Color(0,0,0,128));
		w.setMovable(0);
		w.setTitleVisible(0);
		w.setVisible(0);
		l = glass.GlassLabel("This change will not take effect until you restart.\nWould you like to restart now?");
		w.add(l, 10, 10);
		b = glass.GlassButton("Restart");
		b.setClickAction("shutdown(1);");
		w.add(b, 50, 60);
		b = glass.GlassButton("Cancel");
		b.setClickAction("w=glass.GUI_GetWindow('mainmenu:Restart');w.setVisible(0);w.releaseModalFocus()");
		w.add(b, 150, 60);
		self.setBackgroundColor(glass.Color(0,0,0,128))
		self.setTitleVisible(0)
		self.nickname = None;
	
	def setVisible(self,yes):
		glass.GlassWindow.setVisible(self, yes);
		if self.first == False:
			return;
		self.first = False;
		
		close = glass.GlassButton("Close");
		close.addActionListener(self);
		self.add(close);
		close.setPosition(self.getWidth()-close.getWidth(), self.getHeight()-close.getHeight());
		
		#create the tabs
		tabHolder = glass.GlassTabbedContainer();
		tabHolder.setForegroundColor(white); #TODO doesn't work: we want tab labels that are white
		
		self.add(tabHolder);
		tabHolder.setSize(self.getWidth(),close.getY());
		
		#Controls, Config, Graphics, Sound, Network
		controlsTab = self.build_controls(tabHolder);
		tabHolder.addTab("Controls", controlsTab);
		
		configTab = self.build_config();
		graphicsTab = self.build_graphics();
		soundTab = self.build_sound();
		networkTab = self.build_network();
		
		names = ("Config", "Graphics", "Sound", "Network");
		internalHeight = tabHolder.getTabArea().height;
		#controlsTab sorts itself out
		for i, scrollArea in enumerate((configTab,graphicsTab,soundTab,networkTab)):
			bar = scrollArea.getScrollbarWidth();
			scrollArea.setWidth(min( scrollArea.getWidth() + bar , tabHolder.getWidth() ));
			scrollArea.setHeight(min( scrollArea.getHeight() + bar , internalHeight ));
			tabHolder.addTab(names[i],scrollArea);
	
	def createControls(self, table, controlList, profile):
		bindHandler = BindHandler(profile);
		for i, action in enumerate(controlList):
			text = glass.GlassTextField();
			text.setSize(150, 25);
			text.setLocked(1);
			text.setId(action);
			bindFields[profile].append(text);
			text.setText(makePretty(action, profile));
			text.addMouseListener(bindHandler);
			
			clear = glass.GlassButton("Clear");
			args = str(i)+", "+str(profile);
			clear.setClickAction("clearBinds("+args+")");
			
			default = glass.GlassButton("Default");
			default.setClickAction("defaultBinds(" +args+ ")");
			table.addRow( action, text, default, clear );
	
	#build the Controls Tab
	def build_controls(self,topTC):
		#these heights are broken again
		tabHolder = glass.GlassTabbedContainer();
		tabHolder.setForegroundColor(white);
		tabHolder.setSize(topTC.getWidth(),topTC.getTabArea().height);
		
		tabs = [];
		names = ("Player","Commander","Spectator");
		for i in range(3):
			table = GlassTablePlus();
			table.horizontalJustification = glass.Graphics.LEFT;
			table.setFrame(0);
			self.createControls(table, getBindActions(i), i);
			table.adjustSizeTo();
			scrollArea = glass.GlassScrollArea(table);
			scrollArea.setSize(table.getWidth(),table.getHeight());
			
			internalHeight = tabHolder.getTabArea().height;
			bar = scrollArea.getScrollbarWidth();
			scrollArea.setWidth(min( scrollArea.getWidth() + bar , tabHolder.getWidth() ));
			scrollArea.setHeight(min( scrollArea.getHeight() + bar , internalHeight ));
			
			tabHolder.addTab(names[i], scrollArea);
		
		table = GlassTablePlus();
		table.horizontalJustification = glass.Graphics.LEFT;
		table.setFrame(0);
		
		resets = [ glass.GlassButton("Player"), glass.GlassButton("Commander"), glass.GlassButton("Spectator")];
		for i, button in enumerate(resets):
			button.setClickAction("defaultBindProfile("+str(i)+");");
		
		table.addRow("Reset to defaults: ", *resets);
		table.adjustSizeTo();
		scrollArea = glass.GlassScrollArea(table);
		scrollArea.setSize(table.getWidth(),table.getHeight());
		scrollArea.setWidth(min( scrollArea.getWidth() + bar , tabHolder.getWidth() ));
		scrollArea.setHeight(min( scrollArea.getHeight() + bar , internalHeight ));
		
		tabHolder.addTab("Other", scrollArea);
		return tabHolder;
	
	#build the UI for the Config tab
	def build_config(self):
		table = GlassTablePlus();
		table.setFrame(0);
		table.horizontalJustification = glass.Graphics.LEFT;
		
		self.nickname = glass.GlassTextField( cvar_get("name") );
		self.nickname.setSize(150, 25);
		table.addRow( "Nickname", self.nickname );
		
		blockLeap = glass.GlassCheckbox();
		blockLeap.linkCvar("cl_blockLeapSwitch");
		table.addRow("Block / Leap Switch", blockLeap);
		
		chatFilter = glass.GlassCheckbox();
		chatFilter.linkCvar("cl_filter_filter");
		table.addRow( "Chat Filter", chatFilter );
		
		chatTimestamp = glass.GlassDropMenu();
		chatTimestamp.linkCvar("gui_chatTimestamp");
		chatTimestamp.addOption("Off","0");
		chatTimestamp.addOption("Game Time","1");
		chatTimestamp.addOption("Local Time","2"); 
		table.addRow("Chat Timestamp", chatTimestamp);
		
		showFPS = glass.GlassDropMenu();
		showFPS.linkCvar("cl_showfps");
		showFPS.addOption("Off","0");
		showFPS.addOption("Instant","1");
		showFPS.addOption("Average","2");
		showFPS.addOption("Both","3");
		table.addRow("Show FPS", showFPS);
		
		showServerFPS = glass.GlassCheckbox();
		showServerFPS.linkCvar("cl_showfpsserver");
		table.addRow("Show Server FPS",showServerFPS);
		
		showPing = glass.GlassCheckbox();
		showPing.linkCvar("cl_showping");
		table.addRow("Show Ping", showPing);
		
		showTeamStatus = glass.GlassCheckbox();
		showTeamStatus.linkCvar("gui_showteamstatus");
		table.addRow("Show Team Status",showTeamStatus);
		
		autoRecordDemos = glass.GlassCheckbox();
		autoRecordDemos.linkCvar("cl_autoRecordDemo");
		table.addRow("Auto-Record Demos",autoRecordDemos);
		
		showSquadMates = glass.GlassCheckbox();
		showSquadMates.linkCvar("cl_show_squad");
		table.addRow("Show Squad Mates",showSquadMates);
		#not sure if this is the right var
		#there's also cl_show_squad_comm
		
		cameraView = glass.GlassDropMenu();
		cameraView.linkCvar("cl_cameraPosLerp");
		cameraView.addOption("Smoothed","6");
		cameraView.addOption("Snappy","9999");
		table.addRow("Camera Snap",cameraView);
		
		cameraSmoothing = glass.GlassDropMenu();
		cameraSmoothing.linkCvar("cl_cameraAngleLerp");
		cameraSmoothing.addOption("Snap","9999");
		cameraSmoothing.addOption("Quick","50");
		cameraSmoothing.addOption("Smooth","35");
		cameraSmoothing.addOption("Very Smooth","15");
		cameraSmoothing.addOption("Demo Spectate","5");
		#based on two things: XR GUI and that I like 15 myself :P
		#with that said, people like to tweak this var a lot, perhaps it ought to be a slider
		table.addRow("Camera Smoothing",cameraSmoothing);

		minimapAlpha = glass.GlassSlider();
		minimapAlpha.linkCvar("cl_minimap_brightness");
		table.addRow("Minimap Alpha", minimapAlpha);
		
		#TODO toggle third person camera when using a ranged weapon?
		
		#Crosshair colors here?
		#Commander Tweaks for the Options
		tableHolder = glass.GlassScrollArea(table);
		tableHolder.setSize(table.getWidth(), table.getHeight());
		return tableHolder;
	
	#build the Graphics Tab
	def build_graphics(self):
		table = GlassTablePlus();
		table.setFrame(0);
		table.horizontalJustification = glass.Graphics.LEFT;
		
		videoResolution = glass.GlassDropMenu();
		videoResolution.linkCvar("vid_mode");
		videoResolution.addSelectionListener(reshandler);
		i=1;
		mode = cvar_get("vid_mode"+str(i));
		while len(mode) > 0:
			videoResolution.addOption(mode, mode);
			i += 1;
			mode = cvar_get("vid_mode"+str(i));
	
		table.addRow( "Video Resolution" , videoResolution );
		
		fullscreen = glass.GlassCheckbox();
		fullscreen.linkCvar("vid_fullscreen");
		fullscreen.addSelectionListener(reshandler);
		table.addRow( "Full Screen", fullscreen );

		fov = glass.GlassDropMenu();
		fov.linkCvar("cl_fov");
		fov.addOption("4:3", "90");
		fov.addOption("16:9", "110");
		fov.addOption("16:10", "100");
		table.addRow( "Frame", fov);

		gamma = glass.GlassSlider();
		gamma.linkCvar( "vid_gamma" );
		gamma.setScaleEnd(2.5);
		gamma.setScaleStart(0.5);
		table.addRow( "Brightness" , gamma );
		
		showArmor = glass.GlassCheckbox();
		showArmor.linkCvar( "cl_showLevelArmor");
		table.addRow( "Show Armor" , showArmor );
		
		showImpacts = glass.GlassCheckbox();
		showImpacts.linkCvar("cl_collisionDecals");
		table.addRow( "Show Impact Effects", showImpacts);
		
		showBlood = glass.GlassCheckbox();
		showBlood.linkCvar("cl_bloodSplatter");
		table.addRow( "Show Blood Splatter", showBlood );
		
		antiAliasing = glass.GlassDropMenu();
		antiAliasing.linkCvar("vid_multisample");
		antiAliasing.addOption("None", "0");
		antiAliasing.addOption("2x", "2");
		antiAliasing.addOption("4x", "4");
		antiAliasing.addSelectionListener(reshandler);
		table.addRow( "Anti-Aliasing", antiAliasing );
		
		showClouds = glass.GlassCheckbox();
		showClouds.linkCvar("gfx_clouds");
		table.addRow( "Show Clouds", showClouds );
		
		useShaders = glass.GlassDropMenu();
		useShaders.linkCvar("gfx_GLSLQuality");
		useShaders.addOption("^900Off", "0");
		useShaders.addOption("Low", "1");
		useShaders.addOption("High", "3");
		table.addRow( "Shaders", useShaders);
		
		forceSoft = glass.GlassCheckbox();
		forceSoft.linkCvar("gfx_forceSoftware");
		table.addRow( "Force CPU Animation", forceSoft );

		showGrass = glass.GlassCheckbox();
		showGrass.linkCvar("gfx_grass");
		table.addRow( "Show Grass", showGrass );

		grassFalloff = glass.GlassDropMenu();
		grassFalloff.linkCvar("gfx_grassRange")
		grassFalloff.addOption("Near","500");
		grassFalloff.addOption("Far","1500");
		grassFalloff.addOption("Very Far","3500");
		table.addRow( "Grass Falloff", grassFalloff );

		showShadows = glass.GlassDropMenu();
		showShadows.linkCvar("gfx_shadow");
		showShadows.addOption("Off", "0");
		showShadows.addOption("Fast", "1");
		showShadows.addOption("Nice", "3");
		table.addRow( "Shadows", showShadows);

		postProcMaster = glass.GlassCheckbox();
		postProcMaster.linkCvar("gfx_postProcessing");
		#TODO: disable the other post proc checkboxes if this is disabled
		table.addRow( "Post-Processing", postProcMaster);
	
		postBloom = glass.GlassCheckbox();
		postBloom.linkCvar("gfx_postBloom");
		table.addRow( "   Bloom Filter", postBloom);
		
		postMotion = glass.GlassCheckbox();
		postMotion.linkCvar("gfx_postMotion");
		table.addRow( "   Motion Blur", postMotion);
		
		showGlow = glass.GlassCheckbox();
		showGlow.linkCvar("gfx_glowFilter");
		table.addRow( "   Glow Filter", showGlow );
	
		postWater = glass.GlassCheckbox();
		postWater.linkCvar("gfx_postWater");
		table.addRow( "   Water Effects", postWater);
		
		postSSAO = glass.GlassCheckbox();
		postSSAO.linkCvar("gfx_postSSAO");
		table.addRow( "   Ambient Occlusion", postSSAO);
		
		table.adjustSizeTo();
		tableHolder = glass.GlassScrollArea(table);
		tableHolder.setSize(table.getWidth(), table.getHeight());
		return tableHolder;
	
	#build the Sound Tab
	def build_sound(self):
		table = GlassTablePlus();
		table.setFrame(0);
		table.horizontalJustification = glass.Graphics.LEFT;
		
		MasterVolume = glass.GlassSlider();
		MasterVolume.linkCvar( "sound_mastervolume" );
		MasterVolume.setScaleEnd(1.0);
		MasterVolume.setScaleStart(0);
		table.addRow("Master Volume", MasterVolume);
	
		MusicVolume = glass.GlassSlider();
		MusicVolume.linkCvar( "sound_musicvolume" );
		MusicVolume.setScaleEnd(1.0);
		MusicVolume.setScaleStart(0);
		table.addRow("Music Volume", MusicVolume);
	
		SoundVolume = glass.GlassSlider();
		SoundVolume.linkCvar( "sound_sfxVolume" );
		SoundVolume.setScaleEnd(1.0);
		SoundVolume.setScaleStart(0);
	
		TestSoundButton = glass.GlassButton("Test");
		TestSoundButton.setClickAction("Sound_PlaySound('/sound/human/player/male/good_game_1.ogg');");
		table.addRow("Sound Effect Volume", SoundVolume,TestSoundButton);
		#TODO play this sound when the slider loses focus, ie when the car is released
	
		softwareMode = glass.GlassCheckbox();
		softwareMode.linkCvar("sound_softwareMode");
		table.addRow("Software Mode", softwareMode);
	
		mixrate = glass.GlassDropMenu();
		mixrate.linkCvar("sound_mixrate");
		mixrate.addOption("22050", "22050")
		mixrate.addOption("44100", "44100")
		mixrate.addOption("48000", "48000")
		table.addRow("Sampling Rate", mixrate);
	
		channels = glass.GlassSpinner();
		channels.linkCvar("sound_numChannels");
		channels.setStep(32);
		channels.setWidth(50);
		table.addRow("Sound Channels", channels);
		
		VoIPVolume = glass.GlassSlider();
		VoIPVolume.linkCvar( "sound_voipvolume" );
		VoIPVolume.setScaleEnd(1.0);
		VoIPVolume.setScaleStart(0);
		table.addRow("Voice Volume", VoIPVolume);
		table.adjustSizeTo();
		tableHolder = glass.GlassScrollArea(table);
		tableHolder.setSize(table.getWidth(), table.getHeight());
		return tableHolder;
	
	#build the Network Tab
	def build_network(self):
		table = GlassTablePlus();
		table.setFrame(0);
		table.horizontalJustification = glass.Graphics.LEFT;

		preset = glass.GlassDropMenu();
		preset.addOption("Dial-up","dialup");
		preset.addOption("ISDN","isdn");
		preset.addOption("DSL/Cable","dslcable");
		preset.addOption("LAN","lan");
		preset.addSelectionListener(self);
		table.addRow( "Presets:", preset);
		
		bandwidth = glass.GlassSpinner();
		bandwidth.linkCvar("netBPS");
		bandwidth.setStep(200);
		bandwidth.setWidth(50);
		table.addRow("Bandwidth", bandwidth);
	
		netfps = glass.GlassSpinner();
		netfps.linkCvar("netFrames");
		netfps.setStep(1);
		table.addRow("Updates per second:", netfps);
	
		maxPacketSize = glass.GlassSpinner();
		maxPacketSize.linkCvar("maxPacketSize");
		maxPacketSize.setStep(20);
		table.addRow("Max. Packet Size:", maxPacketSize);
	
		lagcompensation = glass.GlassDropMenu();
		lagcompensation.linkCvar("cl_lerpshift");
		lagcompensation.addOption("Off","0");
		lagcompensation.addOption("Low", "0.1"); #TODO test these values
		lagcompensation.addOption("Medium", "0.2");
		lagcompensation.addOption("High", "0.4");
		table.addRow("Lag Compensation", lagcompensation);
		table.adjustSizeTo();
		tableHolder = glass.GlassScrollArea(table);
		tableHolder.setSize(table.getWidth(), table.getHeight());
		return tableHolder;
	
	netPresetDict = {
		"dialup": (4000,20,1024),
		"isdn": (6000,20,1400),
		"dslcable": (50000,20,1500),
		"lan": (100000,30,2048)
	};
	
	def onValueChanged(self,e):
		value = e.widget.getSelectedValue();
		bps, frames, psize = self.netPresetDict[value];
		cvar_setvalue("netBPS",bps);
		cvar_setvalue("netFrames",frames);
		cvar_setvalue("maxPacketSize",psize);
	
	def onAction(self, e):
		self.setVisible(0);
		cvar_set("name", self.nickname.getText());
		saveconfig();

# (c) 2011 savagerebirth.com
# this file creates the graphics panel
from silverback import *;
import glass;
import tools;

class GraphicsPanel(glass.GlassWindow):
	def __init__(self):
		glass.GlassWindow.__init__(self, 'Graphics Panel');
		self.first=True;
		self.setBackgroundColor(glass.Color(0,0,0,128));
		self.setTitleVisible(0);
		self.setSizePct(0.55,0.8);
		self.setVisible(0);
		
		# config
		
		self.table = GlassTablePlus();
		self.table.setFrame(0);
		self.table.setCellPadding(2);
		self.table.horizontalJustification = glass.Graphics.LEFT;
		
		self.table.addRow("^gConfig","");
		
		self.table.addRow();
		
		blockLeap = glass.GlassCheckbox();
		blockLeap.linkCvar("cl_blockLeapSwitch");
		self.table.addRow("Block / Leap Switch", blockLeap);
		
		showFPS = glass.GlassDropMenu();
		showFPS.linkCvar("cl_showfps");
		showFPS.addOption("Off","0");
		showFPS.addOption("Instant","1");
		showFPS.addOption("Average","2");
		showFPS.addOption("Both","3");
		self.table.addRow("Show FPS", showFPS);
		
		showServerFPS = glass.GlassCheckbox();
		showServerFPS.linkCvar("cl_showfpsserver");
		self.table.addRow("Show Server FPS",showServerFPS);
		
		showPing = glass.GlassDropMenu();
		showPing.linkCvar("gui_showping");
		showPing.addOption("Off","0");
		showPing.addOption("Instant","1");
		showPing.addOption("Average","2");
		self.table.addRow("Show Ping", showPing);
		
		showTeamStatus = glass.GlassCheckbox();
		showTeamStatus.linkCvar("gui_showteamstatus");
		self.table.addRow("Show Team Status",showTeamStatus);
	
		thirdPerson = glass.GlassCheckbox();
		thirdPerson.linkCvar("cl_alwaysThirdPerson");
		self.table.addRow("Force Third Person", thirdPerson);
	
		cameraView = glass.GlassDropMenu();
		cameraView.linkCvar("cl_cameraPosLerp");
		cameraView.addOption("Smoothed","6");
		cameraView.addOption("Snappy","9999");
		self.table.addRow("Camera Snap",cameraView);
		
		cameraSmoothing = glass.GlassDropMenu();
		cameraSmoothing.linkCvar("cl_cameraAngleLerp");
		cameraSmoothing.addOption("Snap","9999");
		cameraSmoothing.addOption("Quick","50");
		cameraSmoothing.addOption("Smooth","35");
		cameraSmoothing.addOption("Very Smooth","15");
		cameraSmoothing.addOption("Demo Spectate","5");
		self.table.addRow("Camera Smoothing",cameraSmoothing);
		
		# Graphics
		
		self.table.addRow();
		
		self.table.addRow("^gGraphics","");
		
		self.table.addRow();
		
		gamma = glass.GlassSlider();
		gamma.linkCvar( "vid_gamma" );
		gamma.setScaleEnd(2.5);
		gamma.setScaleStart(0.5);
		self.table.addRow( "Brightness" , gamma );
		
		showArmor = glass.GlassCheckbox();
		showArmor.linkCvar( "cl_showLevelArmor");
		self.table.addRow( "Show Armor" , showArmor );
		
		showImpacts = glass.GlassCheckbox();
		showImpacts.linkCvar("cl_collisionDecals");
		self.table.addRow( "Show Impact Effects", showImpacts);
		
		showBlood = glass.GlassCheckbox();
		showBlood.linkCvar("cl_bloodSplatter");
		self.table.addRow( "Show Blood Splatter", showBlood );
		
		grassFalloff = glass.GlassDropMenu();
		grassFalloff.linkCvar("gfx_foliageFalloff")
		grassFalloff.addOption("Off","0");
		grassFalloff.addOption("Near","100");
		grassFalloff.addOption("Far","700");
		grassFalloff.addOption("Very Far","1500");
		self.table.addRow( "Grass Falloff", grassFalloff );
		
		showClouds = glass.GlassCheckbox();
		showClouds.linkCvar("gfx_clouds");
		self.table.addRow( "Show Clouds", showClouds );
		
		showShadows = glass.GlassDropMenu();
		showShadows.linkCvar("gfx_shadow");
		showShadows.addOption("Off", "0");
		showShadows.addOption("Fast", "1");
		showShadows.addOption("Nice", "3");
		self.table.addRow( "Shadows", showShadows);
		
		useShaders = glass.GlassDropMenu();
		useShaders.linkCvar("gfx_GLSLQuality");
		useShaders.addOption("^900Off", "0");
		useShaders.addOption("Low", "1");
		useShaders.addOption("High", "3");
		self.table.addRow( "Shaders", useShaders);
		
		forceSoft = glass.GlassCheckbox();
		forceSoft.linkCvar("gfx_forceSoftware");
		self.table.addRow( "Force CPU Animation", forceSoft );
		
		postProcMaster = glass.GlassCheckbox();
		postProcMaster.linkCvar("gfx_postProcessing");
		#TODO: disable the other post proc checkboxes if this is disabled
		self.table.addRow( "Post-Processing", postProcMaster);
		
		postBloom = glass.GlassCheckbox();
		postBloom.linkCvar("gfx_postBloom");
		self.table.addRow( "   Bloom Filter", postBloom);
		
		postMotion = glass.GlassCheckbox();
		postMotion.linkCvar("gfx_postMotion");
		self.table.addRow( "   Motion Blur", postMotion);
		
		showGlow = glass.GlassCheckbox();
		showGlow.linkCvar("gfx_glowFilter");
		self.table.addRow( "   Glow Filter", showGlow );
		
		postWater = glass.GlassCheckbox();
		postWater.linkCvar("gfx_postWater");
		self.table.addRow( "   Water Effects", postWater);
		
		postSSAO = glass.GlassCheckbox();
		postSSAO.linkCvar("gfx_postSSAO");
		self.table.addRow( "   Ambient Occlusion", postSSAO);		
		
		# Sound 
		
		self.table.addRow();
		
		self.table.addRow("^gSound","");
		
		self.table.addRow();
		
		MasterVolume = glass.GlassSlider();
		MasterVolume.linkCvar( "sound_mastervolume" );
		MasterVolume.setScaleEnd(1.0);
		MasterVolume.setScaleStart(0);
		self.table.addRow("Master Volume", MasterVolume);
	
		MusicVolume = glass.GlassSlider();
		MusicVolume.linkCvar( "sound_musicvolume" );
		MusicVolume.setScaleEnd(1.0);
		MusicVolume.setScaleStart(0);
		self.table.addRow("Music Volume", MusicVolume);
	
		SoundVolume = glass.GlassSlider();
		SoundVolume.linkCvar( "sound_sfxVolume" );
		SoundVolume.setScaleEnd(1.0);
		SoundVolume.setScaleStart(0);
		
		VoIPVolume = glass.GlassSlider();
		VoIPVolume.linkCvar( "sound_voipvolume" );
		VoIPVolume.setScaleEnd(1.0);
		VoIPVolume.setScaleStart(0);
		self.table.addRow("Voice Volume", VoIPVolume);
		
		internalHeight = self.getChildrenArea().height;
		
		self.scrollArea = glass.GlassScrollArea(self.table);
		self.add(self.scrollArea);
		self.scrollArea.setScrollPolicy( glass.GlassScrollArea.SHOW_NEVER , glass.GlassScrollArea.SHOW_ALWAYS );
		
		bar = self.scrollArea.getScrollbarWidth();
		self.scrollArea.setWidth(min( self.getWidth() + bar , self.getWidth() - 8 ));
		self.scrollArea.setHeight(min( internalHeight + bar , internalHeight - 4));		
	
	def show(self):
		self.setVisible(1);
		self.mousemode = getMouseMode();
		if self.mousemode == MOUSE_FREE:
			self.mousemode = MOUSE_RECENTER; #stop the gui from getting the main game stuck
		setMouseMode(MOUSE_FREE);
		
	def hide(self):
		setMouseMode(self.mousemode); 
		self.setVisible(0);

# (c) 2011 savagerebirth.com

import mainmenu;
from silverback import *;
import glass;
import default_bindactions;
import formbuilder;

class OptionsSection(AbstractSection):
	
	def create(self):
		
		self.setBackgroundColor(glass.Color(24, 14, 14));
		
		self.restartRequired = False;
		
		bgImage = DefaultImage();
		bgImage.setImage("bar_red_shadow.png");
		bgImage.setSize(self.getWidth(), 40);
		self.add(bgImage, 0, 40);
	
		header = DefaultContainer();
		header.setSize(self.getWidth(), 70);
		header.setBackgroundColor(glass.Color(85, 21, 11));
		header.setOpaque(True);
		self.add(header);
		
		title = DefaultImage();
		title.setImage("txt_options.png");
		header.add(title, "center", 10);

		content = glass.GlassTabbedArea();	
		
		# this is just for the padding
		contentContainer = DefaultContainer();
		contentContainer.setSize(self.getWidth(), self.getHeight() - 72);
		self.add(contentContainer, 0, 40);
		
		content.setSize(contentContainer.getWidth() - 25, contentContainer.getHeight() - 45);
		
		note = DefaultLabel("Note: options are saved instantly");
		note.setFont(fontSizeSmall);
		note.setForegroundColor(tangoGrey3);
		self.add(note, 5, 5, "right", "bottom");
		
		interfaceForm = self.createInterfaceForm(content);
		self.interfaceContainer = glass.GlassScrollArea(interfaceForm);
		self.interfaceContainer.setHorizontalScrollPolicy( glass.GlassScrollArea.SHOW_NEVER );
		content.addTab("INTERFACE", self.interfaceContainer);
		
		self.restartWarning = DefaultContainer();
		self.restartWarning.setSize(self.getWidth(), 50);
		self.restartWarning.setVisible(False);
		self.restartWarning.setBackgroundColor(glass.Color(85, 21, 11));
		self.restartWarning.setOpaque(True);		
		
		restartWarningLabel = DefaultLabel("RESTART REQUIRED");
		self.restartWarning.add(restartWarningLabel, "center");
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		self.restartWarning.add(hr, 0, restartWarningLabel.getHeight() + 3);
		
		restartMessage = DefaultLabel("Some changes won\'t take affect until you restart. Would you like to restart now?");
		restartMessage.setFont(fontSizeSmall);
		self.restartWarning.add(restartMessage, 15, 27);
		
		restart = DefaultButton("RESTART");
		restart.setClickAction("shutdown(1)");
		self.restartWarning.add(restart, 30, 10, "right");
		
		self.gfxForm = self.createGfxForm(content);
		self.gfxContainer = glass.GlassScrollArea(self.gfxForm);
		self.gfxContainer.setHorizontalScrollPolicy( glass.GlassScrollArea.SHOW_NEVER );
		self.gfxForm.setWidth(self.gfxForm.getWidth() - self.gfxContainer.getScrollbarWidth());
		content.addTab("GRAPHICS", self.gfxContainer);
		
		soundForm = self.createSoundForm(content);
		self.soundContainer = glass.GlassScrollArea(soundForm);
		self.soundContainer.setHorizontalScrollPolicy( glass.GlassScrollArea.SHOW_NEVER );
		content.addTab("SOUND", self.soundContainer);
		
		controlForm = self.createControlForm(content);
		self.controlContainer = glass.GlassScrollArea(controlForm);
		self.controlContainer.setHorizontalScrollPolicy( glass.GlassScrollArea.SHOW_NEVER );
		controlForm.setWidth(controlForm.getWidth() - self.controlContainer.getScrollbarWidth());
		content.addTab("CONTROLS", self.controlContainer);

		contentContainer.add(content, 15, 0);
		contentContainer.add(self.restartWarning, 0, 32);
		
		self.binder = Binder();
		mainmenu.add(self.binder);
		
	def onAction(self, e):
		
		if hasattr(e.widget, "bindAction"):
			self.binder.show(e.widget);
		elif e.widget == self.nickSet:
			cvar_set("name", self.nick.getText());
		else:
			self.switchOptions(e.widget);
		
	def get8Col(self, width):
		
		colWidth = width // 8;
		x = [];
		for i in range(8):
			x.append(colWidth * i);
			
			# debug: draw columns for when creating stuff
			if 0:
				c = DefaultContainer();
				c.setBackgroundColor(glass.Color(60, 0, 0, 50));
				c.setSize(colWidth - 2, 400);
				self.add(c, 15 + colWidth * i + 1, 80);
				l = DefaultLabel(str(i));
				self.add(l, colWidth * i + colWidth // 2 + l.getWidth() // 2, 70);
				
		return (colWidth, x);
	
	def buildBinds(self, container, name, x, y, i):
		generalBinds = [
			'Chat (All)', 'Chat (Team)', 'Chat (Clan)', 'Chat (Squad)', 'Chat (Commander)', 'Voice Chat', 'Show Chat History',
			'Vote Yes', 'Vote No',
			'Show Scoreboard', 'Screenshot', 'In-game Menu'
		];
		
		profileBinds = {
			"GENERAL": generalBinds,
			"PLAYER": getBindActions(0),
			"COMMANDER": getBindActions(1)
		};

		yInc = 35;
		
		binds = profileBinds[name];
		
		label = DefaultLabel(str(name) + " BINDS");
		container.add(label, "center", y);
		
		hr = DefaultDivider();
		container.add(hr, 0, y + label.getHeight() + 3);
	
		y += yInc;
	
		actionLabel = DefaultLabel("ACTION");
		actionLabel.setFont(fontSizeSmall);
		container.add(actionLabel, x[0], y);
		
		primaryLabel = DefaultLabel("PRIMARY");
		primaryLabel.setFont(fontSizeSmall);
		container.add(primaryLabel, x[4] - primaryLabel.getWidth() // 2, y);
		
		secondaryLabel = DefaultLabel("SECONDARY");
		secondaryLabel.setFont(fontSizeSmall);
		secondaryLabel.setEnabled(False);
		container.add(secondaryLabel, x[6] - secondaryLabel.getWidth() // 2, y);
		
		y += int(yInc / 1.5);
	
		for action in binds:
			
			if name != "GENERAL" and action in generalBinds:
				continue;
			
			label = DefaultLabel(action);
			label.setFont(fontSizeSmall);
			container.add(label, x[0], y);
			
			keys = getKeyForAction(action, i);
			primary = DefaultButton("unset");
			primary.addActionListener(self);
			primary.bindAction = action;
			primary.profile = name;
			primary.priority = 0;
			primary.hotkey = False;
			primary.setFont(fontSizeSmall);
			primary.setHeight(15);
			if keys != None and len(keys) > 0:
				primary.setCaption(keys[0].capitalize());
			self.bondage.append(primary);
			container.add(primary, x[4] - primary.getWidth() // 2, y);
			secondary = DefaultButton("unset");
			secondary.addActionListener(self);
			secondary.bindAction = action;
			secondary.profile = name;
			secondary.priority = 1;
			secondary.hotkey = False;
			secondary.setFont(fontSizeSmall);
			secondary.setHeight(15);
			secondary.setEnabled(False);
			if keys != None and len(keys) > 1:
				secondary.setCaption(keys[1]);
			#self.bondage.append(secondary);
			container.add(secondary, x[6] - secondary.getWidth() // 2, y);
			
			y += int(yInc / 1.5);
			
		y += int(yInc / 1.5);
		return y;

	def buildHotkeys(self, container, x, y):
		yInc = 35;
		label = DefaultLabel("COMMANDER HOTKEYS");
		container.add(label, "center", y);
		
		hr = DefaultDivider();
		container.add(hr, 0, y + label.getHeight() + 3);
	
		y += int(yInc / 1.5);
		y += int(yInc / 1.5);

		for action in getHotkeyActions(1):
			
			label = DefaultLabel(action);
			label.setFont(fontSizeSmall);
			container.add(label, x[0], y);
			
			key = getHotkeyForAction(action);
			primary = DefaultButton("unset");
			primary.addActionListener(self);
			primary.bindAction = action;
			primary.profile = "COMMANDER";
			primary.priority = 0;
			primary.hotkey = True;
			primary.setFont(fontSizeSmall);
			primary.setHeight(15);
			primary.setCaption(key.capitalize());
			self.bondage.append(primary);
			container.add(primary, x[4] - primary.getWidth() // 2, y);
			y += int(yInc / 1.5);
		y += int(yInc / 1.5);

		return y;
		
	def createControlForm(self, parent):
		
		container = DefaultContainer();
		container.setWidth(parent.getWidth());
		
		(colWidth, x) = self.get8Col(container.getWidth());
		y = 0;
		yInc = 35;
		
		mouseLabel = DefaultLabel("MOUSE OPTIONS");
		container.add(mouseLabel, "center", y);
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		container.add(hr, 0, y + mouseLabel.getHeight() + 3);
		
		y += yInc;
		
		meleeLabel = DefaultLabel("MELEE SENSITIVITY");
		meleeLabel.setFont(fontSizeSmall);
		container.add(meleeLabel, x[0], y);
		
		self.melee = DefaultSlider();
		self.melee.linkCvar("cl_sensitivity_melee");
		self.melee.setScaleStart(10);
		self.melee.setScaleEnd(100);
		self.melee.setWidth(int(colWidth * 1.5));
		container.add(self.melee, x[2], y);
		
		snapLabel = DefaultLabel("CAMERA SNAP");
		snapLabel.setFont(fontSizeSmall);
		container.add(snapLabel, x[4], y);
		
		snap = DefaultSlider();
		snap.linkCvar("cl_cameraPosLerp");
		snap.setScaleStart(1);
		snap.setScaleEnd(9999);
		snap.setWidth(int(colWidth * 1.5));
		container.add(snap, x[6], y);
		
		y += yInc;
		
		rangedLabel = DefaultLabel("RANGED SENSITIVITY");
		rangedLabel.setFont(fontSizeSmall);
		container.add(rangedLabel, x[0], y);
		
		ranged = DefaultSlider();
		ranged.linkCvar("cl_sensitivity_range");
		ranged.setScaleStart(10);
		ranged.setScaleEnd(100);
		ranged.setWidth(int(colWidth * 1.5));
		container.add(ranged, x[2], y);

		smoothLabel = DefaultLabel("CAMERA SMOOTHING");
		smoothLabel.setFont(fontSizeSmall);
		container.add(smoothLabel, x[4], y);
		
		smooth = DefaultSlider();
		smooth.linkCvar("cl_cameraAngleLerp");
		smooth.setScaleStart(0);
		smooth.setScaleEnd(9999);
		smooth.setWidth(int(colWidth * 1.5));
		container.add(smooth, x[6], y);
		
		y += yInc;
		
		dualLabel = DefaultLabel("DUAL SENSITIVITY");
		dualLabel.setFont(fontSizeSmall);
		container.add(dualLabel, x[0], y);

		dualsens = DefaultCheckBox();
		dualsens.linkCvar("cl_dual_sensitivity");
		container.add(dualsens, x[2], y);
		dualsens.addSelectionListener(self);

		pitchLabel = DefaultLabel("CONSTRAINT PITCH");
		pitchLabel.setFont(fontSizeSmall);
		container.add(pitchLabel, x[4], y);
		
		pitch = DefaultCheckBox();
		pitch.linkCvar("cl_meleeConstrain");
		container.add(pitch, x[6], y);
		
		y += yInc; 

		switchLabel = DefaultLabel("BLOCK/LEAP SWITCH");
		switchLabel.setFont(fontSizeSmall);
		container.add(switchLabel, x[0], y);
		
		switch = DefaultCheckBox();
		switch.linkCvar("cl_blockLeapSwitch");
		container.add(switch, x[2], y);
		
		pitchLabel = DefaultLabel("INVERT MOUSE");
		pitchLabel.setFont(fontSizeSmall);
		container.add(pitchLabel, x[4], y);
		
		pitch = DefaultCheckBox();
		pitch.linkCvar("invertmouse");
		container.add(pitch, x[6], y);
		
		y += yInc;
		
		self.bondage = [];
		
		y = self.buildBinds(container, "GENERAL", x, y, 0);
		
		for i, name in enumerate(["PLAYER", "COMMANDER"]):
			
			y = self.buildBinds(container, name, x, y, i);


		y = self.buildHotkeys(container, x, y);
		
		container.setHeight(y);
		
		return container;
		
	def createInterfaceForm(self, parent):
		
		container = DefaultContainer();
		container.setWidth(parent.getWidth());
		
		(colWidth, x) = self.get8Col(container.getWidth());
		y = 0;
		yInc = 35;
		
		interfaceLabel = DefaultLabel("INTERFACE OPTIONS");
		container.add(interfaceLabel, "center", y);
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		container.add(hr, 0, y + interfaceLabel.getHeight() + 3);
		
		y += yInc;
		
		filterLabel = DefaultLabel("PROFANITY FILTER");
		filterLabel.setFont(fontSizeSmall);
		container.add(filterLabel, x[2] - filterLabel.getWidth(), y);
		
		filter = DefaultCheckBox();
		filter.linkCvar("cl_filter_filter");
		container.add(filter, x[2] + 3, y);
		
		stampLabel = DefaultLabel("CHAT TIMESTAMP");
		stampLabel.setFont(fontSizeSmall);
		container.add(stampLabel, x[4] - stampLabel.getWidth(), y);
		
		stamp = DefaultCheckBox();
		stamp.linkCvar("gui_chatTimestamp");
		container.add(stamp, x[4] + 3, y);
		
		pingLabel = DefaultLabel("SHOW PING");
		pingLabel.setFont(fontSizeSmall);
		container.add(pingLabel, x[6] - pingLabel.getWidth(), y);
		
		ping = DefaultCheckBox();
		ping.linkCvar("cl_showping");
		container.add(ping, x[6] + 3, y);
		
		y += yInc;

		serverFpsLabel = DefaultLabel("SERVER FPS");
		serverFpsLabel.setFont(fontSizeSmall);
		container.add(serverFpsLabel, x[6] - serverFpsLabel.getWidth(), y);

		serverFps = DefaultCheckBox();
		serverFps.linkCvar("cl_showfpsserver");
		container.add(serverFps, x[6] + 3, y);

		y += yInc;

		miniLabel = DefaultLabel("MINIMAP OPACITY");
		miniLabel.setFont(fontSizeSmall);
		container.add(miniLabel, x[2] - miniLabel.getWidth(), y);

		mini = DefaultSlider();
		mini.linkCvar("cl_minimap_brightness");
		mini.setWidth(colWidth * 4);
		container.add(mini, x[2] + 3, y);

		y += yInc;

		nickLabel = DefaultLabel("NICKNAME");
		nickLabel.setFont(fontSizeSmall);
		container.add(nickLabel, x[2] - nickLabel.getWidth(), y);

		self.nick = DefaultTextField();
		self.nick.setWidth(colWidth*2);
		container.add(self.nick, x[2]+3, y);
		self.nick.setText(cvar_get("name"));

		self.nickSet = DefaultButton("SET");
		self.nickSet.setFont(fontSizeSmall);
		container.add(self.nickSet, x[4]+25, y);
		self.nickSet.addActionListener(self);

		y += yInc;

		container.setHeight(y)

		return container;

	def createSoundForm(self, parent):
		container = DefaultContainer();
		container.setWidth(parent.getWidth());
		
		(colWidth, x) = self.get8Col(container.getWidth());
		y = 0;
		yInc = 35;
		
		volumeLabel = DefaultLabel("VOLUME OPTIONS");
		container.add(volumeLabel, "center", y);
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		container.add(hr, 0, y + volumeLabel.getHeight() + 3);
		
		y += yInc;
		
		masterLabel = DefaultLabel("MASTER VOLUME");
		masterLabel.setFont(fontSizeSmall);
		container.add(masterLabel, x[0], y);
		
		master = DefaultSlider();
		master.linkCvar("sound_mastervolume");
		master.setScaleEnd(1.0);
		master.setScaleStart(0);
		master.setWidth(colWidth * 5);
		container.add(master, x[2], y);
		
		y += yInc;
		
		soundLabel = DefaultLabel("EFFECTS VOLUME");
		soundLabel.setFont(fontSizeSmall);
		container.add(soundLabel, x[0], y);
		
		sound = DefaultSlider();
		sound.linkCvar("sound_sfxVolume");
		sound.setScaleEnd(1.0);
		sound.setScaleStart(0);
		sound.setWidth(colWidth * 5);
		container.add(sound, x[2], y);
		
		y += yInc;
		
		musicLabel = DefaultLabel("MUSIC VOLUME");
		musicLabel.setFont(fontSizeSmall);
		container.add(musicLabel, x[0], y);
		
		music = DefaultSlider();
		music.linkCvar("sound_musicvolume");
		music.setScaleEnd(1.0);
		music.setScaleStart(0);
		music.setWidth(colWidth * 5);
		container.add(music, x[2], y);
		
		y += yInc;
		
		voiceLabel = DefaultLabel("VOICE VOLUME");
		voiceLabel.setFont(fontSizeSmall);
		container.add(voiceLabel, x[0], y);
		
		voice = DefaultSlider();
		voice.linkCvar("sound_voipvolume");
		voice.setScaleEnd(1.0);
		voice.setScaleStart(0);
		voice.setWidth(colWidth * 5);
		container.add(voice, x[2], y);
		
		y += yInc;
		
		advancedLabel = DefaultLabel("ADVANCED OPTIONS");
		container.add(advancedLabel, "center", y);
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		container.add(hr, 0, y + advancedLabel.getHeight() + 3);
		
		y += yInc;
		
		driverLabel = DefaultLabel("SOUND OUTPUT");
		driverLabel.setFont(fontSizeSmall);
		container.add(driverLabel, x[0], y);
		
		driver = DefaultDropDown();
		driver.linkCvar("sound_driver");
		for i in range(int(cvar_get("sound_numDrivers"))):
			d = cvar_get("sound_driver" + str(i));
			driver.addOption(d, d);
		driver.setWidth(colWidth * 2);
		container.add(driver, x[2], y);
		
		softLabel = DefaultLabel("SOFTWARE MODE");
		softLabel.setFont(fontSizeSmall);
		container.add(softLabel, x[7] - softLabel.getWidth() - 10, y);
		
		soft = DefaultCheckBox();
		soft.linkCvar("sound_softwareModeOn");
		container.add(soft, x[7], y);
		
		y += yInc;
		
		rateLabel = DefaultLabel("SAMPLING RATE");
		rateLabel.setFont(fontSizeSmall);
		container.add(rateLabel, x[0], y);
		
		rate = DefaultDropDown();
		rate.linkCvar("sound_mixrate");
		rate.addOption("22050", "22050")
		rate.addOption("44100", "44100")
		rate.addOption("48000", "48000")
		rate.setWidth(colWidth * 2);
		container.add(rate, x[2], y);
		
		y += yInc;
		
		channelLabel = DefaultLabel("SOUND CHANNELS");
		channelLabel.setFont(fontSizeSmall);
		container.add(channelLabel, x[0], y);
		
		channel = DefaultSlider();
		channel.linkCvar("sound_numChannels");
		channel.setScaleStart(32);
		channel.setScaleEnd(256);
		channel.setStep(32);
		channel.setWidth(colWidth * 5);
		container.add(channel, x[2], y);		

		y += yInc;
		container.setHeight(y);
		
		return container;
		
	def togglePostOptions(self):
		if int(cvar_get("gfx_postProcessing")) and not self.postContainer.isVisible():
			self.postContainer.setVisible(True);
			self.gfxForm.setHeight(self.gfxForm.getHeight() + self.postContainer.getHeight());
			cvar_setvalue("vid_multisample", 0);
		elif int(cvar_get("gfx_postProcessing")) == 0 and self.postContainer.isVisible():
			self.postContainer.setVisible(False);
			self.gfxForm.setHeight(self.gfxForm.getHeight() - self.postContainer.getHeight());
		if cvar_getvalue("cl_dual_sensitivity") == 0:
			self.melee.linkCvar("cl_sensitivity_range");
		elif cvar_getvalue("cl_dual_sensitivity") == 1:
			self.melee.linkCvar("cl_sensitivity_melee");
		
	def onShow(self):
		self.togglePostOptions();
		
	def onValueChanged(self, e):
		if hasattr(e.widget, "requiresRestart") and e.widget.requiresRestart:
			self.restartRequired = True;
			self.showRestartWarning();
		else:
			self.togglePostOptions();
			
	def showRestartWarning(self):
		if not self.restartWarning.isVisible():
			self.restartWarning.setVisible(True);

			self.gfxContainer.setY(self.restartWarning.getHeight() + 15);		
			self.gfxContainer.setHeight(self.gfxContainer.getHeight() - self.restartWarning.getHeight() - 15);

			self.soundContainer.setY(self.restartWarning.getHeight() + 15);		
			self.soundContainer.setHeight(self.soundContainer.getHeight() - self.restartWarning.getHeight() - 15);

			self.interfaceContainer.setY(self.restartWarning.getHeight() + 15);		
			self.interfaceContainer.setHeight(self.interfaceContainer.getHeight() - self.restartWarning.getHeight() - 15);

			self.controlContainer.setY(self.restartWarning.getHeight() + 15);		
			self.controlContainer.setHeight(self.controlContainer.getHeight() - self.restartWarning.getHeight() - 15);
		
	def createGfxForm(self, parent):
		
		container = DefaultContainer();
		container.setWidth(parent.getWidth());
		
		(colWidth, x) = self.get8Col(container.getWidth());
		y = 0;
		yInc = 35;
		
		videoLabel = DefaultLabel("VIDEO OPTIONS");
		container.add(videoLabel, "center", y);
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		container.add(hr, 0, y + videoLabel.getHeight() + 3);
		
		y += yInc;
		
		resolutionLabel = DefaultLabel("SCREEN RESOLUTION");
		resolutionLabel.setFont(fontSizeSmall);
		container.add(resolutionLabel, x[0], y);
		
		resolution = DefaultDropDown();
		resolution.requiresRestart = True;
		resolution.addSelectionListener(self);
		resolution.linkCvar("vid_mode");
		i = 1;
		mode = cvar_get("vid_mode" + str(i));
		while len(mode) > 0:
			resolution.addOption(mode, mode);
			i += 1;
			mode = cvar_get("vid_mode" + str(i));
		resolution.setWidth(colWidth * 2);
		container.add(resolution, x[2], y);
		
		fullLabel = DefaultLabel("FULL SCREEN");
		fullLabel.setFont(fontSizeSmall);
		container.add(fullLabel, x[7] - fullLabel.getWidth() - 10, y);
		
		full = DefaultCheckBox();
		full.requiresRestart = True;
		full.addSelectionListener(self);
		full.linkCvar("vid_fullscreen");
		container.add(full, x[7], y); 
		
		y += yInc;
		
		ratioLabel = DefaultLabel("ASPECT RATIO");
		ratioLabel.setFont(fontSizeSmall);
		container.add(ratioLabel, x[0], y);
		
		ratio = DefaultDropDown();
		ratio.linkCvar("cl_fov");
		ratio.addOption("4:3", "90");
		ratio.addOption("16:9", "110");
		ratio.addOption("16:10", "100");
		ratio.setWidth(colWidth * 2);
		container.add(ratio, x[2], y);
		
		y += yInc;
		
		antiLabel = DefaultLabel("HW ANTI-ALIASING");
		antiLabel.setFont(fontSizeSmall);
		container.add(antiLabel, x[0], y);
		
		anti = DefaultDropDown();
		anti.requiresRestart = True;
		anti.addSelectionListener(self);
		anti.linkCvar("vid_multisample");
		anti.addOption("None", "0");
		anti.addOption("2x", "2");
		anti.addOption("4x", "4");
		container.add(anti, x[2], y);

		y += yInc;

		fpsLabel = DefaultLabel("SHOW FPS");
		fpsLabel.setFont(fontSizeSmall);
		container.add(fpsLabel, x[0], y);
	
		fps = DefaultDropDown();
		fps.linkCvar("cl_showfps");
		fps.addOption("No", "0");
		fps.addOption("Instant", "1");
		fps.addOption("Average", "2");
		fps.addOption("Both", "3");
		container.add(fps, x[2], y);
		
		y += yInc;
		
		vertLabel = DefaultLabel("VERTICAL SYNC");
		vertLabel.setFont(fontSizeSmall);
		container.add(vertLabel, x[0], y);
		
		vert = DefaultDropDown();
		vert.requiresRestart = True;
		vert.addSelectionListener(self);
		vert.linkCvar("gfx_vsync");
		vert.addOption("Off", "0");
		vert.addOption("On", "1");
		vert.addOption("Adaptive", "-1");
		container.add(vert, x[2], y);
		
		y += yInc;
		
		brightLabel = DefaultLabel("GAMMA LEVEL");
		brightLabel.setFont(fontSizeSmall);
		container.add(brightLabel, x[0], y);
		
		bright = DefaultSlider();
		bright.linkCvar("vid_gamma");
		bright.setScaleEnd(2.5);
		bright.setScaleStart(0.5);
		bright.setWidth(colWidth * 5);
		container.add(bright, x[2], y);
		
		y += yInc;
		
		brightLabel = DefaultLabel("BRIGHTNESS LEVEL");
		brightLabel.setFont(fontSizeSmall);
		container.add(brightLabel, x[0], y);
		
		bright = DefaultSlider();
		bright.linkCvar("vid_realbrightMult");
		bright.setScaleEnd(2);
		bright.setScaleStart(1);
		bright.setWidth(colWidth * 5);
		container.add(bright, x[2], y);
		
		y += yInc;

		renderLabel = DefaultLabel("RENDER OPTIONS");
		container.add(renderLabel, "center", y);
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		container.add(hr, 0, y + renderLabel.getHeight() + 3);
		
		y += yInc;
		
		shadowLabel = DefaultLabel("SHADOW QUALITY");
		shadowLabel.setFont(fontSizeSmall);
		container.add(shadowLabel, x[0], y);
		
		shadow = DefaultDropDown();
		shadow.linkCvar("gfx_shadow");
		shadow.addOption("Off", "0");
		shadow.addOption("Fast", "1");
		shadow.addOption("Nice", "3");
		shadow.setWidth(colWidth * 2);
		container.add(shadow, x[2], y);
		
		cpuLabel = DefaultLabel("CPU ANIMATION");
		cpuLabel.setFont(fontSizeSmall);
		container.add(cpuLabel, x[7] - cpuLabel.getWidth() - 10, y);
		
		cpu = DefaultCheckBox();
		cpu.linkCvar("gfx_forceSoftware");
		container.add(cpu, x[7], y);
		
		y += yInc;
		
		shaderLabel = DefaultLabel("SHADER QUALITY");
		shaderLabel.setFont(fontSizeSmall);
		container.add(shaderLabel, x[0], y);
		
		shader = DefaultDropDown();
		shader.linkCvar("gfx_GLSLQuality");
		shader.addOption("^900Off", "0");
		shader.addOption("Playing", "1");
		shader.addOption("Eye Candy", "3");
		shader.setWidth(colWidth * 2);
		container.add(shader, x[2], y);
		
		cloudLabel = DefaultLabel("SHOW CLOUDS");
		cloudLabel.setFont(fontSizeSmall);
		container.add(cloudLabel, x[7] - cloudLabel.getWidth() - 10, y);
		
		cloud = DefaultCheckBox();
		cloud.linkCvar("gfx_clouds");
		container.add(cloud, x[7], y);
		
		y += yInc;
		
		grassLabel = DefaultLabel("GRASS RANGE");
		grassLabel.setFont(fontSizeSmall);
		container.add(grassLabel, x[0], y);
		
		grass = DefaultSlider();
		grass.linkCvar("gfx_grassRange");
		grass.setScaleEnd(3500);
		grass.setScaleStart(100);
		grass.setWidth(colWidth * 5);
		grass.setStep(100);
		container.add(grass, x[2], y);
		
		y += yInc;
		
		postLabel = DefaultLabel("POST PROCESSING");
		postLabel.setFont(fontSizeSmall);
		container.add(postLabel, x[0], y);
		
		self.post = DefaultCheckBox();
		self.post.addSelectionListener(self);
		self.post.linkCvar("gfx_postProcessing");
		container.add(self.post, x[2], y);
		
		self.postContainer = DefaultContainer();
		self.postContainer.setWidth(container.getWidth());
		self.postContainer.setVisible(False);
		container.add(self.postContainer, x[0], y + postLabel.getHeight() + 3);
		
		tempY = 0;
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		self.postContainer.add(hr, 0, tempY);
		
		tempY += yInc - postLabel.getHeight() - 3;
		
		glowLabel = DefaultLabel("GLOW FILTER");
		glowLabel.setFont(fontSizeSmall);
		self.postContainer.add(glowLabel, x[0], tempY);
		
		glow = DefaultCheckBox();
		glow.linkCvar("gfx_glowFilter");
		self.postContainer.add(glow, x[2], tempY);
		
		blurLabel = DefaultLabel("MOTION BLUR");
		blurLabel.setFont(fontSizeSmall);
		blurLabel.setEnabled(False);
		self.postContainer.add(blurLabel, x[4], tempY);
		
		blur = DefaultCheckBox();
		blur.linkCvar("gfx_postMotion");
		blur.setEnabled(False);
		self.postContainer.add(blur, x[6], tempY);
		
		tempY += yInc;
		
		ssaoLabel = DefaultLabel("AMBIENT OCCLUSION");
		ssaoLabel.setFont(fontSizeSmall);
		self.postContainer.add(ssaoLabel, x[0], tempY);
		
		ssao = DefaultCheckBox();
		ssao.linkCvar("gfx_postSSAO");
		self.postContainer.add(ssao, x[2], tempY);
		
		waterLabel = DefaultLabel("WATER EFFECTS");
		waterLabel.setFont(fontSizeSmall);
		self.postContainer.add(waterLabel, x[4], tempY);
		
		water = DefaultCheckBox();
		water.linkCvar("gfx_postWater");
		self.postContainer.add(water, x[6], tempY);
		
		tempY += yInc;
		
		bloomLabel = DefaultLabel("BLOOM");
		bloomLabel.setFont(fontSizeSmall);
		self.postContainer.add(bloomLabel, x[0], tempY);
		
		bloom = DefaultCheckBox();
		bloom.linkCvar("gfx_postBloom");
		self.postContainer.add(bloom, x[2] , tempY);
		
		superLabel = DefaultLabel("SUPER-SAMPLED");
		superLabel.setFont(fontSizeSmall);
		self.postContainer.add(superLabel, x[4], tempY);
		
		super = DefaultCheckBox();
		super.linkCvar("vid_supersample");
		self.postContainer.add(super, x[6], tempY);
		
		tempY += yInc;
		y += yInc;
		
		self.postContainer.setHeight(tempY);
		container.setHeight(y);
		
		return container;

def getKeysForAction(action, profile):
	keys = getKeyForAction(action, profile);
	
	primaryKey = secondaryKey = None;
	if keys != None and len(keys) > 0:
		primaryKey = keys[0];
		
		if len(keys) > 1:
			secondaryKey = keys[1];
			
	return [primaryKey, secondaryKey];


def getKeycodesForAction(action, profile):
	keys = getKeyForAction(action, profile, 1);
	
	primaryKey = secondaryKey = None;
	if keys != None and len(keys) > 0:
		primaryKey = keys[0];
		
		if len(keys) > 1:
			secondaryKey = keys[1];
			
	return [primaryKey, secondaryKey];

def setBind(action, profile, key):
	bindKeyAction(key, action, profile);
	
def clearBindAction(action, profile):
	keys = getKeyForAction(action, profile);
	if keys:
		for key in keys:
			con_dprintln("clearing binds to "+key+" from profile "+str(profile)+"\n")
			if key != "-invalid-":
				unbindKeyAction(key, profile);
	
class Binder(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		self.action = None;
		self.key = None;
		self.profiles = [];

		self.setSizePct(.3,.3);
		self.setBackgroundColor(glass.Color(0,0,0,128))

		self.info = DefaultTextBox();
		self.info.setForegroundColor(glass.Color(238, 238, 238));
		self.info.setOpaque(False);
		self.info.setFocusable(False);
		self.info.setText("To choose a new bind key press a key or click on the current bind key label");
		self.info.setWidth(screenWidthPct(.25));
		self.add(self.info, "center", "top");

		self.cancel = glass.ImageButton("", "/gui/main/images/canceltr.s2g");
		self.cancel.setSize(32,32)
		self.add(self.cancel, "left", "bottom");
		self.cancel.addActionListener(self);
		self.ok = glass.ImageButton("", "/gui/main/images/yestr.s2g");
		self.ok.setSize(32,32)
		self.add(self.ok, "right", "bottom");
		self.ok.addActionListener(self);
		self.clear = DefaultButton("Clear");
		self.add(self.clear, "center", "bottom");
		self.clear.addActionListener(self);

		c = DefaultContainer();
		c.setSize(100,100);
		c.setFrameSize(1);
		self.add(c, "center", "center");

		self.keyLabel = DefaultLabel("Not Set");
		c.add(self.keyLabel, "center", "center");

		self.canvas = glass.GlassCanvas();
		self.canvas.setBackgroundColor(glass.Color(0, 0, 0, 0));
		self.canvas.setVisible(False);
		self.canvas.setOpaque(True);
		self.canvas.invisTextField = DefaultTextField();
		self.canvas.invisTextField.setVisible(False);
		c.add(self.canvas.invisTextField);
		c.add(self.canvas);
		self.canvas.setSizePct(1, 1);
		self.canvas.addMouseListener(self);
		self.canvas.addKeyListener(self);
		self.canvas.invisTextField.addKeyListener(self);
	
		# TODO: add button to set to default
		self.setVisible(False);	
		
	def onAction(self, e):
		if e.widget is self.ok:
			# the bind is done here
			for profile in self.profiles:
				if self.handle.hotkey is False:
					clearBindAction(self.action, profile);
				if self.key is not None:
					setBind(self.action, profile, self.key);
				self.updateKeys(profile);
			self.setVisible(False);
		elif e.widget is self.clear:
			self.updateLabel(None);
			self.key = None;
		elif e.widget is self.cancel:
			self.setVisible(False);
		
	# profile = -1 is a general bind and is to be applied to all profiles
	# profile = 0 is a player bind and is to be applied to 2 as well for spectators
	# profile = 1 is commander binds 
	def show(self, handle):

		profiles = {
			"GENERAL": [0, 1, 2],
			"PLAYER": [0, 2],
			"COMMANDER": [1]
		};
		
		self.action = handle.bindAction;
		self.profiles = profiles[handle.profile];
		self.handle = handle;
		self.key = getKeyFromName(handle.getCaption());
		self.centerWindow();
		self.keyLabel.setCaption(handle.getCaption());
		self.keyLabel.setX(50-self.keyLabel.getWidth()//2)
		self.setVisible(True);
		mainmenu.blocker.setSizePct(1,1);
		mainmenu.blocker.setVisible(True);
		mainmenu.blocker.requestMoveToTop();
		self.requestMoveToTop();
		self.canvas.setVisible(True);
		self.canvas.invisTextField.setVisible(True);
		self.canvas.invisTextField.setPosition(-100, -100);
		self.canvas.invisTextField.requestFocus();

		# TODO: attach this profile and action to the default and clear buttons
		
	def setVisible(self, visible):
		DefaultWindow.setVisible(self, visible);
		self.canvas.setVisible(visible);
		self.canvas.invisTextField.setVisible(visible);
		if visible == 1:
			self.canvas.invisTextField.setPosition(-100, -100);
			self.canvas.invisTextField.requestFocus();
			
		mainmenu.blocker.setVisible(visible);
		self.releaseModalFocus();

	def updateLabel(self, key):
		if key is None:
			self.keyLabel.setCaption("unset");
		else:
			keyString = getNameFromKey(key);
			self.keyLabel.setCaption(keyString.capitalize());
		self.keyLabel.setX(50-self.keyLabel.getWidth()//2)
		self.canvas.invisTextField.requestFocus();
		
	def updateKeys(self, profile):
		profileIds = ["PLAYER", "COMMANDER", "SPECTATOR"];
		for bind in options.bondage:
			if bind.bindAction == self.action and (bind.profile == profileIds[profile] or (bind.profile == "GENERAL" and profile == 0)):
				if bind.hotkey == False:
					keys = getKeysForAction(self.action, profile);
				else:
					keys = [getHotkeyForAction(self.action)];
				key = keys[bind.priority];
				if key is None:
					bind.setCaption("unset");
				else:
					bind.setCaption(key.capitalize());
					
		
	def onMousePress(self, e):
		self.onMouseClick(e);
		
	def onMouseReleased(self, e):
		pass;
	
	def onMouseClick(self, e):
		if e.button == 4:
			b = 236;
		elif e.button == 5:
			b = 237;
		else:
			b = e.button + 199;

		self.key = b;
		self.updateLabel(self.key);

	def onMouseScroll(self, e):
		self.key = e.button+199;
		self.updateLabel(self.key);

	def onKeyPress(self, e):
		self.key = e.key;
		self.updateLabel(self.key);

	def onKeyReleased(self, e):
		pass;
	
	def onMouseMotion(self, e):
		pass;
 
	def onMouseDrag(self, e):

		pass;
	def onMouseEnter(self, e):
		pass;
 
	def onMouseExit(self, e):
		pass;

options = OptionsSection();
#TODO
mainmenu.modules["menu"].addSection("options", options);
options._create();


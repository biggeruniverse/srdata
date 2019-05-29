# (c) 2011 savagerebirth.com

import glass;

class GlassTopStatusBar(DefaultContainer):
	def __init__(self):
		
		DefaultContainer.__init__(self);
		
		self.setSize(screenWidth, 40);zzz
		
		bg = DefaultLabel();
		bg.setImage("top_bar.s2g");
		bg.setSize(screenWidth, 32);
		self.add(bg);
		
		glbDefaultImgFactory.setImageClass(DefaultImage);
		glbDefaultImgFactory.setDefaults({'height': 21, 'width': 21, 'imagePath': "icons/", 'ext': "png"});
		
		quit = glbDefaultImgFactory.create("quit");
		quit.setClickAction("mainmenu.show_confirmquit();");
		self.add(quit, 10, 6, "right");
		
		self.sectionWidth = screenWidth // 3;
		self.sectionHeight = 35;
		
		# Left
		self.left = DefaultContainer();
		self.left.setSize(self.sectionWidth, self.sectionHeight);
		self.add(self.left);
		
		time = DefaultLabel("4:04 AM");
		self.left.add(time, 10, "center");
		
		x = time.getWidth() + 20;
		incX = 30;
		
		options = glbDefaultImgFactory.create("options");
		# TODO: show options
		self.left.add(options, x, "center");
		
		x += incX;
		demos = glbDefaultImgFactory.create("demos");
		# TODO: show demo stuff
		self.left.add(demos, x, "center");
		
		x += incX;
		log = glbDefaultImgFactory.create("log");
		# TODO: show console log
		self.left.add(log, x, "center");
		
		x += incX + 10;
		playersIcon = glbDefaultImgFactory.create("players");
		self.left.add(playersIcon, x, "center");
		
		x += incX - 5;
		players = DefaultLabel("54,239");
		self.left.add(players, x, "center");
		
		# Middle
		self.middle = DefaultContainer();
		self.middle.setSize(self.sectionWidth, self.sectionHeight);
		self.add(self.middle, "center", "top");
		
		# create account OR avatar, username, stats, logout
		create = DefaultLabel("Create Account");
		self.middle.add(create, "center", "center");
		
		# Right
		self.sectionWidth -= 50;
		self.right = DefaultContainer();
		self.right.setSize(self.sectionWidth, self.sectionHeight);self.right.setBackgroundColor = glass.Color(0, 255, 0);
		self.add(self.right, 50, "top", "right");
		
		# username, password, submit OR messages, buddies, clans, notifications
		self.submit = glbDefaultImgFactory.create("login");
		self.submit.addActionListener(self);
		self.right.add(self.submit, "right", "center");
		
		self.password = DefaultTextField();
		self.password.setPlaceHolder("password...");
		self.password.setSize(110, 20);
		self.password.addKeyListener(self);
		self.right.add(self.password, 31, "center", "right");
		
		self.username = DefaultTextField();
		self.username.setPlaceHolder("Username...");
		self.username.setSize(110, 20);
		self.username.addKeyListener(self);
		self.right.add(self.username, 151, "center", "right");
		
	def login(self):
		if cvar_get("auth_sessionid") == "":
			cvar_set("username", self.username.getText());
			cvar_set("password", self.password.getText());
		
			self.submit.setVisibility(0);
			self.working.setVisibility(1);
			
			self.httpHandle = CL_Auth_Authenticate();

	def show(self):
		if self.seq is not None:
			self.seq.stop();
		self.seq=ActionSequence(SlideAction(self, 0, 0));

		if len(cvar_get("auth_sessionid")) > 1:
			self.logout.setVisible(True);
			self.login.setVisible(False);
			self.statsbutton.setVisible(True);
		else:
			self.login.setVisible(True);
			self.logout.setVisible(False);
			self.statsbutton.setVisible(False);

	def hide(self):
		if self.seq is not None:
			self.seq.stop();
		self.seq=ActionSequence(SlideAction(self, 0, -32));

	def onAction(self, e):
		if e.widget.getCaption() == "login":
			self.startLogin();

	def connected(self):
		self.server.setCaption("Connected to "+Client_GetStateString("svr_name"));
		self.server.adjustSize();
		self.server.setX((screenWidth-self.server.getWidth())//2);

		self.disconnect.setX(self.server.getX() + self.server.getWidth()+4);
		self.disconnect.setVisible(True);

	def disconnected(self):
		self.server.setCaption("Not connected to a server");
		self.server.setCaption("");
		self.server.adjustSize();
		self.server.setX((screenWidth-self.server.getWidth())//2);
		self.disconnect.setVisible(False);

	def onEvent(self, e):
		if e.scope != "auth":
			return;
		if e.string == "login":
			self.authstatus.setCaption("Logged in as "+cvar_get('name')); #add website icon
			self.login.setVisible(False);
			self.logout.setVisible(True);
			self.statsbutton.setVisible(True);
		elif e.string == "logout":
			self.authstatus.setCaption("Not logged in");
			self.login.setVisible(True);
			self.logout.setVisible(False);
			self.statsbutton.setVisible(False);


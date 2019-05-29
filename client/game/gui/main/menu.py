# (c) 2010 savagerebirth.com

from silverback import *;
import glass;
#import random;
import logging;

logger = logging.getLogger("gui")

class Menu(DefaultWindow):

	def __init__(self):
		DefaultWindow.__init__(self);
		self.alertWindow = None;
		self.setBackgroundColor(transparency);
		self.setSize(980, 530);

		self.sectionStack = {};
		self.currentSection = "serverlist";
		self.previousSection = None;		

		msgs = [
			"Confirm making a huge mistake in your life?",
			"You want to quit? Then thou hast lost an eighth!",
			"Yeah, get to your WoW-addicts anonymous meeting. Addict.",
			"Don't quit! Savage makes a great chat client!",
			"Press Cancel to quit. Psych!",
			"You've almost reached that achievement, just play a bit longer...",
			"Very well then, be that way! We won't even bother with the traditional royal farewell!"
		];

		msg = M_Randnum() % len(msgs);

		self.quitConfirm = DefaultConfirm(msgs[msg], "shutdown();", "Quit");
		self.add(self.quitConfirm, "center", "center");

		class ButtonGroup:
			def __init__(self, buttonList):
				self.buttons = buttonList;
				self.selectionListeners = [];
				self.selected = 0;

				for i, button in enumerate(self.buttons):
					button.addActionListener(self);
				self.buttons[self.selected].setState(glass.ImageButton.GB_PRESSED);                                

			def onAction(self, e):
				self.buttons[self.selected].setState(glass.ImageButton.GB_IDLE);
				self.selected = self.buttons.index(e.widget);
				self.buttons[self.selected].setState(glass.ImageButton.GB_PRESSED);

				e = glass.ValueChangedEvent(self);
				for l in self.selectionListeners:
					l.onValueChanged(e);

			def addSelectionListener(self, listener):
				self.selectionListeners.append(listener);

			def getSelection(self):
				return self.buttons[self.selected];

		joinGame = glass.GlassButton("JOIN A GAME");
		joinGame.setStyle("main");
		joinGame.setSize(264, 42);
		joinGame.setFont(fontSizeLarge);
		self.add(joinGame, 0, 0)

		hostGame = glass.GlassButton("HOST GAME");
		hostGame.setStyle("main");
		hostGame.setSize(264, 42);
		hostGame.setFont(fontSizeLarge);
		self.add(hostGame, 0, 52)

		options = glass.GlassButton("OPTIONS");
		options.setStyle("main");
		options.setSize(264, 42);
		options.setFont(fontSizeLarge);
		self.add(options, 0, 104)

		self.buttonGroup = ButtonGroup( [joinGame, hostGame, options] );
		self.buttonGroup.addSelectionListener(self);

		self.quit = glass.GlassButton("QUIT");
		self.quit.setStyle("main");
		self.quit.setSize(264, 42);
		self.quit.setClickAction("mainmenu.modules['menu'].quitConfirm.setVisible(True)");
		self.quit.setFont(fontSizeLarge);
		self.add(self.quit, 0, 156);

		# Until big fixes windows:

		class NewsWindow(DefaultWindow):
			def __init__(self):
				DefaultWindow.__init__(self);
				self.setFrameStyle("TrimmedEight");				
				self.httpHandle = -1;
				gblEventHandler.addHttpListener(self);

				self.setSize(265, 200);
				self.setVisible(False);
				self.setTitleVisible(False);
				self.setBackgroundColor(windowBackground);

				top = DefaultContainer();
				self.add(top, 0, 0);
				top.setSize(self.getWidth(), 35);
				top.setBackgroundColor(windowTop);

				"""

				title = DefaultImage();
				title.setImage("txt_savagenews.png");
				top.add(title, "center", "center");

				content = DefaultContainer();
				self.add(content, 10, 42);
				content.setSize(245, 148);

				self.heading = DefaultLabel("Savage Rebirth Pre-Beta has begun!")
				content.add(self.heading, 0, 0);
				self.heading.setFont(fontSizeSmall);
				"""

				title = DefaultLabel("Important Bulletin");
				title.setForegroundColor(tangoYellowDark);
				title.setFont(fontSizeLarge);
				top.add(title, "center", "center");

				self.text = DefaultTextBox("No News.");
				self.text.setSize(245, 200);
				self.text.setBackgroundColor(transparency);
				self.text.setForegroundColor(glass.Color(211, 201, 168));
				self.text.setFont(fontSizeSmall);
				self.text.setEditable(False);
				self.add(self.text, 10, 50);

				"""

				self.date = DefaultLabel("7:16pm, 3.11.2011");
				self.date.setFont(fontSizeSmall);
				content.add(self.date, "left", "bottom");

				self.readMore = DefaultLabel("...read more");
				self.readMore.setFont(fontSizeSmall);
				self.readMore.setForegroundColor(tangoYellow);
				self.readMore.addActionListener(self);
				content.add(self.readMore, "right", "bottom");

				"""
			def getNews(self):
				self.httpHandle = HTTP_Get("http://savagerebirth.com/misc/news");

			def onEvent(self, e):
				if e.handle == self.httpHandle:			
					self.httpHandle = -1;
					msg = e.responseMessage; #.replace("\n", " ");
					if len(msg) == 0:
						self.setVisible(False);
					else:
						self.setVisible(True);
						self.text.setText(msg);
				#else:
				#	self.setVisible(False);


		div = DefaultDivider();
		div.setForegroundColor(tangoRed);
		self.add(div, 0, self.quit.getY() + self.quit.getHeight() + 10);
		div.setWidth(self.quit.getWidth());

		self.news = NewsWindow();
		self.add(self.news, 0, div.getY() + div.getHeight() + 10);

		if int(cvar_get("con_developer")):
			#execwindow.newExecWindow("mainmenu");
			#self.add(DevTools(), 0, self.quit.getY() + self.quit.getHeight() + 10);
			pass;

	def onValueChanged(self, e):
		caption = e.widget.getSelection().getCaption();
		if caption == "JOIN A GAME":
			self.showSection("serverlist");
		elif caption == "HOST GAME":
			self.showSection("hostgame");
		elif caption == "OPTIONS":
			self.showSection("options");

	def addSection(self, name, obj):
		self.sectionStack[name] = obj;
		self.add(obj, self.quit.getWidth() + 15, 0);
		obj.setSize(690, self.getHeight() - 65);
		obj.setVisible(False);

	def showSection(self, name):
		
		if name == 'previous' and self.previousSection is not None:
			name = self.previousSection;
			self.previousSection = None;
		
		logger.debug("Showing section: %s", (str(name)));
		
		if name in self.sectionStack:
			
			if self.currentSection is not None:
				if self.sectionStack[self.currentSection].onHide() is not None:
					return;
				
				self.previousSection = self.currentSection;
				self.sectionStack[self.currentSection].setVisible(False);
			
			self.currentSection = name;
			self.sectionStack[name].setVisible(True);
			self.sectionStack[name].onShow();

		else:
			logger.warn("Section \"%s\" doesn't exist", (str(name)));

	def onShow(self):
		self.showSection(self.currentSection);
		self.news.getNews();

menu = Menu();
mainmenu.addModule("menu", menu);
mainmenu.showModule("menu");
menu.showSection("serverlist");

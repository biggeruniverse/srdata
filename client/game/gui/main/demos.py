#copyright savagerebirth.com (c) 2011
#demo screen

from silverback import *;
import glass;
import gdata.youtube;
import gdata.youtube.service;

class DemosLoadAction(Action):
	def __init__(self, win):
		Action.__init__(self);
		self.list = File_ListFiles("/demos/", "*.demo", 0);
		self.done = False;
		self.window = win;

	def run(self):
		for demo in self.list:
			demos.list.addWidgetItem(DemoListItem(demo, self.window.getWidth()//3))
			#TODO: maybe add the Demo_GetInfo here

		self.window.list.setWidth(self.window.getWidth()//3);
		self.done = True;

	def isDone(self):
		return self.done;

class DemoListItem(DefaultContainer):
	def __init__(self, demoname, width):
		DefaultContainer.__init__(self);
		self.demoname = demoname;
		self.setId(demoname);
		
		self.mapName = DefaultLabel("?map?");
		self.add(self.mapName, 66,1);
		
		self.server = DefaultLabel("?server?");
		self.add(self.server, 66,15);
		
		self.overhead = DefaultImage();
		self.overhead.setSize(64,64);
		self.add(self.overhead, 1,1);
		
		self.setSize(width, 66);
		
		self.icons = [];
		i = DefaultImage();
		i.setImage("icons/shield.s2g");
		i.setSize(32,32);
		self.add(i, 65, 34);
		self.icons.append(i);
		i = DefaultImage();
		i.setImage("icons/hvb.s2g");
		self.add(i, 98, 34);
		self.icons.append(i);
		
		self.update();

	def update(self):
		data = Demo_GetInfo(self.demoname);
		overhead = "/world/"+data["world"]+"_overhead.jpg";
		
		w, h = self.overhead.getWidth(), self.overhead.getHeight();
		Host_VerifyOverhead(overhead);
		self.overhead.setImage(overhead, "none", 1);
		self.overhead.setSize(w,h);
		
		world = "/world/"+data["world"]+".s2z";
		
		self.server.setCaption(data["server"]);
		self.server.adjustSize();
		
		record = "#"+str(data["matchid"]);
		if data["matchid"] == 0:
			record = "";
		self.mapName.setCaption(data["world"] + " "+record);
		self.mapName.adjustSize();
		
		self.updateIcons(data);
		
	def updateIcons(self, data):
		#do the icons part
		if data["matchid"] == 0:
			self.icons[0].setEnabled(0);
		else:
			self.icons[0].setEnabled(1);
			
		self.icons[1].setImage("icons/"+data["races"]+".s2g");
		self.icons[1].setSize(32, 32);


class DemoHandler:
	def __init__(self, win):
		self.window = win;
		
	def getSelectedDemo(self, name=False):
		s = self.window.list.getItem(self.window.list.getSelected());
		if name:
			s = s[7:-5]; #remove /demos/ and .demo
		return s;
	
	def onValueChanged(self, e):
		path = self.getSelectedDemo();
		
		data = Demo_GetInfo(path);
		
		data["msgs"] = Demo_GetMessages(path);
		
		self.window.update(data);
	
	def play(self):
		path = self.getSelectedDemo();
		Demo_Play(path);

	def getModalFocus(self):
		demos.confirmWin.setVisible(1);
		demos.confirmWin.requestModalFocus();
		ActionSequence(FadeInAction(demos.backdrop, target=180));
		#seems to be executing too fast. TODO make the fade actions work like guiaction??
	
	def confirmDelete(self):
		self.getModalFocus();
		demos.confirmWin.setCaption("Delete Demo");
		demos.confirmWin.setVisible(1);
		
		s = "Are you sure you want to delete\n" + self.getSelectedDemo(name=True) + ".demo?";
		demos.confirm.setVisible(1);
		demos.confirm.setCaption(s);
		demos.confirm.adjustSize();
		demos.input.setVisible(0);
		
		winWidth = 8+demos.confirm.getWidth();
		demos.confirmWin.setWidth(winWidth);
		demos.confirmWin.centerWindow();
		
		demos.yes.setCaption("Yes");
		demos.no.setCaption("No");
		widgetWidth = demos.yes.getWidth() + 16 + demos.no.getWidth();
		demos.yes.setX((winWidth - widgetWidth)//2);
		demos.no.setX(demos.yes.getX() + demos.yes.getWidth() + 16);
	
	def confirmRename(self):
		self.getModalFocus();
		demos.confirmWin.setCaption("Rename Demo");
		demos.confirmWin.setVisible(1);
		
		demos.confirm.setVisible(0);
		demos.confirm.adjustSize();
		demos.input.setVisible(1);
		demos.input.setText(self.getSelectedDemo(name=True)+".demo");
		
		winWidth = 8+demos.input.getWidth();
		demos.confirmWin.setWidth(winWidth);
		demos.confirmWin.centerWindow();
		
		demos.yes.setCaption("Rename");
		demos.no.setCaption("Cancel");
		widgetWidth = demos.yes.getWidth() + 16 + demos.no.getWidth();
		demos.yes.setX((winWidth - widgetWidth)//2);
		demos.no.setX(demos.yes.getX() + demos.yes.getWidth() + 16);
	
	def onAction(self, e):
		if e.widget is self.window.play:
			path = self.getSelectedDemo();
			cvar_setvalue("demo_makeMovie", 0);
			Demo_Play(path);
			
		elif e.widget is self.window.convert:
			path = self.getSelectedDemo();
			cvar_setvalue("demo_makeMovie", 1);
			Demo_Play(path);
	
	def hideConfirm(self):
		ActionSequence(FadeOutAction(demos.backdrop, target=0));
		demos.confirmWin.releaseModalFocus();
		demos.confirmWin.setVisible(0);
		
class UploadHandler:
	def __init__(self):
		import gdata.youtube;
		import gdata.youtube.service;
		## set up the yt service object		
		self.yt_service = gdata.youtube.service.YouTubeService();
		self.yt_service.ssl = False # documentation says that ssl is not ready/finished yet
		#self.yt_service.developer_key = "AI39si7Dksm64Mm-l5sW3prUoVNCbm9LC_RdQdIj0fSA_FUR8KjIE2ampVhxseyuEII8L212uwa68jaogblrlHkPInzj8uMyFw"
		#self.yt_service.source = 'justsometesting' # program name, should be Savage: Rebirth or something similar 
		self.previousContent = [];
		self.currentContent = [];
		self.titles = [["Next", "Select a video."], ["Log in", "Log in to your YouTube account."], ["Upload", "Edit video information"]];
		self.count = 0;
		self.videopath = "";
		self.standardKeywords = "SR, Savage, Rebirth, Savage Rebirth, iminspace, rts, fps"; #Maybe ask Tirza about some standard keywords, she's the one who knows everything about YouTube.
	
	def showUploadWin(self):
		self.currentContent = demos.contents[0];
		demos.uploadWin.setVisible(1);
		supportedEndings = ["*.mov", "*.mp4", "*.avi", "*.wmv"]; # I have no idea which video formats youtube supports; maybe this could be done in an easier way
		paths = [];
		for ending in supportedEndings:
			path = File_ListFiles("/demos",ending,0);	
			for video in path:
				paths.append(video);
		for path in paths:
			demos.videoList.addItem(str(path));
			
	def getVideoFile(self):	
		v = demos.videoList.getItem(demos.videoList.getSelected());
		return v;
		
	def swapContents(self, dir):
		self.previousContent = self.currentContent;
		self.count += dir;
		if self.count < 0 or self.count > 2:
			self.count = 0;
			demos.uploadWin.setVisible(0);
			self.currentContent = [];
		self.currentContent = demos.contents[self.count];		
		for element in self.previousContent:
			element.setVisible(0);
		for element in self.currentContent:	
			element.setVisible(1);	
		demos.next.setCaption(self.titles[self.count][0]);
		demos.title.setCaption(self.titles[self.count][1]);
		
	def onAction(self, e):
		widget = e.widget;
		if widget == demos.next:	
			#TODO: put a "Stop-icon" behind unfilled textfields
			if widget.getCaption() == "Next":
				self.videopath = self.getVideoFile();
			elif widget.getCaption() == "Log in":
				demos.uploadWin.workingWindow(1);
				#self.yt_service.email = demos.usernameInput.getText();
				#self.yt_service.password = demos.passwordInput.getText();
				#self.yt_service.ProgrammaticLogin(); 
				demos.uploadWin.workingWindow(0);
			elif widget.getCaption() == "Upload":
				videoTitle = demos.titleInput.getText();
				videoKeywords = self.standardKeywords + " , " + demos.keywordsInput.getText();
				videoDescription = demos.descriptionInput.getText();
				#mediaGroup = gdata.media.Group(
				# title =gdata.media.Title(text=videoTitle), 
				# description = gdata.media.Description(description_type='plain', text=videoDescription), 
				# keywords=gdata.media.Keywords(text=videoKeywords), 
				# category=[gdata.media.Category(text='Gaming', scheme='http://gdata.youtube.com/schemas/2007/categories.cat', label='Gaming')], 
				# player=None #The category scheme thingy is strange...
				# )
				#video_entry = gdata.youtube.YouTubeVideoEntry(media=mediaGroup);
				con_println("Uploading now...");
				#new_entry = yt_service.InsertVideoEntry(video_entry, self.videopath);
				## TODO: Show progress bar and video url; send a message to the devs somehow ( a video list would be nice)
				con_println("Finished uploading");
				## TODO: Put that ^ in a own function maybe
			self.swapContents(1);
		if widget == demos.back:
			self.swapContents(-1);			

class DemoWindow(DefaultWindow):
	def __init__(self):
		DefaultWindow.__init__(self);
		self.setFrameStyle("TrimmedEight");
		self.setBackgroundColor(glass.Color(24, 14, 14));

		self.setSize(int(screenWidth*.9), 458);
		self.loadingAction = None;

		self.handler = DemoHandler(self);

		bgImage = DefaultImage();
		bgImage.setImage("bar_red_shadow.png");
		bgImage.setSize(self.getWidth(), 20);
		self.add(bgImage, 0, 40);

		header = DefaultContainer();
		header.setSize(self.getWidth(), 40);
		header.setBackgroundColor(glass.Color(85, 21, 11));
		header.setOpaque(1);
		self.add(header);

		title = DefaultImage();
		title.setImage("txt_options.png");
		header.add(title, "center", 10);

		self.list = glass.GlassListBox();
		self.list.addSelectionListener(self.handler);
		
		scroll = glass.GlassScrollArea();
		scroll.setContent(self.list);
		scroll.setScrollPolicy(glass.GlassScrollArea.SHOW_NEVER, glass.GlassScrollArea.SHOW_ALWAYS);
		self.add(scroll);
		scroll.setPosition(10,70);
		scroll.setSize(self.getWidth()//3, self.getHeight()-100);
		
		self.match = DefaultLabel();
		self.match.setFont(fontSizeLarge);
		self.add(self.match, self.getWidth()//3+20, 70);
		
		#info container
		
		container = DefaultContainer();
		self.add(container, self.getWidth()//3+20, self.match.getHeight()+80);
		
		self.matchMap = DefaultLabel();
		self.matchMap.setSize(128, 128);
		container.add(self.matchMap, 0, 0)
		
		self.played = DefaultLabel();
		container.add(self.played, 128+10, 0);
		
		self.matchLength = DefaultLabel();
		container.add(self.matchLength, 128+10, self.played.getHeight());
		
		self.size = DefaultLabel();
		container.add(self.size, 128+10, self.played.getHeight()+self.matchLength.getHeight());
		
		self.chat = DefaultTextBox();
		self.chat.setSize(2*self.getWidth()//3, 200);
		self.chat.setOpaque(0);
		scroll = glass.GlassScrollArea();
		scroll.setContent(self.chat);
		scroll.setSize(self.getWidth()//3, 200);
		container.add(scroll, 0, 128+10);
		
		container.setSize(2*self.getWidth()//3-20, 400);
	
		#action container
		
		container = DefaultContainer();
		container.setSize(self.getWidth()//3, self.getHeight());
		self.add(container, self.getWidth()*2//3+40, self.match.getHeight()+80);
		
		l = DefaultLabel("Quality");
		container.add(l);
		
		self.quality = DefaultDropDown();
		self.quality.linkCvar("ven_bitrate");
		self.quality.addOption("Low", "1347000");
		self.quality.addOption("Standard", "3500000");
		self.quality.addOption("High", "15500000");
		self.quality.addOption("HD", "25500000");
		container.add(self.quality, l.getWidth(), 0);
		
		l = DefaultLabel("Video");
		container.add(l, 0, self.quality.getHeight()+10);
		self.vencoder = DefaultDropDown();
		self.vencoder.linkCvar("ven_codec");
		self.vencoder.addOption("H.264", "libx264");
		self.vencoder.addOption("MPEG-4", "mpeg4");
		self.vencoder.addOption("WMP 8", "wmv2");
		container.add(self.vencoder, l.getWidth(), self.quality.getHeight()+10);
		
		self.convert = DefaultButton("<>");
		self.convert.addActionListener(self.handler);
		container.add(self.convert, 0, self.vencoder.getHeight()+self.quality.getHeight()+20);
		
		self.play = DefaultButton(">");
		self.play.addActionListener(self.handler);
		container.add(self.play, 40, self.vencoder.getHeight()+self.quality.getHeight()+20);
	
	def update(self, data):
		name = "Unofficial Match on "+data["server"];
		
		if data["matchid"] > 0:
			name = "Match #"+str(data["matchid"])+" on "+data["server"];
		
		self.match.setCaption(name);
		
		overhead = "/world/"+data["world"]+"_overhead.jpg";
		Host_VerifyOverhead(overhead);
			
		w, h = self.matchMap.getWidth(), self.matchMap.getHeight();
		self.matchMap.setImage(overhead, 1);
		self.matchMap.setSize(w,h);
		
		self.played.setCaption(data["datetime"]);
		self.played.adjustSize();
		
		m, s = divmod(data['length'], 60)
		h, m = divmod(m, 60)
		self.matchLength.setCaption("Length: %02d:%02d:%02d" % (h,m,s));
		
		size = data['filesize'] * 2**-20;
		self.size.setCaption("Size: "+ str(round(size, 2)) +" MB");
		
		self.chat.setText("");
		for line in data["msgs"]:
			self.chat.addRow(line);
		self.size.adjustSize();
		
	def onShow(self):
		if self.loadingAction is not None:
			self.loadingAction.stop();
		self.list.erase();
		self.loadingAction = ActionSequence(DemosLoadAction(self));

demos = DemoWindow();
mainmenu.addModule("demos", demos);
demos.setX(int(screenWidth*.05));

# (c) 2010 savagerebirth.com

from silverback import *;
import glass;

def frame():
	# No idea why section.frame() gets called here: No section has a frame method.
	"""
	if mainmenu.menu.currentSection is not None:
		mainmenu.menu.sectionStack[mainmenu.currentSection].frame();
	"""
	pass;

def onShow():
	GUI_ShowCursor("arrow");
	mainmenu.topBar.doAutoLogin();
	try:
		mainmenu.modules["menu"].onShow()
	except KeyError:
		con_println("KeyError: There is no mainmenu module named menu");


def add(obj, x=None, y=None):    
	if x is not None:
		obj.setPosition(x, y);
	glass.GUI_ScreenAddWidget("mainmenu", obj);

def addModule(name, obj):
	# Every "module" should have the same position
	mainmenu.modules[name] = obj	
	obj.setVisible(False);	
	mainmenu.content.add(obj);	
	obj.setX(screenWidth // 2 - obj.getWidth() // 2);

def showModule(name):
	for modName in mainmenu.modules:
		visible = True if modName == name else False;
		try:
			mainmenu.modules[modName].setVisible(visible);
		except KeyError:
			con_println("KeyError: There is no mainmenu module named " + name);
	mainmenu.currentModule = name;
	try:
		mainmenu.modules[mainmenu.currentModule].onShow();
	except AttributeError:
			con_println("AttributeError: A manmenu module has no attribute 'onShow'");
	

def show_gameerror(msg):
	mainmenu.alert(msg);

def show_mismatch(msg):
	mainmenu.mismatchWindow.setVisible(True);
	

def alert(msg, okLabel="Ok"):
	if mainmenu.alertWindow is None:
		mainmenu.alertWindow = DefaultAlert(msg);
		mainmenu.add(mainmenu.alertWindow);

	mainmenu.alertWindow.msg.setText(msg);
	mainmenu.alertWindow.ok.setCaption(okLabel);

	mainmenu.alertWindow.setVisible(True);

def showLoading():
	mainmenu.loading.setVisible(True);
	mainmenu.loading.setAlpha(255);

def hideLoading():
	ActionSequence(FadeOutAction(mainmenu.loading));

modules = {}
currentModule = None
alertWindow = None;
mismatchWindow = DefaultWindow();
mismatchWindow.setVisible(False);

# Logo:
logo = DefaultImage();
logo.setImage("logo.png");
logo.setSize(int(logo.getWidth() * 0.5), int(logo.getHeight() * 0.5));
add(logo, screenWidth // 2 - logo.getWidth() // 2, 80);

#content container
content = DefaultContainer();
content.setSize(screenWidth, screenHeight-290);
add(content, 0, 290);
#joinGame = glass.GlassButton("Join Game");
#joinGame.setStyle("main");
#joinGame.setClickAction("con_println('CLICKED');");
#add(joinGame, screenWidth // 2 - 490, 170);
#joinGame.setSize(263, 42)

# Top bar
topBar = MainTopBar();
add(topBar);

loading = DefaultWindow();
loading.setSize(screenWidth, screenHeight);
loading.setBackgroundColor(black);
#loading.setOpaque(False);
loadbg = DefaultImage();
loadbg.setImage("loadbg.png");
loading.add(loadbg);
loadbg.setSizePct(1,1);
loadtitle = DefaultImage();
loadtitle.setImage("loadtitle.png");
loading.add(loadtitle);
loadtitle.scale(0.5);
loadtitle.setPosition(screenWidth//2-loadtitle.getWidth()//2, screenHeight//2-loadtitle.getHeight()//2);
add(loading, 0, 0);

blocker = DefaultContainer();
blocker.setBackgroundColor(glass.Color(0,0,0,80));
blocker.setSizePct(1,1);
blocker.setVisible(False);
add(blocker);

#if int(cvar_get("con_developer")) == 1:
#	add(DevTools(), 0, 50);


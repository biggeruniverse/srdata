# (c) 2010 savagerebirth.com
# this file creates the mainmenu

from silverback import *;
import glass;

def frame():
	pass;

def onShow():
	if mainmenu.overlay.getAlpha() > 0:
		ActionSequence(FadeOutAction(mainmenu.overlay,step=6));
	Sound_StopMusic();
	Sound_PlayMusic('/music/interface/menu'+str(M_Randnum()%2+1)+'.ogg');
	if cvar_getvalue("autologin") == 1:
		mainmenu.authwin.startLogin();
	IRC_Connect("irc.freenode.net");

	if isConnected():
		mainmenu.ret.setVisible(1);
                mainmenu.play.setVisible(0);
		mainmenu.topstatus.connected();
	else:
		mainmenu.ret.setVisible(0);
                mainmenu.play.setVisible(1);
		mainmenu.topstatus.disconnected();
	mainmenu.topstatus.show();

#this screen is created by silverback hardcode, for some reason
#Big: because it should never be overridden

trap = glass.GlassContainer();
glass.GUI_ScreenAddWidget("mainmenu", trap);
trap.setSizePct(1,1);
trap.setPosition(0,0);

backdrop = glass.GlassWindow();
backdrop.setTitleVisible(0);
backdrop.setBackgroundColor(glass.Color(233, 233, 187, 64));
backdrop.setGradientColor(glass.Color(233, 233, 187, 0));
backdrop.setSize(600, screenHeight);
backdrop.setPosition(screenWidth / 2 - 300, 0);
backdrop.setFocusable(0);
trap.add(backdrop);

testConfirm = DefaultConfirm("You sure bro?", "test1", "test2", "test3");
#test = DefaultWindow("test");
#con_println("TEST2\n");
#test = glass.GlassWindow("TEST");con_println("TEST\n");
glass.GUI_ScreenAddWidget("mainmenu", testConfirm);

topstatus = GlassTopStatusBar();
glass.GUI_ScreenAddWidget("mainmenu", topstatus);
gblEventHandler.addNotifyListener(topstatus);

logo = glass.GlassLabel();
logo.setImage("/gui/standard/logo.png");
logo.setSize(int(logo.getWidth()*0.5), int(logo.getHeight()*0.5));
logo.setPositionPct( 0.5-(logo.getWidth()/float(screenWidth))*0.5, 0.25);
glass.GUI_ScreenAddWidget("mainmenu",logo);

play = gblButtonFactory.createInstance("Play");
play.setClickAction("mainmenu.playgame();");
backdrop.add(play);
play.setWidth(80);
play.setPositionPct(.41, .6);

def playgame():
	#if isAuthed: #TODO
	GUI_ShowScreen('serverlist')
	#else:
	#	mainmenu.show_login();

def disconnected():
	mainmenu.ret.setVisible(0);
	mainmenu.play.setVisible(1);
	mainmenu.topstatus.disconnected();

ret = gblButtonFactory.createInstance("Return");
backdrop.add(ret);
ret.setWidth(80);
ret.setPositionPct(.41, .6);
ret.setClickAction("GUI_ShowScreen('lobby')");
ret.setVisible(0);

options = gblButtonFactory.createInstance("Options");
options.setClickAction("mainmenu.optionwin.setVisible(1);");
backdrop.add(options);
options.setPositionPct(.1, .6);
options.setWidth(80);

demos = gblButtonFactory.createInstance("Demos");
backdrop.add(demos);
demos.setWidth(80);
demos.setPositionPct(.72, .6);
demos.setClickAction("GUI_ShowScreen('demos')");

authwin = AuthWindow();
glass.GUI_ScreenAddWidget("mainmenu", authwin);
authwin.centerWindow();

optionwin = OptionsWindow();
glass.GUI_ScreenAddWidget("mainmenu", optionwin);
optionwin.setSizePct(.55, .45);
optionwin.centerWindow();
optionwin.setVisible(0);

stats = StatsWindow(cvar_get('username'));
glass.GUI_ScreenAddWidget("mainmenu", stats);
stats.setSizePct(.45, .55);
stats.centerWindow();
stats.setVisible(0);

#create and hide the game error dialog
gameerror = glass.GlassWindow("Game Error")
gameerror.setSizePct(.2, .15)
gameerrormsg = glass.GlassLabel("text here")
gameerrormsg.setId("msg")
gameerrormsg.setSize(500, 40)
gameerror.add(gameerrormsg, 10, 10)
gameerror.setVisible(0)
ok = gblButtonFactory.createInstance("OK")
ok.setClickAction("w=glass.GUI_GetWidget('mainmenu:Game Error');w.setVisible(0);")
gameerror.add(ok, 50, 45);
glass.GUI_ScreenAddWidget("mainmenu", gameerror)
gameerror.centerWindow()

def show_login():
	mainmenu.authwin.setVisible(1);
	mainmenu.authwin.requestModalFocus();

def show_confirmquit():
	quit_msg = [
	  "Confirm making a huge mistake in your life?",
	  "You want to quit? Then thou hast lost an eighth!",
	  "Yeah, get to your WoW-addicts anonymous meeting. Addict.",
	  "Don't quit! Savage makes a great chat client!",
	  "Press Cancel to quit. Psych!",
	  "You've almost reached that achievement, just play a bit longer..."
	];
	msg = M_Randnum() * len(quit_msg)

	win = glass.GUI_GetWindow("mainmenu:Confirm")
	if win != None:
		glass.GUI_GetWidgetTyped('mainmenu:Confirm:message', glass.GlassLabel).setCaption(quit_msg[msg])	
		win.setVisible(1)
		win.requestModalFocus()
		win.setSize(lbl.getWidth()+30, 100)
		return

	win = glass.GlassWindow("Confirm");

	lbl = glass.GlassLabel(quit_msg[msg])
	lbl.setId('message');
	win.add(lbl, 15,30)
	win.setSize(lbl.getWidth()+30, 100)

	ok = gblButtonFactory.createInstance("Quit")
	ok.setClickAction("shutdown();")
	win.add(ok);
	ok.setPositionPct(.5, .5);

	cancel = gblButtonFactory.createInstance("Cancel")
	cancel.setClickAction("w=glass.GUI_GetWindow('mainmenu:Confirm');w.setVisible(0);w.releaseModalFocus()")
	win.add(cancel)
	cancel.setPositionPct(.7, .5);

	glass.GUI_ScreenAddWidget("mainmenu", win);
	win.centerWindow();
	win.requestModalFocus();

def show_gameerror(msg):
	mainmenu.gameerrormsg.setCaption(msg);
	#TODO make me wrap
	#TODO raise the window?
	w = glass.GUI_GetWidget('mainmenu:Game Error');
	w.setVisible(1);
	con_println(msg);

execwindow.newExecWindow("mainmenu");

credits = gblButtonFactory.createInstance("Credits");
credits.setPosition(100,screenHeight-credits.getHeight());
credits.setClickAction("GUI_ShowScreen('credits')");
glass.GUI_ScreenAddWidget( "mainmenu", credits);

gotoTestScreen = gblButtonFactory.createInstance("Test Screen");
gotoTestScreen.setPosition(0,screenHeight-gotoTestScreen.getHeight());
gotoTestScreen.setClickAction("GUI_ShowScreen('guitest')");
#gotoTestScreen.setClickAction("GUI_ShowScreen('endgame')");
#glass.GUI_ScreenAddWidget( "mainmenu", gotoTestScreen);

testmodels = gblButtonFactory.createInstance("Model Test");
testmodels.setPosition(screenWidth-testmodels.getWidth(), screenHeight-testmodels.getHeight());
testmodels.setClickAction("GUI_ShowScreen('modeltest')");
#glass.GUI_ScreenAddWidget("mainmenu", testmodels);

overlay = glass.GlassLabel("");
overlay.setOpaque(1);
overlay.setBackgroundColor(black);
overlay.setSize(screenWidth,screenHeight);
glass.GUI_ScreenAddWidget("mainmenu",overlay);

##Demo Speed Test Window - todo move into its own class
demotracker = DemoTracker();
demo_window = glass.GlassWindow();
demo_window.setCaption("Demo Speed Test Results");

demo_table = GlassTablePlus();
demo_table.setPosition(5,5);
demo_table.makeBlank();

demo_results = glass.GlassLabel();
demo_table.addRow(demo_results);

demo_log = gblButtonFactory.createInstance("Save Log");
demo_log.setTooltip("NB Logs are saved to the .savage folder.")
demo_log.setClickAction("mainmenu.demotracker.writeData()");
demo_repeat = gblButtonFactory.createInstance("Repeat Test");
demo_repeat.setClickAction("mainmenu.demotracker.repeatDemo()");

demo_wrapper = glass.GlassContainer();
demo_wrapper.add(demo_log,0,0);
demo_wrapper.add(demo_repeat, demo_log.getWidth() + 5,0);
demo_wrapper.setWidth(demo_repeat.getX() + demo_repeat.getWidth());
demo_wrapper.setHeight(max(demo_repeat.getHeight(), demo_log.getHeight()));
demo_table.addRow(demo_wrapper);

demo_results.adjustSize();
demo_table.adjustSize();
demo_window.setSize(demo_table.getWidth() + 10,demo_table.getHeight() + 10);

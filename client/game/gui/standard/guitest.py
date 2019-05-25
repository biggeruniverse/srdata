# (c) 2010 savagerebirth.com

from silverback import *;
import glass;

def frame():
	pass;

def onShow():
	pass;

glass.GUI_CreateScreen('guitest');

bg = glass.GlassLabel();
bg.setBackgroundColor(glass.Color(128,128,128));
bg.setOpaque(1);
bg.setSizePct(1,1);
glass.GUI_ScreenAddWidget("guitest", bg);

tomain = glass.GlassButton("Main Menu");
tomain.setPosition(0,screenHeight-tomain.getHeight());
tomain.setClickAction("GUI_ShowScreen('mainmenu')");
glass.GUI_ScreenAddWidget("guitest", tomain);

execwindow.newExecWindow("guitest");

# ##############################
# Start testing stuff from here!

testAlpha = glass.GlassContainer();
testAlpha.setAlpha(20);
testAlpha.setSize(100,100)
textAlpha = glass.GlassLabel("^crespect test");
testAlpha.add(textAlpha);
glass.GUI_ScreenAddWidget("guitest", testAlpha);

progress = glass.GlassProgressDisc();
progress.setPosition(50,50);
progress.setSize(100,100);
progress.setForegroundColor(glass.Color(0,0,255));
progress.setProgress(.47);
glass.GUI_ScreenAddWidget("guitest", progress);
state = glass.GlassLabel();
state.setImage("/models/human/weapons/ranged/icons/regenerate.s2g");
state.setPosition(75,75);
state.setSize(50,50);
glass.GUI_ScreenAddWidget("guitest", state);

table = GlassTablePlus();
table.addRow("Hello!", "Here is another Cell", "I want to be BLUE");
table.addRow("Hello!", "Here is another Cell", "I want to be RED");
table.addRow("Hello!", "Here is another Cell", "I want to be GREEN");
table.addRow("Hello!", "Here is another Cell", "I want to be YELLOW");

table.adjustSizeToPct(0.5, 0.5);
table.setPositionPct(0.25,0.25);

table.setOpaque(1);
table.setAlternate(0);
table.setFrame(0);

table.rows[0].setBackgroundColor(tangoPurpleDark);

table.getCell(0,2).setBackgroundColor(tangoBlueDark);
table.getCell(1,2).setBackgroundColor(tangoRedDark);
table.getCell(2,2).setBackgroundColor(tangoGreenDark);
table.getCell(3,2).setBackgroundColor(tangoYellowDark);

table.setBackgroundColor(tangoOrangeDark);

glass.GUI_ScreenAddWidget("guitest", table);

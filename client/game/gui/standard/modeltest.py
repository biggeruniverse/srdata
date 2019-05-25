# (c) 2010 savagerebirth.com
from silverback import *;
import glass;

def frame():
	pass;

def onShow():
	pass;

glass.GUI_CreateScreen('modeltest');

class ModelChangeHandler:
	def onValueChanged(self, e):
		modeltest.modelviewer.setModel(modeltest.modeldropmenu.getSelectedValue())

class AnimChangeHandler:
	def onValueChanged(self, e):
		modeltest.modelviewer.setAnimation(modeltest.animdropmenu.getSelectedValue())

bg = glass.GlassLabel();
bg.setBackgroundColor(glass.Color(0,0,0,255));
bg.setSizePct(1,1);
bg.setPosition(0,0);
glass.GUI_ScreenAddWidget("modeltest", bg);

modelviewer = glass.GlassViewer();
modelviewer.setModel("/models/null.model")
modelviewer.setCameraPosition(0,10,10)
modelviewer.setCameraTarget(0,0,10)
modelviewer.setPosition(0, 0);
modelviewer.setSizePct(1,1);
glass.GUI_ScreenAddWidget("modeltest", modelviewer);

modeldropmenu = glass.GlassDropMenu();
modeldropmenu.setPositionPct(0.2, 0);
modeldropmenu.linkCvar("gui_modelviewermodel");
modeldropmenu.addSelectionListener(ModelChangeHandler());
glass.GUI_ScreenAddWidget("modeltest", modeldropmenu);

animdropmenu = glass.GlassDropMenu();
animdropmenu.setPositionPct(0.2, 0.05);
#animdropmenu.linkCvar("gui_modelviewermodel");
animdropmenu.addSelectionListener(AnimChangeHandler());
glass.GUI_ScreenAddWidget("modeltest", animdropmenu);

modeltomain = glass.GlassButton("Main Menu");
modeltomain.setPosition(0,0);
modeltomain.setClickAction("GUI_ShowScreen('mainmenu')");
glass.GUI_ScreenAddWidget("modeltest", modeltomain);

modellist = File_ListFiles("/models", ".model", 1 );
for model in modellist:
	modeldropmenu.addOption( model, model);
	#need to trim the string that gets displayed

modellist = File_ListFiles("/models", ".s2m", 1 );
for model in modellist:
	modeldropmenu.addOption( model, model);

modeldropmenu.setWidth(screenWidth-modeldropmenu.getX());

#hard-coded animations
animdropmenu.addOption( "none", "");
animdropmenu.addOption( "idle", "idle");
animdropmenu.addOption( "melee_1", "melee_1");
animdropmenu.addOption( "melee_2", "melee_2");
animdropmenu.addOption( "melee_3", "melee_3");
animdropmenu.addOption( "melee_4", "melee_4");
animdropmenu.addOption( "block", "block");
animdropmenu.addOption( "walk_fwd", "walk_fwd");
animdropmenu.addOption( "run_fwd", "run_fwd");
animdropmenu.addOption( "death_generic", "death_generic");
animdropmenu.addOption( "resurrected", "resurrected");

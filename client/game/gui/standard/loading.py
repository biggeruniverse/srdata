# (c) 2010 savagerebirth.com
# this file creates the loading screen
from silverback import *;
import glass;

def frame():
	loading.loadingLabel.setCaption("Loading "+cvar_get("world_name")+"...")
	loading.mapback.setImage(cvar_get("world_overhead"));
	loading.mapback.setSizePct(.5,.6667);

	if len(cvar_get("cl_currentContentDownload")) > 0:
		loading.loadingProgress.setVisible(True);
		loading.loadingProgress.setProgress(cvar_getvalue("cl_currentContentDownloadProgress"));
	else:
		loading.loadingProgress.setVisible(False);

def onShow():
	loading.mapback.setImage(cvar_get("world_overhead"));
	loading.mapback.setPositionPct(.25,.16667)
	loading.mapback.setSizePct(.5,.6667)
	loading.loadingbk.setPositionPct(.25,.16667)
	loading.loadingLabel.setCaption("Loading "+cvar_get("world_name")+"...")
	loading.loadingLabel.setPositionPct(.4, .69)
	loading.loadingbk.setSizePct(.5,.6667);
	loading.loadingProgress.setPositionPct(.3, .72)

glass.GUI_CreateScreen('loading')

loadingbk = glass.GlassLabel()
loadingbk.setImage('/gui/standard/black.s2g')
glass.GUI_ScreenAddWidget('loading', loadingbk)
loadingbk.setSizePct(1,1)

mapback = glass.GlassLabel()
mapback.setId('mapback')
glass.GUI_ScreenAddWidget('loading', mapback)

loadingbk = glass.GlassLabel()
loadingbk.setImage('/textures/loading/nfm_mapoverlay.s2g')
#uncomment this when a solution is found to resolution not being set when 
#these scripts are run
#loadingbk.setPosition(int(Vid_GetScreenW()/2.0-256),int(Vid_GetScreenH()/2.0-256))
glass.GUI_ScreenAddWidget('loading', loadingbk)

loadingLabel = glass.GlassLabel("Loading xxxxxxxxxxxxxxxxxxxxxxxxx")
loadingLabel.setForegroundColor(glass.Color(59,45,25))
glass.GUI_ScreenAddWidget('loading', loadingLabel)

loadingProgress = glass.GlassProgressBar();
loadingProgress.setForegroundColor(glass.Color(59,45,25));
glass.GUI_ScreenAddWidget('loading', loadingProgress);
loadingProgress.setSizePct(.3, .1);
loadingProgress.setHeight(30);

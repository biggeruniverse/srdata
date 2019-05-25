# (c) 2010 savagerebirth.com

from silverback import *
import glass;

def show_demoselect():
	w = glass.GUI_GetWidget('mainmenu:Demos');
	if w != None:
		w.setVisible(1)
		return
	window = glass.GlassWindow('Demos');
	window.setTitleVisible(0);
	window.setSizePct(.7, .4);
	window.centerWindow();

	demos = File_ListFiles("/demos/", "*.demo", 0);
	demoList = glass.GlassListBox();
	demoList.setSizePct(200,200);

	for f in demos:
		demoList.addItem(f[7:]);
	demoScroll = glass.GlassScrollArea(demoList);
	window.add(demoScroll);
	demoScroll.setPositionPct(.01, .03);
	demoScroll.setSizePct(.5, .9);
	demoScroll.setId('list');

	demoPlay = glass.GlassButton("Play Demo");
	demoPlay.setClickAction('thelist = glass.GUI_GetWidgetTyped("mainmenu:Demos:list", glass.GlassScrollArea).getContent(glass.GlassListBox);demo=thelist.getItem(thelist.getSelected());Demo_Play(demo[:demo.rfind(".")]);');
	window.add(demoPlay);
	demoPlay.setPositionPct(.6, .85);

	demoClose = glass.GlassButton("Close");
	demoClose.setClickAction("glass.GUI_GetWidget('mainmenu:Demos').setVisible(0);");
	window.add(demoClose);
	demoClose.setPositionPct(.8, .85);

	glass.GUI_ScreenAddWidget("mainmenu", window);

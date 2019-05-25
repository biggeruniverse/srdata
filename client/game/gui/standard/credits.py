# (c) 2011 savagerebirth.com
import glass;

def frame():
	credits.scroll();

def onShow():
	credits.scroller = glass.GUI_GetWidget("credits:scroller");
	#credits.scroller.setPosition(screenWidth/2-credits.scroller.getWidth()/2, min(768, screenHeight)-200);
	credits.scroller.setPosition(screenWidth/2-credits.scroller.getWidth()/2, 0);

def scroll():
	credits.scroller.setY(credits.scroller.getY()-1);

scroller = None;

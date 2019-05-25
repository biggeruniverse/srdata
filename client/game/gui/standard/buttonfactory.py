#(c) 2011 savagerebirth.com

class ButtonFactory:
	def __init__(self):
		self.border = 0;
		self.bgcolor = glass.Color(255,255,255);

	def createInstance(self, cap="", img=None):
		if img is None:
			w = glass.GlassNinePatchButton(cap);
		else: w = glass.ImageButton(cap, img);
		w.setForegroundColor(themeGold);
		return w;


gblButtonFactory = ButtonFactory();

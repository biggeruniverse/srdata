#(c) 2011 savagerebirth.com

class WindowFactory:
	def __init__(self):
		self.border = 0;
		self.bgcolor = glass.Color(0,0,0,128);

	def createInstance(self):
		w = glass.GlassWindow();
		w.setBorderSize(self.border);
		w.setTitleVisible(0);
		w.setBackgroundColor(self.bgcolor);
		return w;

	def initInstance(self, w):
		glass.GlassWindow.__init__(w);
		w.setBorderSize(self.border);
		w.setTitleVisible(0);
		w.setBackgroundColor(self.bgcolor);
		return w;
		
gblWindowFactory = WindowFactory();

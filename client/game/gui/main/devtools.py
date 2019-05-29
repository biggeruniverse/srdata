
from silverback import *;

class DevTools(DefaultWindow):
	
	def __init__(self):
		DefaultWindow.__init__(self);
		
		self.setBackgroundColor(glass.Color(24, 14, 14));
		self.setOpaque(True);
		self.setSize(265, 250);
		
		restart = DefaultButton("RESTART");
		restart.setClickAction("shutdown(1)");
		self.add(restart, "center", 10);
		
		execButton = DefaultButton("PYTHON EXECUTOR");
		execButton.setClickAction("execwindow.showAllWindows();");
		self.add(execButton, "center", 70);
		
		screenLabel = DefaultLabel("Show Screen:");
		self.add(screenLabel, 10, 130);
		
		self.showScreen = DefaultTextField();
		self.showScreen.setText("loading");
		self.showScreen.setWidth(100);
		self.showScreen.addKeyListener(self);
		self.add(self.showScreen, screenLabel.getWidth() + 15, 130);

		self.testmodels = DefaultButton("Model Test");
		self.testmodels.setClickAction("GUI_ShowScreen('modeltest')");
		self.add(self.testmodels, "center", 160);
		
	def onKeyPress(self, e):
		if e.key == glass.Key.ENTER:
			GUI_ShowScreen(e.widget.getText());
			
	def onKeyReleased(self, e):
		pass;

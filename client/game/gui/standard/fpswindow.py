import savage;
import glass;
from silverback import *;

class FpsWindow(glass.GlassLabel):
	def __init__(self):
		glass.GlassLabel.__init__(self);
		self.setFont(fontSizeSmall);
	#cl_showfps: 0 don't show anything, 1 show instant fps, 2 show average fps, 3 show both
	#cl_showfpsserver: 0 don't show it, 1 do
	#cl_showping: 0 don't show it, 1 do
	def update(self):
		if cvar_getvalue("cl_showfps") == 0 and cvar_getvalue("cl_showping") == 0:
			self.setVisible(0);
			return;
		self.setVisible(1);
		name = "";
		cl_showfps = cvar_getvalue("cl_showfps");
		if cl_showfps in (1,3):
			name += "Instant:  " + str(round(cvar_getvalue("cl_fpsClient"))) + "\n";
		if cl_showfps in (2,3):
			name += "Average: " + str(round( cvar_getvalue("cl_fpsClientAvg"))) + "\n";
		if cvar_getvalue("cl_showfpsserver") == 1:
			name += "Server:  " + str(round( cvar_getvalue("cl_fpsServer"))) + "\n";
		if cvar_getvalue("cl_showping") == 1:
			name += "Ping:    " + str(savage.getLocalPlayer().getPing()) + " \n";

		self.setCaption(name);
		self.adjustSize();

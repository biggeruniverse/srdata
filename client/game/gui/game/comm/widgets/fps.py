
from silverback import *;
import glass;
import savage;

class CommFPS(DefaultContainer):    
	def __init__(self):  
		DefaultContainer.__init__(self);
		#self.setFrameStyle("Shadow");  
		self.setBackgroundColor( glass.Color(0,0,0,128));
		self.setSize(120, 20);
		
		self.label = DefaultLabel();
		self.label.setFont(fontSizeSmall);
		self.add(self.label, 5, 3);
		
		self.alwaysUpdate = True;
		
	#cl_showfps: 0 don't show anything, 1 show instant fps, 2 show average fps, 3 show both
	#cl_showfpsserver: 0 don't show it, 1 do
	#cl_showping: 0 don't show it, 1 do
	def frame(self):
		
		instantStr = "Instant:  " + str(round(cvar_getvalue("cl_fpsClient"))) + "\n";
		averageStr = "Average: " + str(round( cvar_getvalue("cl_fpsClientAvg"))) + "\n";
		serverStr = "Server:  " + str(round( cvar_getvalue("cl_fpsServer"))) + "\n";
		pingStr = "Ping:    " + str(savage.getLocalPlayer().getPing()) + " \n";
		
		out = "";
		
		clientFps = cvar_getvalue("cl_showfps");
		if clientFps in (1,3):
			out += instantStr;
			
		if clientFps in (2,3):
			out += averageStr;
		
		#Big: because it's not anyway, it's just the network send rate		
		#if cvar_getvalue("cl_showfpsserver") == 1:
		#	out += serverStr;
			
		if cvar_getvalue("cl_showping") == 1:
			out += pingStr;
			
		if out == "":
			self.setVisible(0);
			return;
		
		self.label.setCaption(out);
		self.label.adjustSize();
		self.setHeight(self.label.getHeight() - 10);
	


#copyright (c) 2011 savagerebirth.com
#this file makes demo_speedTest 1 more useful
import statistics;

class DemoTracker:
	CVARS = (
		#TODO include the map name and demo name
		"vid_fullscreen","vid_currentMode","vid_multisample", 
		"gfx_forceSoftware","gfx_vsync","gfx_radeon","gfx_nvidia","gfx_intel",
		"gfx_clouds","gfx_cloudScale",  "gfx_shadow",
		"gfx_GLSL", "gfx_GLSLQuality", "gfx_GLSLFalloff",
		"gfx_GLSLSceneryProps", "gfx_GLSLSceneryNPCs", "gfx_GLSLTechBuildings", "gfx_GLSLOwnUnit", "gfx_GLSLSceneryNature",
		"gfx_postProcessing","gfx_postBloom","gfx_postWater","gfx_postMotion",
		"gfx_foliage","gfx_foliageFalloff",
		"host_os","host_maxfps","host_date","host_time"
	);
	
	def __init__(self):
		gblEventHandler.addDemoListener(self);
		self.fps = [];
		self.times = [];
		self.frames = [];
		self.lastDemoName = "";
	
	def clear(self):
		self.fps = [];
		self.times = [];
		self.frames = [];
		self.lastDemoName = "";
	
	def repeatDemo(self):
		cvar_setvalue("demo_speedtest",1);
		Demo_Play(self.lastDemoName);
	
	def onEvent(self, e):
		#update the data
		self.parseResult(e);
		
		resultstr = self.getSummary(e);
		mainmenu.demo_results.setCaption(resultstr);
		mainmenu.demo_results.adjustSize();
		mainmenu.demo_table.adjustSize();
		mainmenu.demo_window.setSize(demo_table.getWidth() + 10,demo_table.getHeight() + 10);
		
		screen = glass.GUI_GetScreen("mainmenu");
		screen.moveToTop(mainmenu.demo_window);
		
		#TODO do the same for game errors?
		mainmenu.demo_window.centerWindow();
		mainmenu.demo_window.setVisible(1);
		
		
	def parseResult(self, e):
		demoname = "" #e.name or something
		if demoname != self.lastDemoName:
			self.clear();
			self.lastDemoName = demoname;
		self.fps.append(e.fps);
		self.times.append(e.time);
		self.frames.append(e.frames);
		
	def getData(self):
		string = "Raw Results:"
		for value in self.fps:
			string += " " + str(value);
		string += "\r\n";
		return string;
	
	def getSummary(self, e=None):
		string = "";
		#string = "Demo: " +self.lastDemoName +" Map: " + Demo_GetWorld(self.lastDemoName) +"\r\n"; #TODO
		if e != None:
			string += "Test number: "+str(len(self.fps))            +"\r\n";
			string += "FPS: "        +str(e.fps)                    +"\r\n"; 
			string += "Frames Drew: "+str(e.frames)                 +"\r\n";
			string += "Run Time: "   +str(e.time)                   +"\r\n";
			
		string += "Number of tests: "+str(len(self.fps))            +"\r\n";
		string += "Average FPS: "    +str(statistics.mean(self.fps))+"\r\n";
		string += "Std Dev FPS: "    +str(statistics.sd(self.fps))  +"\r\n";
		return string;
	
	def writeData(self, filepath=""):
		i = 0;
		while not File_Exists(filepath):
			filepath= "demospeedtest%04d.log" % i;
			i += 1;
		File_Open(path,"w");
		
		File_Write(self.getSummary());
		File_Write(self.getData());
		
		File_Write("At the time of log creation, the following cvars had the values:\r\n")
		for key in self.CVARS:
			value = cvar_get(key);
			File_Write(key+" : "+value+"\r\n")
		File_Close(path);

# (c) 2011 savagerebirth.com
#
# This file generates the motd ticker
	
class MotdWindow(glass.GlassContainer):
	def __init__(self):
		glass.GlassContainer.__init__(self);
		self.setBackgroundColor(glass.Color(0,0,0,128));		
		self.setSizePct( 0.6 , 0.05);
		self.setPositionPct(0.2,0.025);
		self.receivedMotd = False;
		self.padding = int(self.getWidth() * 0.2);
		self.rate = 3;
		self.stopTime = 0;		
		self.httpHandle = -1;
		
		self.message = glass.GlassLabel("Loading message of the day...");
		self.add(self.message);
		self.message.setSizePct(1,1);
		self.message.setPositionPct(0,0);
		self.message.addMouseListener(self);
		
		self.message2 = glass.GlassLabel("");
		self.add(self.message2);
		self.message2.setSizePct(1,1);
		self.message2.addMouseListener(self);
		
		
		gblEventHandler.addHttpListener(self);
		
	def getMotd(self):
		self.httpHandle = HTTP_Get("http://savagerebirth.com/updates/motd.txt");
		
		
	def moveLabel(self):				
		if Host_Milliseconds() > self.stopTime + 1000:
			self.rate = 3;
		if self.receivedMotd: 
			if self.message.getX() + self.message.getWidth() < 0:            
				self.message.setX(self.padding);			
			self.message.setX( self.message.getX() - self.rate );
			self.message2.setX( self.message.getX() + self.message.getWidth() + self.padding);
		
	def onMouseMotion(self, e):
		self.stopTime = Host_Milliseconds();
		self.rate = 0;		
	
	def onEvent(self, e):
		if e.handle == self.httpHandle:			
			self.httpHandle = -1;
			msg = e.responseMessage.replace("\n", " ");
			self.message.setCaption(msg);
			self.message.adjustSize();
			self.message2.setCaption(msg);
			self.message2.adjustSize();
			self.message2.setPosition(int(self.message2.getWidth() + self.padding),0);			
			self.receivedMotd = True;

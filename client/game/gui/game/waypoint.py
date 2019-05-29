# (c) 2012 savagerebirth.com

import savage;
import glass;

class Waypoint(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);

		self.label = DefaultLabel();
		self.dist = DefaultLabel();
		self.waypointObject = None;

		self.add(self.label);
		self.add(self.dist, 0, 48);
		self.setSize(48, 68);

	def setObject(self, obj):
		self.waypointObject = obj;

	def setImage(self, img):
		self.label.setImage(img);
		self.label.setSize(48,48);

	def showDistance(self, s):
		if s == True:
			self.dist.setVisible(True);
		else:
			self.dist.setVisible(False);

	def update(self):
		x,y = 0,0;
		d = 0;

		if self.isVisible() == False:
			return;

		if self.waypointObject == None:
			x,y = CL_GetWaypointPosition(0);
		else:
			x,y = savage.go_getscreenposition(self.waypointObject.objectId);

		if x > screenWidth:
			self.setPosition(int(screenWidth-self.getWidth()), int(y-58));
		elif x<0:
			self.setPosition(0, int(y-58));
		else:
			self.setPosition(int(x-24), int(y-58));
		self.dist.setCaption(str(int(savage.getLocalPlayer().getWaypointDistance()/16))+"m");
		self.dist.setX(24-self.dist.getWidth()//2);

	def onEvent(self, e):
		if isinstance(e, WaypointEvent):
			if e.eventType == 'waypoint_complete' or e.eventType == 'waypoint_cancel' or e.eventType == 'waypoint_destroy':
				self.setVisible(False);
			else:
				self.label.setImage(CL_GetWaypointImage(0));
				self.label.setSize(48,48);
				self.setVisible(True);
				if e.targetId != -1:
					self.waypointObject = savage.getGameObject(e.targetId);
				else:
					self.waypointObject = None;

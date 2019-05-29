#copyright (c) 2011 savagerebirth.com
#this file creates the crosshair, and the associated name label

from silverback import *;
import glass;
import savage;
from vectors import Vec3;
import math;

class HUDCrossHair (DefaultTable):
	barWidthPct = 0.095;
	STATUS_INACTIVE = 0;
	STATUS_ACTIVE = 1;
	alphaStep = 40;
	
	def __init__( self ):
		DefaultTable.__init__(self);
		self.horizontalJustification = glass.Graphics.CENTER
		
		self.status = self.STATUS_INACTIVE;
		self._alpha = 1;
		self.lastObject = None;
		self.makeBlank();
		self.setCellPadding(0);
		
		barWidth = int(screenHeight * self.barWidthPct)
		barHeight = barWidth // 8;
		
		self.teamNum = glass.GlassLabel(" Team 0 ");
		self.addRow(self.teamNum);
		
		self.targetName = glass.GlassLabel("LOOKIHAVEARidiculouslyLongName");
		self.targetName.setAlignment(glass.Graphics.CENTER);
		self.addRow(self.targetName);
		
		self.health = glass.GlassProgressBar();
		self.health.setSize(barWidth, barHeight);
		self.health.setBackgroundColor( glass.Color(133,11,10) );
		self.health.setForegroundColor( glass.Color(255,21,22) );
		
		self.addRow(self.health);
		
		self.build = glass.GlassProgressBar();
		self.build.setSize(barWidth, barHeight);
		self.build.setOpaque(True);
		self.build.setBackgroundColor( glass.Color(10,115,110) );
		self.build.setForegroundColor( glass.Color(20,255,248) );
		self.build.setVisible(False);
		
		self.addRow(self.build);
		
		self.crosshair = glass.GlassLabel();
		self.crosshair.setImage("/gui/standard/crosshair.png");
		self.crosshair.setOpaque(False);
		
		self.crosshair_row = self.addRow(self.crosshair);
		
		self.alphaWidgets = [ self.teamNum, self.targetName, self.health, self.build ];
		self.reposition();

	def reposition( self ):
		#ASSUMPTION
		#xhair is horizontally centred in the table and is the bottom-most item in the table
		self.adjustSize();
		self.adjustJustification();
		
		mouseX, mouseY = Input_GetMouseXY();
		
		self.setX( mouseX - self.getWidth()//2);
		self.setY( mouseY - self.getHeight() + self.crosshair_row.getHeight() - self.crosshair.getHeight()//2);
	
	def update(self):
		#0. don't show if we're free
		if getMouseMode() == MOUSE_FREE:
			self.setVisible(False);
		else:
			self.setVisible(True);

		player = savage.getLocalPlayer();
		#1. get the object behind the crosshair
		obj = savage.getObjectUnder(  *Input_GetMouseXY() );
		#2. if we're not pointing at anything, hide!
		if obj == None:
			self.status = self.STATUS_INACTIVE;
			self.adjustAlpha();
			self.reposition();
			return;
		#3. else, get ready to do something
		self.status = self.STATUS_ACTIVE;
		self.lastObject = obj;
		obj_type = obj.getType();
		name = "";
		showHealth = False;
		showBuild = False;
		#4. if it's a unit (includes players and vehicles and NPCS)
		if obj_type.isUnitType():
			name = obj.getNameColorCode() + obj.getName();
			if obj.isPlayer():
				name = "^w" + obj.getClanIcon() + name;
			if obj_type.getValue("tier") == 5 or obj.getTeam() == player.getTeam() or player.getTeam() == 0:
				#second level of siege, or our team (or NPC)
				showHealth = True;
			
		#5. if it's a building
		elif obj_type.isBuildingType():
			name = obj.getNameColorCode()  + obj_type.getValue("description");
			showHealth = True;
			showBuild = obj.isBeingBuilt();
		#6. Anything else
		else:
			name = obj.getName();
		
		if ( cvar_getvalue("sv_numTeams") > 3 or player.getTeam() == 0) and obj.getTeam() != 0:
			self.teamNum.setCaption("Team " + str(obj.getTeam()));
		else:
			self.teamNum.setCaption("");
		
		self.targetName.setCaption(name);
		
		self.updateHealth( showHealth, obj);
		self.updateBuild( showBuild, obj);
		
		self.adjustAlpha();
		self.reposition();
		
	def reset( self):
		self.reposition();
		self.setAlpha(0);
		self.status = self.STATUS_INACTIVE;
	
	def updateHealth( self, showHealth, obj):
		if showHealth:
			self.health.setVisible(True);
			self.health.setProgress( obj.getHealthPct() );
		else:
			self.health.setVisible(False);
	
	def updateBuild( self, showBuild, obj):
		if showBuild:
			self.build.setVisible(True);
			self.build.setProgress( obj.getBuildProgress());
		else:
			self.build.setVisible(False);
			
	def adjustAlpha( self):
		if self.status == self.STATUS_ACTIVE and self.getAlpha() < 255:
			self.setAlpha (self.getAlpha() + self.alphaStep);
		elif self.status == self.STATUS_INACTIVE and self.getAlpha() > 0:
			self.setAlpha (self.getAlpha() - self.alphaStep);
	
	def setAlpha(self, alpha):
		if alpha > 255: alpha = 255;
		if alpha < 0: alpha = 0;
		
		self._alpha = alpha;
	
		for widget in self.alphaWidgets:
			fgc = widget.getForegroundColor();
			fgc.a = self._alpha;
			widget.setForegroundColor( fgc );
			bgc = widget.getBackgroundColor();
			bgc.a = self._alpha;
			widget.setBackgroundColor( bgc );
			#add base color here too, if needed
		
	def getAlpha(self):
		return self._alpha;

	def getLastObject(self):
		if self.lastObject is None:
			return -1;
		return self.lastObject.objectId;

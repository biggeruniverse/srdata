# copyright 2011 savagerebirth.com
# this class represents a compass widget used in the HUD

# possible TODO for vectors module
# x.bearing() returns the bearing in degrees

from silverback import *;
import savage; #add me to ui_game.cfg
import glass;
import math;
from vectors import Vec3;

class HUDCompass( glass.GlassContainer ):
	DISPLAY_ANGLE = 100;
	damping = 0.35;
	
	def __init__(self):
		self.lastbearing = 0
		self.lastdisplay = 0
		
		glass.GlassContainer.__init__(self);
		
		self.label1 = glass.GlassLabel();
		self.label1.setImage( "/gui/standard/compass.s2g" );
		self.add(self.label1,0,0);
		
		self.imagewidth = self.label1.getWidth();
		
		self.label2 = glass.GlassLabel();
		self.label2.setImage( "/gui/standard/compass.s2g" );
		self.add(self.label2,self.imagewidth,0);
		
		self.setSize( int(self.DISPLAY_ANGLE * self.imagewidth / 360) , self.label1.getHeight() );
		self.displaywidth = self.getWidth();
		#assumption: we have an image 360 pixels wide
		#the nth pixel corresponds to a bearing of n degrees
		#TODO account for images of any width (e.g. 512 in an s2g)
		self.update();
	
	def rotateTo(self, bearing):
		self.label1.setX( int( (self.DISPLAY_ANGLE/2 - bearing )*self.imagewidth/360 ) );
		if self.label1.getX() > 0:
			self.label2.setX( self.label1.getX() - self.imagewidth );
		else:
			self.label2.setX( self.label1.getX() + self.imagewidth );
	
	def update(self):
		player = savage.getLocalPlayer();
		#1. obtain the forward vector
		f = Vec3(player.getForwardVector());
		
		#2. calculate the bearing using maths
		#since we're measuring from the north, f(theta) = (sin theta, cos theta)
		#so tan theta = f_x/f_y, therefore...
		
		bearing = f.getBearing();
		x = self.lastbearing - self.lastdisplay;
		if x > 180:
			x -= 360;
		elif x < -180:
			x += 360;
		displayAngle = self.lastdisplay + self.damping*( x );
		#exponential decay of sorts
		displayAngle %= 360;

		self.rotateTo(displayAngle);
		self.lastbearing = bearing;
		self.lastdisplay = displayAngle;


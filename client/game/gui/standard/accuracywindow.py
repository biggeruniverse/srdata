# copyright (c) 2011 savagerebirth.com

import glass;
import savage;
from silverback import *;

class AccuracyWindow( glass.GlassWindow ):
	def __init__ ( self ):
		glass.GlassWindow.__init__(self);
		self.setCaption( "Weapon Accuracy" );
		self.setFocusable(False);
		
		self.table = GlassTablePlus();
		self.add( self.table , 0 , 0);
		self.table.setBackgroundColor(transparency);
		self.table.setAlternate(False);
		self.table.autoAdjust = False;
		self.table.setCellPadding(0);
	
	def update( self ):
		self.table.erase();
		player = savage.getLocalPlayer();
		shots, hits, siege = player.getAccuracy();
		weapons = [w for w in shots if shots[w] > 0];
		
		self.addRow("Weapon","Shots","Hit%","Siege%");
		
		for w in sorted(weapons):
			weapon_shots = shots[w];
			if weapon_shots != 0:
				weapon_hit   = 100*hits[w] /weapon_shots;
				weapon_siege = 100*siege[w]/weapon_shots;
			self.addRow("Weapon", str(weapon_shots), str(weapon_hit), str(weapon_siege));
		
		weapon_shots = sum(shots.values());
		if weapon_shots != 0:
			weapon_hit   = 100*sum(hits.values() )/weapon_shots;
			weapon_siege = 100*sum(siege.values())/weapon_shots;
		else:
			weapon_hit = weapon_siege = 0;
		
		self.addRow("Total" ,str(weapon_shots), str(weapon_hit), str(weapon_siege));
		
		self.table.adjustSize();
		self.setSize(self.table.getWidth() + 2, self.table.getHeight() + 2 + self.getTitleBarHeight());
	
	def addRow(self, *labels):
		labels = [glass.GlassLabel(s) for s in labels];
		for l in labels:
			l.setFont(fontSizeSmall);
		self.table.addRow(*labels);

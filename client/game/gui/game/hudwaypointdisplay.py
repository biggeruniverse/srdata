#copyright (c) 2010 savagerebirth.com
#this class handles the waypoints shown onscreen

class HUDWaypointDisplay( glass.GlassContainer, EventListener ):
	def __init__( self ):
		glass.GlassContainer.__init__(self);
		
		global gblEventHandler;
		#gblEventHandler.addWaypointListener(self);
		
	def onEvent( self, e):
		pass;
		"""
		1. play the appropriate sound if neccesary
		2. show an icon on the hud as appropriate
		3. show a green or red target icon on the hud as appropriate
		4. call update() if needed
		5. set some variable to indicate that update() should be called each frame
		"""
	
	def update( self):
		#called every frame
		pass;
		"""
		if we're handling a waypoint event:
			1. use pythagoras to find the distance to the waypoint, and update the appropriate label
			2. use maths to determine if we should move left or right
			3. use maths, or some magic python function, to position the waypoint icons on the hud
		else:
			hide everything
			set some variable to indicate that update() should NOT be called each frame
		"""

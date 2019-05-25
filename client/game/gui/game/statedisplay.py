# copyright (c) savagerebirth.com 2010
# this class displays the state icons, indicating what status affect the player
import glass;
import savage;

class StateDisplay( glass.GlassContainer):
	def __init__(self):
		glass.GlassContainer.__init__(self);
		self.setOpaque(0);
		
		self.setSizePct(0.4, 0.06);
		
		self.timers = [];
		self.counters = [];
		self.progresses = [];
		self.newState();
	
	def newState( self):
		progress = glass.GlassProgressDisc();
		progress.setProgress(1);
		progress.setSize( screenWidthPct(0.045), screenWidthPct(0.045));

		self.progresses.append(progress);

		#timer = glass.GlassTimer();
		timer = glass.GlassLabel();
		timer.setSize( int( 0.033 * screenHeight) , int( 0.033 * screenHeight) );
		timer.setX( len(self.timers) * (timer.getWidth()+5));
		timer.setY( self.getHeight() - timer.getHeight() );

		progress.setX((timer.getX()+timer.getWidth()/2)-progress.getWidth()/2);
		progress.setY((timer.getY()+timer.getHeight()/2)-progress.getHeight()/2);
		
		#timer.setFrameSize(1);
		#timer.setForegroundColor( glass.Color(20,20,20) );
		
		self.add(timer);
		self.timers.append(timer);

		self.add(progress);
		
		counter = glass.GlassLabel("999");
		counter.setAlignment(glass.Graphics.RIGHT);
		counter.setY(0);
		
		self.add( counter);
		self.counters.append(counter);

	def update( self ):
		player = savage.getLocalPlayer();
		stateList = player.getStateList();
		stateCount = len( stateList);
		timerCount = len( self.timers);
		#first, ensure that we have enough 'state slots'
		for j in range( stateCount - timerCount ):
			self.newState();
		
		widthToUse = (self.timers[0].getWidth() + 5)*stateCount;
		#xOffset = (self.getWidth() - widthToUse )// 2;
		xOffset = 0;
		
		for i in range( stateCount ):
			state = stateList[i];
			timer = self.timers[i];
			counter = self.counters[i];
			progress = self.progresses[i];
			
			w = timer.getWidth();
			h = timer.getHeight();
			timer.setImage(state.getIcon());
			progress.setImage(state.getIcon());
			timer.setSize( w , h);
			progress.setSize( w , h);
			timer.setVisible(1);
			#timer.update(); #or whatever will update the GlassTimer
			timer.setX( xOffset + i*(timer.getWidth() + 5));
			inflictor = state.getInflictor();
			
			if inflictor == None or inflictor.getTeam() == player.getTeam():
				progress.setForegroundColor( tangoBlue );
			else:
				progress.setForegroundColor( tangoRed );

			counter.setVisible(1);
			counter.setCaption( state.getTimeRemaining() );
			counter.setX( timer.getX() + timer.getWidth() - counter.getWidth() );

			progress.setVisible(1);
			try:
				progress.setProgress(1.0-state.getTimeRemaining(False)/state.getDuration());
			except ZeroDivisionError:
				progress.setProgress(1.0)
			progress.setX((timer.getX()+timer.getWidth()/2)-progress.getWidth()/2);
			progress.setY((timer.getY()+timer.getHeight()/2)-progress.getHeight()/2);
			
		for i in range( stateCount , timerCount):
			timer = self.timers[i];
			counter = self.counters[i];
			progress = self.progresses[i];
			timer.setVisible(0);
			counter.setVisible(0);
			progress.setVisible(0);



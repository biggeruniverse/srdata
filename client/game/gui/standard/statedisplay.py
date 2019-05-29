# copyright (c) savagerebirth.com 2010
# this class displays the state icons, indicating what status affect the player
import glass;
import savage;

class StateDisplay( glass.GlassContainer):
	def __init__(self):
		glass.GlassContainer.__init__(self);
		self.setOpaque(0);
		
		self.setSizePct(0.4, 0.05);
		
		self.timers = [];
		self.counters = [];
		self.progresses = [];
		self.newState();
	
	def newState( self):
		progress = glass.GlassProgressDisc();
		progress.setProgress(1);
		progress.setSize( int(0.06 * screenHeight), int(0.06 * screenHeight));
		progress.setX(len(self.progresses) * progress.getWidth());
		progress.setY(self.getHeight() - progress.getHeight());

		self.add(progress);
		self.progresses.append(progress);

		#timer = glass.GlassTimer();
		timer = glass.GlassLabel();
		timer.setSize( int( 0.033 * screenHeight) , int( 0.033 * screenHeight) );
		timer.setX( len(self.timers) * (timer.getWidth()+5));
		timer.setY( self.getHeight() - timer.getHeight() );
		
		#timer.setFrameSize(1);
		#timer.setBaseColor( tangoGrey3 );
		
		self.add(timer);
		self.timers.append(timer);
		
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
		for j in xrange( stateCount - timerCount ):
			self.newState();
		
		widthToUse = (self.timers[0].getWidth() + 5)*stateCount;
		xOffset = (self.getWidth() - widthToUse )// 2;
		
		for i in xrange( stateCount ):
			state = stateList[i];
			timer = self.timers[i];
			counter = self.counters[i];
			progress = self.progresses[i];
			
			w = timer.getWidth();
			h = timer.getHeight();
			timer.setImage(state.getIcon());
			timer.setSize( w , h);
			timer.setVisible(True);
			#timer.update(); #or whatever will update the GlassTimer
			timer.setX( xOffset + i*(timer.getWidth() + 5));
			inflictor = state.getInflictor();
			
			if inflictor.getTeam() == player.getTeam():
				progress.setForegroundColor( tangoBlue );
			else:
				progress.setForegroundColor( tangoRed );

			counter.setVisible(True);
			counter.setCaption( state.getTimeRemaining() );
			counter.setX( timer.getX() + timer.getWidth() - counter.getWidth() );

			progress.setVisible(True);
			progress.setProgress(state.getTimeRemaining(False)/state.getDuration());
			
			progress.setX( xOffset + i*(timer.getWidth() + 5));
			
		for i in xrange( stateCount , timerCount):
			timer = self.timers[i];
			counter = self.counters[i];
			progress = self.progresses[i];
			timer.setVisible(False);
			counter.setVisible(False);
			progress.setVisible(False);



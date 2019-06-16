# (c) 2010 savagerebirth.com

from silverback import *;
import glass;

class VoteInfoBox( glass.GlassWindow, EventListener ):
	def __init__( self ):
		glass.GlassWindow.__init__(self);
		
		global gblEventHandler;
		gblEventHandler.addVoteListener(self);
		
		self.setOpaque(False);
		self.setSizePct( 0.4, 0.16 );
		self.setBackgroundColor( glass.Color(0,0,0,100) );
		self.setFrameSize(0);
		self.setTitleVisible(False);
		self.setTitleBarHeight(0);
		
		self.description = glass.GlassLabel("");
		self.add(self.description, 0 ,0);
		self.description.setSizePct( 0.5 , 0.4 );
		self.description.setPositionPct( 0.05, 0 );
		self.description.setForegroundColor( tangoYellow );
		
		self.commStats = glass.GlassLabel("");
		self.add(self.commStats);
		self.commStats.setSizePct( 0.5,0.6 );
		self.commStats.setPositionPct( 0.05, 0.4 );
		self.commStats.setForegroundColor( tangoYellow );
		self.commStats.setAlignment(1); #center
		
		self.barBG = glass.GlassLabel("");
		self.add(self.barBG);
		self.barBG.setImage("/gui/standard/vote_barGrey.png");
		self.barBG.setSizePct( 0.5, 0.2);
		self.barBG.setPositionPct( 0.05, 0.6);
		self.barBG.setOpaque(True);
		
		self.barYes = glass.GlassLabel("");
		self.add(self.barYes);
		self.barYes.setImage("/gui/standard/vote_barGreen.png");
		self.barYes.setSizePct( 0, 0.2);
		self.barYes.setPositionPct( 0.05, 0.6);
		self.barYes.setOpaque(True);
		
		self.barNo = glass.GlassLabel("");
		self.add(self.barNo);
		self.barNo.setImage("/gui/standard/vote_barRed.png");
		self.barNo.setSizePct( 0, 0.2);
		self.barNo.setPositionPct( 0.05, 0.6);
		self.barNo.setOpaque(True);
		
		self.barDivider = glass.GlassLabel("");
		self.add(self.barDivider);
		self.barDivider.setSizePct( 0, 0.2);
		self.barDivider.setWidth(1);
		self.barDivider.setPositionPct( 0, 0.6);
		self.barDivider.setBackgroundColor( white );
		self.barDivider.setOpaque(True);
		
		self.labelYes = glass.GlassLabel("F1 for YES");
		self.add(self.labelYes);
		self.labelYes.setForegroundColor( tangoGreenLight );
		self.labelYes.setPositionPct( 0, 0.8);
		self.labelYes.setAlignment(glass.Graphics.RIGHT);
		
		self.labelNo = glass.GlassLabel("F2 for NO");
		self.add(self.labelNo);
		self.labelNo.setPositionPct( 0.7, 0.8);
		self.labelNo.setAlignment(glass.Graphics.RIGHT);
		self.labelNo.setForegroundColor( tangoRedLight );
		
		self.results = glass.GlassLabel("^5750^w/^6110");
		self.add( self.results );
		self.results.setSizePct(0.2,0.2);
		self.results.setPositionPct( 0.4, 0.8);
		
		"""self.timer = glass.GlassTimer("");
		self.add ( self.timer );
		self.timer.setSizePct(0.1, 0.1);
		self.timer.setPositionPct(0.9, 0.65);
		"""
		self.timeLeft = glass.GlassLabel("");
		self.add(self.timeLeft);
		self.timeLeft.setSizePct(0.1, 0.1);
		self.timeLeft.setPositionPct(0.9, 0.65);
		self.timeLeft.setForegroundColor( tangoGrey1 );
		
		self.anotherTeam = glass.GlassLabel("Another team is voting");
		self.add( self.anotherTeam);
		self.anotherTeam.setForegroundColor( tangoGrey1 );
		self.anotherTeam.setSizePct(1,0.2);
		self.anotherTeam.setPositionPct(0,0.8);
		self.anotherTeam.setAlignment(1); #center
		
		self.miniMapImage = glass.GlassLabel("");
		self.add(self.miniMapImage);
		self.miniMapImage.setSize(64,64);
		self.miniMapImage.setPositionPct(0.6,0.1);
		self.miniMapImage.setVisible(False);
		
		self.status = self.INACTIVE;
		self.activeseq = None;
	
	def reset( self ):
		self.hide();	
	#add this to hud.frame()
	def frame( self ):
		if cvar_getvalue("vote_show") == 1:
			self.timeLeft.setCaption(cvar_get("vote_seconds"));
		else:
			self.reset()
	
	def onEvent(self, e):
		if cvar_getvalue("vote_show") == 1:
			
			vote_duration = cvar_get("vote_duration");
			vote_description = cvar_get("vote_description");
			vote_team = cvar_getvalue("vote_team");
			vote_commander = cvar_getvalue("vote_commander");
			player_team = cvar_getvalue("player_team");
			
			if self.status == self.INACTIVE:
				self.status = self.VOTE_IN_PROGRESS;
				Sound_PlaySound("/sound/general/vote.ogg");
				#self.timer.setEnd(vote_duration);
				if self.activeseq != None:
					self.activeseq.stop();
					self.activeseq = None;
				self.activeseq = ActionSequence(SlideAction(self, self.getX(), 40));
			
			#common to all votes are the description, time and sliders
			
			self.description.setCaption( vote_description );
			#the timer is updated in frame() as the event does not appear to fire every frame
			self.updateResults();
			
			if vote_team == 0 or vote_team == player_team: #we can vote
				#'own' votes show F1 F2 count
				self.labelYes.setVisible(True);
				self.labelNo.setVisible(True);
				self.results.setVisible(True);
				self.anotherTeam.setVisible(False);

				
			else: #we can't vote
				#'other' votes show the "other team" label
				self.labelYes.setVisible(False);
				self.labelNo.setVisible(False);
				self.results.setVisible(False);
				self.anotherTeam.setVisible(True);
			if vote_commander == 1:
				self.commStats.setCaption( cvar_get( "vote_commander_stats" ));
				self.commStats.setVisible(True);
			else:
				self.commStats.setVisible(False);
			data = cvar_get("vote_description").split(" ");
			if data[0] == "Load":
				data2 =  data[2].split("\n");
				self.miniMapImage.setImage("world/"+data2[0]+"_overhead.jpg");
				self.miniMapImage.setSize(64,64);
				self.miniMapImage.setVisible(True);

				
		else: #assuming a voteEvent is sent when the vote passes or fails or is cancelled
			self.hide();
	
	def updateResults( self ):
		yesVotes = cvar_getvalue("vote_yes");
		noVotes = cvar_getvalue("vote_no");
		eligibleVoters = cvar_getvalue("vote_population");
		minVotesRequired = cvar_getvalue("vote_min") * eligibleVoters;
		yesProportionRequired = cvar_getvalue("vote_need") * eligibleVoters;
		
		#I have no idea if these cvars are the right way round or not, due to their ambiguous names
		#might need to take the floor, ceil or round these last two
		maxBarLength = self.barBG.getWidth();
		if minVotesRequired != 0:
			lengthOfBar = min( maxBarLength, (yesVotes + noVotes) * maxBarLength / minVotesRequired );
		else:
			#division by zero - vote will automatically pass?
			#if this is ever triggered, this has to be a bug with vote_population, surely
			lengthOfBar = maxBarLength;
		
		if yesVotes + noVotes != 0:
			yesLength = int( yesVotes * lengthOfBar / (yesVotes + noVotes) );
			noLength = int( noVotes * lengthOfBar / (yesVotes + noVotes) );
		else:
			noLength = 0;
			yesLength = 0;
		#when no votes have been cast, yesVotes + noVotes == 0
		#division by zero!
				
		self.barYes.setWidth( yesLength );
		self.barNo.setX( self.barBG.getX() + yesLength );
		self.barNo.setWidth( noLength );
		self.barDivider.setX( int( self.barBG.getX() +  self.barBG.getWidth() * yesProportionRequired ) );
		#again, should we take the floor, ceil or just round here? int() appears to floor
		
		#finally update the vote counter
		self.results.setCaption("^575%d^w/^611%d"%(int(yesVotes), int(noVotes)));
		#the number of yes and no votes are handled as floats, thankfully
	
	def hide( self):
		if self.status != self.INACTIVE:
			if self.activeseq != None:
				self.activeseq.stop();
			self.activeseq = ActionSequence(SlideAction(self, self.getX(), -(self.getHeight()+5)));
		self.status = self.INACTIVE;
		self.labelYes.setCaption("F1 for YES");
		self.labelNo.setCaption("F2 for NO");
		
	def castVote(self, vote ):
		if vote == 'yes':
			self.labelYes.setCaption("YES");
			CL_VoteYes();
		if vote == 'no':
			self.labelNo.setCaption("NO");
			CL_VoteNo();
	
	INACTIVE = 0;
	VOTE_IN_PROGRESS = 1;
	
	ANIMATION_OFF = -1;
	ANIMATION_ON = 0;

#http://www.newerth.com/smf/index.php/topic,11610.0.html
"""
lengthOfBar = min(maxBarLength, ((yesVotes + noVotes) / minimumVotesRequired) * maxBarLength)
greenPieceLength = (yesVotes / (yesVotes + noVotes)) * lengthOfBar
redPieceLength = (noVotes / (yesVotes + noVotes)) * lengthOfBar
winningBarPosition = yesPercentageRequired * maxBarLength
"""


from silverback import *;

import glass;

class VoteSelectionWindow( DefaultWindow ):
	def __init__(self):
		DefaultWindow.__init__(self);
		
		self.setSize(470, 275);
		self.setPositionPct(0.2, 0.25);
		self.setTitleVisible(0);
		self.setTitleBarHeight(0);
		self.setBackgroundColor(glass.Color(0, 0, 0, 180));
		self.setVisible(0); 
		
		self.create();		
		
	def show(self, player = ""):
		self.nameInput.setText(player);
		self.setVisible(1);
		self.mousemode = getMouseMode();
		setMouseMode(MOUSE_FREE);		
	
	def close(self):		
		setMouseMode(self.mousemode);
		self.setVisible(0);
		
	def create(self):
		
		columnX = self.getWidth() // 2 - 30;
		columnY = self.getHeight() - 20;

		playerVotes = DefaultContainer();
		playerVotes.setBackgroundColor(glass.Color(80, 50, 50, 180));
		playerVotes.setSize( columnX, columnY);
		self.add(playerVotes, 10, 10);		

		playerTop = DefaultContainer();
		playerTop.setBackgroundColor(glass.Color(0, 0, 0, 50));
		playerTop.setSize(columnX, 25);
		playerVotes.add(playerTop);
		
		playerLabel = DefaultLabel("Player Votes");
		playerLabel.setFont(fontSizeSmall);
		playerTop.add(playerLabel, 10, 3);
		
		playerName = DefaultLabel("Name");
		playerVotes.add(playerName, 10, 35)
		
		self.nameInput = DefaultTextField();
		self.nameInput.setSize(120, 25);
		playerVotes.add(self.nameInput, 60, 35)
		
		playerID = DefaultLabel("ID");
		playerVotes.add(playerID, 10, 70)
		
		self.idInput = DefaultTextField();
		self.idInput.setSize(120, 25);
		playerVotes.add(self.idInput, 60, 70)
		
		elect = DefaultButton("Elect Player");		
		playerVotes.add(elect, 10, 105)
		elect.setWidth(120);
		elect.addActionListener(self);
		
		mute = DefaultButton("Mute Player");
		playerVotes.add(mute, 10, 140);
		mute.setWidth(120);
		mute.addActionListener(self);
		
		banish = DefaultButton("Banish Player");
		playerVotes.add(banish, 10, 175);
		banish.setWidth(120);
		banish.addActionListener(self);
		
		kick = DefaultButton("Kick Player");
		playerVotes.add(kick, 10, 210);
		kick.setWidth(120);
		kick.addActionListener(self);
		
		gameVotes = DefaultContainer();
		gameVotes.setBackgroundColor(glass.Color(80, 50, 50, 180));
		gameVotes.setSize(columnX, columnY);
		self.add(gameVotes, self.getWidth() // 2 + 5, 10);
		
		gameTop = DefaultContainer();
		gameTop.setBackgroundColor(glass.Color(0, 0, 0, 50));
		gameTop.setSize(columnX, 25);
		gameVotes.add(gameTop);
		
		gameLabel = DefaultLabel("Game Votes");
		gameLabel.setFont(fontSizeSmall);
		gameTop.add(gameLabel, 10, 3);
		
		worldLabel = DefaultLabel("World:");
		gameVotes.add(worldLabel, 10, 35);
		
		self.worldInput = DefaultTextField();
		self.worldInput.setSize(120, 25);
		gameVotes.add(self.worldInput, 70, 35);
		
		world = DefaultButton("Load Map");
		gameVotes.add(world, 10, 70);
		world.setWidth(120);
		world.addActionListener(self);
		
		random = DefaultButton("Random Map");
		gameVotes.add(random, 10, 105);
		random.setWidth(120);
		random.setClickAction("CL_CallVote('randommap')");
		
		time = DefaultButton("Extend Time");
		gameVotes.add(time, 10, 140);
		time.setWidth(120);
		time.setClickAction("CL_CallVote('time '+ "")");
		
		restart = DefaultButton("Restart Match");
		gameVotes.add(restart, 10, 175);
		restart.setWidth(120);
		restart.setClickAction("CL_CallVote('restartmatch')");
		
		pause = DefaultButton("Pause Match");
		gameVotes.add(pause, 10, 210);
		pause.setWidth(120);
		pause.setClickAction("CL_CallVote('pause')");
		
		close = DefaultButton("Close");
		gameVotes.add(close, 10, 210, "right");
		close.addActionListener(self);
		
	def onAction(self, e):
		if e.widget.getCaption() == "Close":
			self.close();
			
		elif e.widget.getCaption() == "Kick Player":
			# TODO: Confirm window
			if len(self.nameInput.getText()) != 0:
				CL_CallVote('kick ' + (self.nameInput.getText()));
				
		elif e.widget.getCaption() == "Mute Player":
			if len(self.nameInput.getText()) != 0:
				CL_CallVote('mute ' + (self.nameInput.getText()));
		
		elif e.widget.getCaption() == "Banish Player":
			if len(self.nameInput.getText()) != 0:
				CL_CallVote('banish ' + (self.nameInput.getText()));
		
		elif e.widget.getCaption() == "Elect Player":
			if len(self.nameInput.getText()) != 0:
				CL_CallVote('elect ' + (self.nameInput.getText()));
			else:
				pass; #TODO: elect self
				
		elif e.widget.getCaption() == "Load Map":
			if len(self.worldInput.getText()) != 0:
				CL_CallVote('world ' + (self.worldInput.getText()));	
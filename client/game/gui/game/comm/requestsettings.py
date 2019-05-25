
class ResearchToggleButton(glass.ImageButton):
	def __init__(self, var):
		glass.ImageButton.__init__(self);
		self.addActionListener(self);
		# Ask what the cvar is and set currentState then:
		self.var = var
		self.states = ["/gui/main/images/canceltr.s2g","/gui/main/images/yestr.s2g","/gui/game/images/promote.s2g"];
		self.setImage(self.states[int(cvar_getvalue(self.var))]);
		self.setSize(32,32);

	def onAction(self, e):
		if e.widget == self:			
			currentState = int(cvar_getvalue(self.var)) + 1 if int(cvar_getvalue(self.var)) < 2 else 0;
			cvar_set(self.var, str(currentState))
			self.setImage(self.states[currentState]);
			self.setSize(32,32);

class RequestSettings(DefaultWindow):

	def __init__(self):
		DefaultWindow.__init__(self);

		self.setSize(200, 136);
		#self.setPosition(270, screenHeight - 210);
		self.setBackgroundColor( transparency );
		#self.setVisible(0);

		self.unitsLabel = DefaultLabel("Units"); 
		self.unitsLabel.setFont(fontSizeSmall);
		self.unitsLabel.setImage("/gui/standard/icons/human/human_savage.s2g");
		self.unitsLabel.setSize(32,32);		
		self.add(self.unitsLabel, 10, 10);

		self.siegeLabel = DefaultLabel("Siege");
		self.siegeLabel.setFont(fontSizeSmall);
		self.siegeLabel.setImage("/gui/standard/icons/human/human_ballista.s2g");
		self.siegeLabel.setSize(32,32);		
		self.add(self.siegeLabel, 10, 52 );

		self.buffsLabel = DefaultLabel("Buffs");
		self.buffsLabel.setFont(fontSizeSmall);
		self.buffsLabel.setImage("/models/beast/items/icons/fireshield.s2g");
		self.buffsLabel.setSize(32,32);		
		self.add(self.buffsLabel, 10, 94);


		self.weaponsLabel = DefaultLabel("Weps");
		self.weaponsLabel.setFont(fontSizeSmall);
		self.weaponsLabel.setImage("/gui/standard/icons/human/human_crossbow.s2g");
		self.weaponsLabel.setSize(32,32);		
		self.add(self.weaponsLabel, 110, 10);

		self.itemsLabel = DefaultLabel("Items");
		self.itemsLabel.setFont(fontSizeSmall);
		self.itemsLabel.setImage("/gui/standard/icons/human/human_ammo_pack.s2g");
		self.itemsLabel.setSize(32,32);		
		self.add(self.itemsLabel, 110, 52);

		self.goldLabel = DefaultLabel("Gold");
		self.goldLabel.setFont(fontSizeSmall);
		self.goldLabel.setImage("/gui/standard/icons/gold/gold_icon.s2g");
		self.goldLabel.setSize(32,32);		
		self.add(self.goldLabel, 110, 94)


		self.unitsButton = ResearchToggleButton("cl_cmdr_aAR_units");	
		self.add(self.unitsButton, 52, 10);

		self.siegeButton = ResearchToggleButton("cl_cmdr_aAR_siege");	
		self.add(self.siegeButton, 52, 52);

		self.buffsButton = ResearchToggleButton("cl_cmdr_aAR_buffs");		
		self.add(self.buffsButton, 52, 94);

		self.weaponsButton = ResearchToggleButton("cl_cmdr_aAR_weapons");	
		self.add(self.weaponsButton, 152, 10);

		self.itemsButton = ResearchToggleButton("cl_cmdr_aAR_items");	
		self.add(self.itemsButton, 152, 52);

		self.goldButton = ResearchToggleButton("cl_cmdr_aAR_money");	
		self.add(self.goldButton, 152, 94);

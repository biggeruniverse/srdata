# Copyright (c) 2011 savagerebirth.com 
# this file creates the lobby

from silverback import *;
import glass;
import savage;

def frame():
	lobby.update();

def onShow():
	lobby.arrange();

glass.GUI_CreateScreen('lobby');

bg = glass.GlassLabel(" ");
bg.setBackgroundColor(black);
bg.setOpaque(1);
bg.setSizePct(1,1);
bg.setPositionPct(0,0);
glass.GUI_ScreenAddWidget("lobby", bg);

boxWidth = 0.2;
boxHeight = 0.5;
buttonHeight = boxHeight / 10;
totalPadding = 0.05;
paddingPerBox = totalPadding / 8;
centralPadding = 0.15;

interface = glass.GlassContainer();
interface.setBackgroundColor( tangoGrey2 );
interface.setSizePct( 2 * boxWidth, 0.2);
interface.setPositionPct((0.5 - boxWidth), ( 1 - 0.2));
glass.GUI_ScreenAddWidget("lobby", interface);

interfaceMainMenu = glass.GlassButton(" << MAIN MENU");        
interfaceMainMenu.setClickAction("GUI_ShowScreen('mainmenu');");
interface.add( interfaceMainMenu );
interfaceMainMenu.setSizePct(0.5,0.2);
interfaceMainMenu.setPositionPct(0,0);

interfaceSpectatorButton = glass.GlassButton(" Join Spectators ");
interface.add( interfaceSpectatorButton );
interfaceSpectatorButton.setClickAction("CL_RequestTeam(0);CL_RequestLoadout();");
interfaceSpectatorButton.setSizePct(0.5,0.2);
interfaceSpectatorButton.setPositionPct(0.5,0);

interfaceChatBox = HUDChatBox();
interfaceChatBox.alwaysShowInput(1);
interfaceChatBox.inputType.setVisible(False);
interface.add( interfaceChatBox );
interfaceChatBox.setSizePct(1,0.8);
interfaceChatBox.setPositionPct(0,0.2);
interfaceChatBox.resize();

scrolls = [];
backgrounds = [];
listboxes = [];
buttons = [];


def getScrollBoxXCoord( n ): # n in range(1,9)
	global boxHeight, boxWidth, totalPadding, paddingPerBox, centralPadding
	boxIndex = (n - 1)/ 2; #0, 1, 2, 3
	if n % 2 == 1: #left hand side
		xCoord = paddingPerBox + boxIndex *( boxWidth + paddingPerBox );
	else: #right hand side pad
		xCoord = 1 - (paddingPerBox + boxWidth  )  -  boxIndex * ( boxWidth );
	return xCoord;


#1. do the following 5 times
for i in range(0, 5):
    #a. create a scrollarea, listbox, a buttons, and append them to the relevant lists.
    #b. add them to the screen, and make them invisible
			
	scroll = glass.GlassScrollArea();	
	scroll.setVisible(False);
	scroll.setOpaque(1);
	scroll.setBackgroundColor(transparency);
	scroll.setSizePct(boxWidth,boxHeight);			
	#position the scrollareas some how
	scroll.setPositionPct( getScrollBoxXCoord( i ) , 0.5 - (( boxHeight + buttonHeight ) /2.0));  
	scrolls.append(scroll);              
		
	#Add the backgrounds before the scrolls. 
	background = glass.GlassLabel(" ");		
	background.setPosition( scroll.getX(), scroll.getY());
	background.setVisible(False);
	backgrounds.append(background);
	glass.GUI_ScreenAddWidget("lobby", background);	
	glass.GUI_ScreenAddWidget("lobby", scroll);
	
	button = glass.GlassButton("Join Team "+str(i));                        
	button.setClickAction("CL_RequestTeam("+str(i)+"); CL_RequestLoadout();");
	button.setVisible(False);
	button.setSizePct( boxWidth , buttonHeight );
	buttons.append(button);
	glass.GUI_ScreenAddWidget("lobby", button);        
			
	#position the buttons below the bottom of the scroll area
	button.setPosition( scroll.getX(), scroll.getY() + scroll.getHeight() );
			
	listbox = glass.GlassListBox();
	listbox.setBackgroundColor(transparency);
	listbox.setSelectionColor(tangoBlueDark);
	listboxes.append(listbox);
	scroll.setContent( listbox );
			
	
        
        
        
def arrange():
	#1. work out how many teams we have
        
	sv_numteams = cvar_getvalue("sv_numteams");
        
	#.2 for eact team, set their UI visible and color the background
	for i in range( 1, sv_numteams):  
		button = lobby.buttons[i];
		scroll = lobby.scrolls[i];
		background = lobby.backgrounds[i];
		
		button.setVisible(True);
		scroll.setVisible(True);
		background.setVisible(True);		
		
		team = savage.Team(i);		
		race = team.getRace();
		
		if race == "human":    
			#scroll.setBackgroundColor(tangoBlueLight);
			background.setImage("/gui/standard/human_playerlist_background.s2g");			
		elif race == "beast":
			#scroll.setBackgroundColor(tangoRedLight);
			background.setImage("/gui/standard/beast_playerlist_background.s2g");
			
		background.setSizePct(boxWidth,boxHeight);
        
	#3. set the UI for other teams invisible
	for i in range( sv_numteams, 5):
			lobby.buttons[i].setVisible(False);
			lobby.scrolls[i].setVisible(False);
			lobby.backgrounds[i].setVisible(False);
        
def update():
	teamsList = [[],[],[],[],[],[],[],[],[]];
	#1. get a list of players on each team
        
	players = savage.getPlayers();
        
	for p in players:
		teamsList[p.getTeam()].append(p);
        
		#2. for each team, add an entry for each person to the list box
        
	for teamIndex in range(1, 5):
		team = teamsList[teamIndex];
		listbox = lobby.listboxes[teamIndex];
		listbox.clear();
		for player in team:
			if player.isCommander():
				name = "^w^icon ../../gui/standard/icons/comm_crown^";
			elif player.isOfficer():
				name = "^w^icon ../../models/human/items/icons/officer1^";
			else:
				name = "^w^icon transparent^";
				name += "^888" + player.getFormattedName();
			listbox.addItem( name );

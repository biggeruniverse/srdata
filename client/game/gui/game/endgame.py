#copyright savagerebirth.com (c) 2011
#this file generates the endgame screen and updates it as neccesary

from silverback import *;
import glass;
import savage;

class StatsHandler:
	def __init__(self):
		pass;

	def onEvent(self, e):
		pass;
	

statsHandler = StatsHandler();

def frame():
	#endgame.updateTeams();
        #endgame.updatePersonal();
        endgame.updateGameInfo();
        #endgame.updateOutcome();

def onShow():
	#1. set all the thingies to indicate that they're loading
	#2. request all the needed stats from the server (match stats or like, statistics from the stats server?) both!
	#3. set up some sort of callback so that the information gets filled in listen for events is that what the http thing in motd does? ya
	
	#fire a request for scores
	CL_RequestScores();
	
	endgame.updatePersonal();
	endgame.accuracy_window.setVisible(False);
	endgame.accuracy_window.update();
	endgame.accuracy_window.centerWindow();
	
	endgame.updateGameInfo();
	endgame.updateOutcome();
	endgame.rebuildAwards(savage.getGameStats());
	
	#gblEventHandler.addHttpListener(endgame.statsHandler);
	
	#endgame.statsHandler.httpHandle = HTTP_Get("http://savagerebirth.com/api/index.php/map/"+cvar_get("svr_world"));

glass.GUI_CreateScreen('endgame');

bg = glass.GlassLabel();
bg.setBackgroundColor(glass.Color(0,0,0,64));
bg.setSizePct(1,1);
glass.GUI_ScreenAddWidget("endgame",bg);

PADDING = int(screenHeight*0.01);

vbreak = 0.2;   vbreakpx = int(vbreak * screenHeight);
hbreak1 = 0.25; hbreak1px = int(hbreak1 * screenWidth);
hbreak2 = 0.75; hbreak2px = int(hbreak2 * screenWidth);

#1. Personal Information
fave_unit = glass.GlassViewer();
fave_unit.setBackgroundColor(transparency);
fave_unit.setEnabled(False);
fave_unit.setPosition(PADDING, PADDING);
fave_unit.setSizePct(0.075,0);
fave_unit.setHeight( vbreakpx - fave_unit.getY() - PADDING);
fave_unit.rotateModel(160);
glass.GUI_ScreenAddWidget("endgame",fave_unit);

name = glass.GlassLabel(allyColorCode + "Player Name");
name.setPosition( fave_unit.getX() + fave_unit.getWidth() + PADDING, fave_unit.getY() );
name.setWidth( hbreak1px - PADDING - name.getX() );
glass.GUI_ScreenAddWidget("endgame",name);

score = glass.GlassLabel("Score: ^g0^w/^r0^w/^y0");
score.setPosition( name.getX(), name.getY() + name.getHeight() + PADDING );
score.setWidth( name.getWidth() );
glass.GUI_ScreenAddWidget("endgame",score);

accuracy = glass.GlassButton("Accuracy");
accuracy.setClickAction("endgame.accuracy_window.setVisible(True); ActionSequence(FadeInAction(endgame.accuracy_window))");
accuracy.setY( score.getY() + score.getHeight() + PADDING);
glass.GUI_ScreenAddWidget("endgame",accuracy);

accuracy_window = AccuracyWindow();
glass.GUI_ScreenAddWidget("endgame", accuracy_window);
#TODO: whatever yeti does to enable the close button (or change what the accuracy button does)

career = glass.GlassButton("Career Stats");
career.setY( accuracy.getY() + accuracy.getHeight() + PADDING);
career.setClickAction(""); #TODO
glass.GUI_ScreenAddWidget("endgame",career);

w = max( career.getWidth(), accuracy.getWidth() );
for widget in (accuracy, career):
	widget.setX( score.getX() + (score.getWidth() - w)//2 );
	widget.setWidth(w);

personal_widgets = (fave_unit, name, score, accuracy, career);

def updatePersonal():
	player = savage.getLocalPlayer();
	
	#If we're a spectator, hide the personal info; otherwise show it
	show_personal = (player.getTeam() != 0);
	for w in endgame.personal_widgets:
		w.setVisible(show_personal);
	if not show_personal:
		return;
	
	endgame.name.setCaption( player.getStatusIcon() + player.getClanIcon() + allyColorCode + player.getName() );
	#crown or officer icon or empty string, then clan icon or empty string, then name
	score = "Score: ";
	score += commColorCode + str(player.getKills()) + "^w/";
	score += enemyColorCode + str(player.getDeaths()) + "^w/";
	score += refColorCode + str(player.getAssists())
	endgame.score.setCaption( score );
	
	model = player.getType().getValue("model");
	endgame.fave_unit.setModel(model);
	endgame.fave_unit.setAnimation("idle");
	endgame.fave_unit.setCameraFOV(45);
	endgame.fave_unit.fitCameraToModel(0);

#2. Chat Box
"""
chat = HUDChatBox(); #yes another one folks!
chat.setSize( hbreak2px - hbreak1px -2*PADDING , vbreakpx - 2*PADDING);
chat.setPosition( hbreak1px + PADDING, PADDING );
chat.resize();
glass.GUI_ScreenAddWidget("endgame",chat);"""

#3. Game Information

time = glass.GlassLabel("_H:MM:SS");
time.setAlignment(glass.Graphics.CENTER);
time.setY(PADDING);
glass.GUI_ScreenAddWidget("endgame",time);

dist = glass.GlassLabel("Longer than\n55% of matches");
dist.setFont(fontSizeSmall);
dist.adjustSize();
dist.setY(time.getY() + time.getHeight());
glass.GUI_ScreenAddWidget("endgame",dist);

windata = glass.GlassLabel("Legion  0\nHorde   0\nTotal   0");
windata.setFont(fontSizeSmall);
windata.adjustSize();
windata.setY(vbreakpx - PADDING - windata.getHeight());
glass.GUI_ScreenAddWidget("endgame",windata);

width = int((screenWidth-hbreak2px-2*PADDING)*0.4) - PADDING;
for w in (time, dist, windata):
	w.setWidth(int(width))
	w.setX( hbreak2px + PADDING )

mapname = glass.GlassLabel("map_name");
mapname.setAlignment(glass.Graphics.CENTER);
mapname.setPosition( time.getX() + time.getWidth() + PADDING, time.getY() );
mapname.setWidth( screenWidth - mapname.getX() - PADDING );
glass.GUI_ScreenAddWidget("endgame",mapname);

map = glass.GlassLabel("");
map.setY(mapname.getY() + mapname.getHeight() + PADDING);
w = min(mapname.getWidth(), vbreakpx - map.getY());
map.setImage("/world/eden2_overhead.jpg");
map.setSize(w, w);
map.setX(mapname.getX() + (mapname.getWidth() - w)//2 );
glass.GUI_ScreenAddWidget("endgame",map);

def updateGameInfo():
	endgame.time.setCaption("^icon ../../gui/standard/icons/timer^" + getGameTimeString( cvar_getvalue("game_timePassedSeconds")));
	endgame.dist.setCaption(LOADING);
	endgame.windata.setCaption("\n"+LOADING);
	endgame.mapname.setCaption(cvar_get("svr_world"));
	overhead = "/world/" + cvar_get("svr_world") + "_overhead.jpg";
	if File_Exists(overhead):
		w, h = endgame.map.getWidth(), endgame.map.getHeight(); 
		endgame.map.setImage(overhead);
		endgame.map.setVisible(True);
		endgame.map.setSize(w,h);
	else:
		endgame.map.setVisible(False);

def updateDist(q):
	"""If this match was:             Then q should be:
	   the shortest on record         0
	   longer than 30%                0.3
	   of mean length                 0.5
	   longest on record              1"""
	
	if q <= 0.5:
		percent = round(100*(1-p));
		desc = "Shorter than";
	else:
		percent = round(100*p);
		desc = "Longer than";
	percent = str(int(percent));
	endgame.dist.setCaption(desc + "\n" + percent + "% of matches");

def updateWinData(team_wins):
	#team_wins: a list of integers. The ith entry is the number of times team i has won this map. For example: [0, 100, 100];
	caption = "";
	for i in (1,2):
		team = savage.Team(i);
		caption += team.getNameColorCode() + team.getRace() + ": " + team_wins[i] + "\n";
	caption += "Total: " + str(sum(team_wins));
	endgame.windata.setCaption(caption);

#4. Outcome Label

outcome = glass.GlassLabel();
outcome.setOpaque(False);
outcome.setPosition(hbreak1px + PADDING, PADDING);
outcome.setWidth(hbreak2px - hbreak1px - 2*PADDING);
outcome.setHeight(outcome.getWidth()//5);
glass.GUI_ScreenAddWidget("endgame",outcome);

def updateOutcome():
	w, h = endgame.outcome.getWidth(), endgame.outcome.getHeight();
	if savage.getLocalTeam().getWinStatus():
		endgame.outcome.setImage("/gui/standard/images/endgame_victory.s2g");
	else:
		endgame.outcome.setImage("/gui/standard/images/endgame_defeat.s2g");
	endgame.outcome.setSize(w,h);

#5 Bottom Buttons

tolobby = glass.GlassButton("<< BACK TO LOBBY");
tolobby.setPosition(PADDING, screenHeight-PADDING-tolobby.getHeight());
tolobby.setClickAction("GUI_ShowScreen('lobby')");
glass.GUI_ScreenAddWidget("endgame",tolobby);

#buddies = BuddyListGUI();
#buddies.setAlignment(glass.Graphics.CENTER);
#buddies.setPosition( (screenWidth-buddies.getWidth())//2, screenHeight-PADDING-buddies.getHeight() );
#glass.GUI_ScreenAddWidget("endgame",buddies);

battle = glass.GlassButton("TO BATTLE! >>");
battle.setClickAction("CL_RequestEndGame(-1)"); #or something
battle.setPosition( screenWidth - PADDING - battle.getWidth(), screenHeight - PADDING - battle.getHeight());
glass.GUI_ScreenAddWidget("endgame",battle);

#6.Awards

awardsTitle = glass.GlassLabel("Awards");
awardsTitle.setAlignment(glass.Graphics.CENTER);
awardsTitle.setFont(fontSizeLarge);
awardsTitle.adjustSize();
awardsTitle.setPosition(outcome.getX(), outcome.getY() + outcome.getHeight() + PADDING);
awardsTitle.setWidth(outcome.getWidth());
awardsTitle.setForegroundColor(gold);
glass.GUI_ScreenAddWidget("endgame", awardsTitle);

awardsScroll = glass.GlassScrollArea();
awardsScroll.setBackgroundColor(tangoGrey6);
awardsScroll.setPosition(awardsTitle.getX(), awardsTitle.getY() + awardsTitle.getHeight() + PADDING);
#awardsScroll.setSize(outcome.getWidth(), screenHeight - awardsScroll.getY() - 2*PADDING - buddies.toggle.getHeight());
awardsScroll.setSize(outcome.getWidth(), screenHeight - awardsScroll.getY() - 2*PADDING)
awardsScroll.setScrollPolicy(awardsScroll.SHOW_NEVER, awardsScroll.SHOW_ALWAYS);
glass.GUI_ScreenAddWidget("endgame",awardsScroll);

awards = glass.GlassContainer()
awards.setWidth(awardsScroll.getWidth() - awardsScroll.getScrollbarWidth());
awardsScroll.setContent(awards);


def rebuildAwards(data):
	"""data = {
		"^gBest Commander^w (%.1f rating)": "0;0;0",
		"^gSadist^w (%d Kills)": "0;0;0",
		"^gUnbreakable^w": "0;0;0",
		"^gMost Violent^w (%d Player Damage)": "0;0;0",
		"^Minute Man^w (%.1f Kills/min)": "0;0;0",
		"^gSurvivor^w (%d Kills in a row)": "0;0;0",
		"^gHero^w (Last Hit)": "0;0;0",
		"^gHomewrecker^w (%d Building Damage)": "0;0;0",
		"^gOutpost Basher^w (%d Outpost Damage)": "0;0;0",
		"^gDownsizer^w (%d Worker Kills)": "0;0;0",
		"^gSiege Hater^w (%d Killed)": "0;0;0",
		"^gCapitalist^w (Surplus of %d Gold)": "0;0;0",
		"^gEntrepreneur^w (Earned %d Gold)": "0;0;0",
		"^gBest Flag Thief^w (%d Flags)": "0;0;0",
		"^gBruce Lee^w (%d Blocks)": "0;0;0",
		"^gMartyr^w (%d Sacrifices)": "0;0;0",
		"^gBest Healer^w (%d Aggregated XP)": "0;0;0",
		"^gBest Miner^w (%d Resources)": "0;0;0",
		"^gBob The Builder^w (%d HP)": "0;0;0",
		"^gVeteran^w (Most XP)": "0;0;0",
		"^gMartial Artist^w (%d Melee Kills)": "0;0;0",
		"^gCarnivore^w (%d pints of blood)": "0;0;0",
		"^gTeacher's Pet^w (%d Orders Followed)": "0;0;0",
		"^gFlurry Bunny!^w (%d Jumps)": "0;0;0",
		"^900Buffy McBuffin^w (%d Self-Buffs)": "0;0;0",
		"^900Big Spender^w (Spent %d Gold)": "0;0;0",
		"^Communist^w (Used %d Team Gold)": "0;0;0",
		"^yMMORPG Fan^w (%d NPC Kills)": "0;0;0",
		"^900Reaper's Best Buddy^w": "0;0;0",
		"^900Task Master^w (%d Orders Given)": "0;0;0",
	};"""
	
	endgame.awards.clear();
	
	COLS = 2;
	PADDING = 2;
	y = PADDING;
	colors = [tangoGrey3, tangoGrey4];
	
	if len(data) == 0:
		return; #no awards!
	
	for i, item in enumerate(data.iteritems()):		
		award, idString = item;

		recipients = []

		for id_ in idString.split(";"):
			try:
				recipients.append(savage.Player(int(id_)).getFormattedName())
			except:
				pass
		
		index = award.find(" (");
		if index == -1:
                        name = award
		else:
		#	#remove color codes                it's less hackish if you just edit awards.cfg ^^
		#	if '0' <= award[1] <= '9':
		#		name = award[4:index];
		#	else:
		#		name = award[2:index];
                        name = award[0:index]
		icon = "/textures/awards/" + name.replace(' ','_').lower() + ".s2g";
		
		award_icon = glass.GlassLabel("");
		award_icon.setImage(icon);
		
		award_name = glass.GlassLabel(award);
		award_name.setFont(fontSizeSmall);
		awardee = recipients[0] if len(recipients) > 0 else "";
		award_owner = glass.GlassLabel(awardee);
		bg = glass.GlassLabel("");
		bg.setOpaque(True);
		bg.setBackgroundColor(colors[(i//COLS)%len(colors)]);
		
		#1. position the background
		bg.setX( PADDING + (PADDING + endgame.awards.getWidth()//COLS)*(i%COLS) );
		bg.setWidth( (endgame.awards.getWidth() - PADDING*(COLS+1) )//COLS );
		bg.setY( y );
		
		#2. position the labels - these will determine the height of the box
		award_name.setY(bg.getY() + PADDING);
		award_owner.setY(award_name.getY() + award_name.getHeight() + PADDING);
		bg.setHeight(3*PADDING + award_name.getHeight() + award_owner.getHeight());
		
		tools.widgetInfoDump(award_name,"NAME")
		tools.widgetInfoDump(award_owner,"OWNER")
		
		#3. the icon is square and fills the bg's height
		h = bg.getHeight() - 2*PADDING;
		award_icon.setSize(h, h);
		award_icon.setPosition(bg.getX() + PADDING, bg.getY() + PADDING);
		
		#4. offset the labels and set their width
		award_name.setX(award_icon.getX() + award_icon.getWidth() + PADDING);
		award_owner.setX(award_name.getX());
		award_name.setWidth(bg.getWidth() - award_icon.getWidth() -3*PADDING);
		award_owner.setWidth(award_name.getWidth());
		
		#5. add the widgets to the container
		endgame.awards.add(bg);
		endgame.awards.add(award_icon);
		endgame.awards.add(award_name);
		endgame.awards.add(award_owner);
		
		#6. update y if we need a new row
		if i % COLS == COLS - 1:
			y += bg.getHeight() + PADDING;
		
		#7. if we have runners-up, add them to the tooltip info
		if len(recipients) > 1:
			tooltip = "Runners Up:";
			for i, p in enumerate(recipients[1:]):
				tooltip += "\n" + str(i+2) + ". " + p;
			bg.setTooltip(tooltip);
			award_icon.setTooltip(tooltip);
			award_name.setTooltip(tooltip);
			award_owner.setTooltip(tooltip);
	
	if i % COLS != COLS - 1:
		y += bg.getHeight(); #in case we didn't end with a full row
	
	endgame.awards.setHeight(y);

	tools.widgetInfoDump(endgame.awards,"AWARDS")


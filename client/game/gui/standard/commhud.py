# (c) 2010 savagerebirth.com
# this file assembles the Commander's HUD

from silverback import *;
import glass;
import savage;
import commcontexts;

def frame():
	commhud.resourcesPanel.update();
	commhud.queueWindow.update();
	commhud.voteWindow.frame();
	commhud.fpswindow.update();
	commhud.unitinfowindow.updateUnitInfo();
	if commhud.scoreboard.isVisible(): 
		commhud.scoreboard.update();
	
	gametime = getGameTimeString(cvar_getvalue("game_timeLimitSeconds"));
	if gametime != "":
		if cvar_getvalue("game_timeLimitSeconds") < 45:
			gametime = "^900"+gametime;
		commhud.timer.setCaption("^icon ../../gui/standard/icons/timer^" + gametime);
		commhud.timer.adjustSize();
        else:
		commhud.timer.setCaption("");		

def onShow():
	commcontexts.buildContextsIfNeeded();
	commhud.contextmenu.setVisible(False);
	commhud.contextmenu.close();
	
	commhud.resourcesPanel.resetDiffCounters();
	commhud.resourcesPanel.update();
	commhud.chatBox.deactivate();
	commhud.minimap.setMap(cvar_get("world_overhead"));
	commhud.unitinfowindow.buildUnitInfo(savage.Team( savage.getLocalPlayer().getTeam() ));	
	commhud.researchWindow.onTeamChange();
	commhud.scoreboard.arrange();
	commhud.scoreboard.update(); #remove the placeholders in scoreboard

glass.GUI_CreateScreen('commhud');

selectionList = [];

def clearSelection(send=True):
	for obj in commhud.selectionList:
		obj.unselect();
	commhud.selectionList = [];
	if send:
		CL_SendSelection([]);  #tell the server we want our selection cleared

def selectObject(obj, ignorekey):
	if not Input_IsKeyDown(KEY_SHIFT) and not ignorekey:
		commhud.clearSelection();

	if obj == None:
		commhud.clearSelection();
		return;

	if obj not in commhud.selectionList:
		obj.select();
		commhud.selectionList.append(obj);

def ResearchSimple(typename):
	objtype = savage.getObjectType(typename);

	team = savage.Team(savage.getLocalPlayer().getTeam());

	value = objtype.getValue("builder1");
	if value != "":
		candidates = team.getObjectsByType(value);
		con_println("candidates:"+str(len(candidates))+"\n");
		if len(candidates) == 0:
			return False;
		else:
			#TODO: base this on which building will be available first
			builder = candidates[int(M_Randnum(0, len(candidates)))];
			gblQueue.addResearch(savage.ResearchItem(objtype.typeId, builder.objectId, 0,0));

def defaultAction(x, y):
	obj = savage.getObjectUnder(x,y);
	teamNum = savage.getLocalTeam().teamId;
	if obj == None:
		CL_CommanderLeftClick(); #send it thru to the hardcode to see if something is doing
	CL_SendSelection([ go.objectId for go in commhud.selectionList if go.getType().isUnitType() and go.getTeam() == teamNum]);
	if obj == None:
		CL_OrderWaypoint(x,y);
	else:
		CL_OrderWaypoint(x,y,obj.objectId);

class CommInputHandler:
	def __init__(self):
		self.pressX = 0;
		self.pressY = 0;

	def onMouseClick(self, e):
		cm = commhud.contextmenu;
		x,y = Input_GetMouseXY();
		if e.button == MOUSE_RIGHTBUTTON:
			cm.coords = x,y; #remember where we clicked!
			if Input_IsKeyDown(KEY_CTRL):
				commhud.defaultAction(x,y);
			else:
				obj = savage.getObjectUnder(x,y);
				ctx = self.determineContext(obj);
				ctx.object = obj;
				cm.buildContext( ctx );
				if x < cm.RADIUS:
					x = cm.RADIUS;
				elif x > screenWidth - cm.RADIUS:
					x = screenWidth - cm.RADIUS;
				if y < cm.RADIUS:
					y = cm.RADIUS;
				elif y > screenHeight - cm.RADIUS:
					y = screenHeight - cm.RADIUS;
			
				cm.setPosition( x-cm.RADIUS , y-cm.RADIUS );
				actions = cm.context.getContextActions();
				if len(actions) > 0:
					cm.setAlpha(0);
					cm.open();

		elif e.button == MOUSE_LEFTBUTTON:
			cm.close();
			if commhud.selectionRect.getWidth() > 0:
				sel = savage.getObjectsWithin(commhud.selectionRect.getX(), commhud.selectionRect.getY(), commhud.selectionRect.getWidth(), commhud.selectionRect.getHeight());
				for o in sel:
					commhud.selectObject(o, True);
				commhud.selectionRect.setSize(0, 0);
			else:
				obj = savage.getObjectUnder(x,y);
				if obj == None:
					CL_CommanderLeftClick();
				commhud.selectObject(obj, False);

		else:
			cm.close();

	def onMouseMotion(self, e):
		pass;

	def onMouseScroll(self, e):
		pass;
	
	def onMousePress(self, e):
		if e.button == MOUSE_LEFTBUTTON:
			self.pressX = e.x;
			self.pressY = e.y;
			if Input_IsKeyDown(KEY_SHIFT) == False:
				commhud.clearSelection(False);
	
	def onMouseReleased(self, e):
		pass;
	
	def onMouseDrag(self, e):

		if e.button == MOUSE_LEFTBUTTON:
			sX = self.pressX;
			sY = self.pressY;
			eX = 0;
			eY = 0;
			if e.x < sX:
				sX = e.x+1;
				eX = self.pressX;
			else:
				eX = e.x;

			if e.y < sY:
				sY = e.y+1;
				eY = self.pressY;
			else:
				eY = e.y;

			commhud.selectionRect.setPosition(sX, sY);
			commhud.selectionRect.setSize(eX-sX, eY-sY);

			sel = savage.getObjectsWithin(commhud.selectionRect.getX(), commhud.selectionRect.getY(), commhud.selectionRect.getWidth(), commhud.selectionRect.getHeight());
			for o in sel:
				commhud.selectObject(o, True);
	
	def determineContext(self, obj):
		cm = commhud.contextmenu;
		try:
			name = obj.getType().getName() if obj != None else None;
			ctx = commcontexts.contextDict[name];
		except KeyError:
			#if the key doesn't exist, because we haven't defined a context
			ctx = commcontexts.emptycontext;
		return ctx

class MapClickHandler:
	def onMouseClick(self, e):
		w = e.widget.getWidth();
		h = e.widget.getHeight();

		wsize = World_GetGridSize()*100;

		mapx, mapy, z = savage.getLocalPlayer().getPosition();

		mapx = (e.x / float(w)) * wsize;
		mapy = wsize - (e.y / float(h)) * wsize;

		savage.getLocalPlayer().setPosition(Vec3(mapx, mapy, z));

	def onMouseMotion(self, e):
		pass;
	
	def onMousePress(self, e):
		pass;
	
	def onMouseReleased(self, e):
		pass;
	
	def onMouseDrag(self, e):
		pass;

canvas = glass.GlassCanvas();

comminputhandler = CommInputHandler();
canvas.addMouseListener(comminputhandler);

selectionRect = glass.GlassContainer();
selectionRect.setBackgroundColor(tangoGreenLight);
selectionRect.setAlpha(64);
canvas.add(selectionRect);

#starting from the top-centre (12 o'clock) of the screen and proceeding anti clockwise

## RESOURCES/INFO PANEL ##

resourcesPanel = ResourcePanel();
glass.GUI_ScreenAddWidget("commhud", resourcesPanel);

## MINIMAP ##
#Beard: skope suggests moving this to the bottom
minimap = glass.GlassMiniMap();
minimap.setPositionPct(0.01875, 0.025);
minimap.setSize(int(0.208*screenHeight),int(0.208*screenHeight));
minimap.addMouseListener(MapClickHandler());

## TIMER ##
timer = glass.GlassLabel("_AB:CD ");
timer.setFont(glass.GUI_GetFont(20));
timer.setPositionPct(0.01875, 0.025+0.208);
glass.GUI_ScreenAddWidget("commhud", timer);

## VOTES ##

voteWindow = VoteInfoBox();
glass.GUI_ScreenAddWidget("commhud", voteWindow);
voteWindow.setPosition( minimap.getWidth() + minimap.getX() + 10, -voteWindow.getHeight());

## CHAT BOX ##

chatBox = HUDChatBox();
chatBox.setPositionPct(0,0.625);
chatBox.setX(10);
chatBox.setBackgroundColor(glass.Color(0,0,0,100));
chatBox.setSizePct(0.4,0.23);
chatBox.resize();
glass.GUI_ScreenAddWidget("commhud", chatBox);
chatBox.alwaysShowInput(1)
chatBox.buffer.addMouseListener(comminputhandler); #TODO doesn't work

#the bottom-level canvas
canvas.setSizePct(1,1);
canvas.setBackgroundColor(transparency);
canvas.setPosition(0,0);
glass.GUI_ScreenAddWidget("commhud",canvas);

glass.GUI_ScreenAddWidget("commhud",minimap);



#next, any objects in the screen's center, proceeding from the top downward

## VOICE CHAT ##

voiceChat = VoiceChatBox();
voiceChat.setSizePct(0.3,0.35);
voiceChat.table.adjustSizeToPct(1,1);
glass.GUI_ScreenAddWidget("commhud",voiceChat);
voiceChat.centerWindow();
voiceChat.setY(screenHeight/2+40);

## NOTIFICATIONS ##
scroll = glass.GlassScrollArea();
scroll.setAutoscroll(1);
scroll.setSizePct(0.32,0.16);
scroll.setPosition(screenWidth-scroll.getWidth() - 10,10);
scroll.setPosition(screenWidth-360, 10);
scroll.setScrollPolicy(1,1); #SHOW_NEVER
glass.GUI_ScreenAddWidget("commhud", scroll);

notifyBuffer = MessageBuffer(["notify"]); #TODO notify_generalhide too?
scroll.setContent(notifyBuffer);
notifyBuffer.setSize(scroll.getWidth(), scroll.getHeight());
notifyBuffer.setFadeTop(1);
notifyBuffer.setFadeBottom(0);
notifyBuffer.showTime(0);
for i in range(10):
	notifyBuffer.addRow(" ");

## QUICKBAR ##
quickbar = glass.GlassContainer();
quickbar.setBackgroundColor(glass.Color(0,0,0,128));
glass.GUI_ScreenAddWidget("commhud",quickbar);
quickbar.setPositionPct(.25,.9);
quickbar.setSizePct(.5,.1);

resign = glass.GlassButton("Resign");
quickbar.add(resign);
resign.setPositionPct(0,.01);
resign.setClickAction("CL_RequestResign()");

research = glass.GlassButton("Research");
quickbar.add(research);
research.setPositionPct(.15,.01);
research.setClickAction("""
if commhud.researchWindow.isVisible():
	commhud.researchWindow.close();
else:
	commhud.researchWindow.open();
""");

researchWindow = CommResearchWindow();
glass.GUI_ScreenAddWidget("commhud",researchWindow);

queue = glass.GlassButton("Queue");
quickbar.add(queue);
queue.setPositionPct(.34,.01);
queue.setClickAction("""
if commhud.queueWindow.isVisible():
	commhud.queueWindow.close();
else:
	commhud.queueWindow.open();
""");

queueWindow = ResearchManager();
gblEventHandler.addGameListener(queueWindow);
gblQueue.addListener(queueWindow);
glass.GUI_ScreenAddWidget("commhud",queueWindow);

#last, the context menu
contextmenu = ContextMenu();
glass.GUI_ScreenAddWidget("commhud",contextmenu);

## FPS WINDOW ##

fpswindow = FpsWindow();
fpswindow.setPositionPct(0, 0.5);
glass.GUI_ScreenAddWidget("commhud",fpswindow);

## unit info window ##

unitinfowindow = UnitInfoWindow();
glass.GUI_ScreenAddWidget("commhud",unitinfowindow);
unitinfowindow.setPosition(minimap.getX(),timer.getY()+timer.getHeight() + 10);

### SCOREBOARD ##

scoreboard = TeamScore();
glass.GUI_ScreenAddWidget("commhud",scoreboard);


from silverback import *;
import glass;
import savage;

class CommInputHandler:
	def __init__(self):
		self.pressX = 0;
		self.pressY = 0;
		self.lastClickTime = 0;
		self.seq = None;
		self.selection = CommSelection()

	def onMouseClick(self, e):
		#cm = commhud.contextmenu;
		x = e.x
		y = e.y
		if e.button == MOUSE_RIGHTBUTTON:
			#cm.coords = x,y; #remember where we clicked!
			#cm.close();
			#if Input_IsKeyDown(KEY_CTRL):
			if CL_CommanderMode() in (CMDR_PLACING_OBJECT, CMDR_PLACING_LINK, CMDR_PICKING_LOCATION, CMDR_PICKING_UNIT):
				CL_CommanderExitMode();
			else:
				commhud.defaultAction(x,y);
			#else:
			#    obj = savage.getObjectUnder(x,y);
			#    ctx = self.determineContext(obj);
			#    ctx.object = obj;
			#    cm.buildContext( ctx );
			#    if x < cm.RADIUS:
			#        x = cm.RADIUS;
			#    elif x > screenWidth - cm.RADIUS:
			#        x = screenWidth - cm.RADIUS;
			#    if y < cm.RADIUS:
			#        y = cm.RADIUS;
			#    elif y > screenHeight - cm.RADIUS:
			#        y = screenHeight - cm.RADIUS;
			#
			#    cm.setPosition( x-cm.RADIUS , y-cm.RADIUS );
			#    actions = cm.context.getContextActions();
			#    if len(actions) > 0:
			#        cm.setAlpha(0);
			#        cm.open();

		elif e.button == MOUSE_LEFTBUTTON:
			#cm.close();
			if commhud.selectionRect.getWidth() > 0:
				#sel = savage.getObjectsWithin(commhud.selectionRect.getX(), commhud.selectionRect.getY(), commhud.selectionRect.getWidth(), commhud.selectionRect.getHeight());
				#for o in sel:
				#    commhud.selectObject(o, True);
				commhud.selectionRect.setSize(0, 0);

			elif savage.getGameTime() - self.lastClickTime < 500:
				try:
					obj = savage.getObjectsWithin(x-1,y-1,3,3)[0];
					if obj == None:
						CL_CommanderLeftClick();
					self.selection.selectObjectAndRadius(obj, 500);
					commhud.selection.updateSelection(self.selection);
				except IndexError:
					pass;

			else:
				try:
					if CL_CommanderMode() in (CMDR_PLACING_OBJECT, CMDR_PLACING_LINK, CMDR_PICKING_LOCATION, CMDR_PICKING_UNIT):
						CL_CommanderLeftClick();				
					else:
						obj = savage.getObjectsWithin(x-1,y-1,3,3)[0]
						self.selection.selectObject(obj, False);
						commhud.selection.updateSelection(self.selection);
				except IndexError:
					pass
			self.lastClickTime = savage.getGameTime();

		else:
			#cm.close();
			pass;

	def onMouseMotion(self, e):
		pass;

	def onMouseEnter(self, e):
		pass;

	def onMouseExit(self, e):
		pass;

	def onMouseScroll(self, e):
		pass;
	
	def onMousePress(self, e):
		if CL_CommanderMode() in (CMDR_PLACING_OBJECT, CMDR_PLACING_LINK, CMDR_PICKING_LOCATION, CMDR_PICKING_UNIT):
			return;
		elif e.button == MOUSE_LEFTBUTTON:
			self.pressX = e.x;
			self.pressY = e.y;
			commhud.selectionRect.setVisible(True);
			if Input_IsKeyDown(KEY_SHIFT) == False:
				self.selection.clear(False);
		"""
		elif e.button == MOUSE_RIGHTBUTTON:
			obj = savage.getObjectUnder(e.x,e.y);
			if obj is not None and commhud.selection.empty():
				commhud.selection.selectObject(obj, True);
				teamNum = savage.getLocalTeam().teamId;
				commhud.selection.send(teamNum)
			self.seq = ActionSequence(savage.WaitAction(150), OpenContextAction(savage.getObjectUnder(e.x,e.y), e.x, e.y));
		"""
		
	def onMouseReleased(self, e):
		commhud.selectionRect.setVisible(False);
		if self.selection.containsUnits():
			self.selection.filterUnitsOnly()
		commhud.selection.updateSelection(self.selection)
		commhud.selection.send()
		if e.button == MOUSE_RIGHTBUTTON and self.seq is not None:
			self.seq.stop();
			self.seq = None;
	
	def onMouseDrag(self, e):
		if CL_CommanderMode() in (CMDR_PLACING_OBJECT, CMDR_PLACING_LINK, CMDR_PICKING_LOCATION, CMDR_PICKING_UNIT):
			return;
		elif e.button == MOUSE_LEFTBUTTON:
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

			commhud.selectionRect.setVisible(True);
			commhud.selectionRect.setPosition(sX, sY);
			commhud.selectionRect.setSize(eX-sX, eY-sY);

			self.selection.clear()

			if commhud.selectionRect.getWidth() > 0 and commhud.selectionRect.getHeight() > 0:
				sel = savage.getObjectsWithin(commhud.selectionRect.getX(), commhud.selectionRect.getY(), commhud.selectionRect.getWidth(), commhud.selectionRect.getHeight());
				for o in sel:
					self.selection.selectObject(o, True);
				commhud.selection.updateSelection(self.selection)


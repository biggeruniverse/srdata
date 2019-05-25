#(c) 2012 savagerebirth.com

from silverback import *
import savage

class CommSelectionEvent:
	def __init__(self, sel):
		self.selection = sel

	def isEmpty(self):
		return not bool(len(self.selection.list));

	def isSingle(self):
		if len(self.selection.list) == 1:
			return True;
		else:
			return False;

class CommSelection:
	def __init__(self):
		self.list = []
		self.listeners = []

	def empty(self):
		return not self.list

	def clear(self, send=True):
		for obj in self.list:
			obj.unselect()
		self.list = []
		self.fireEvent()
		if send:
			self.send()  #tell the server we want our selection cleared

	def setSelection(self, s):
		self.clear(False)
		for go in s:
			if go is not None:
				self.selectObject(go, True)
		self.list = list(s)
		self.fireEvent()

	def updateSelection(self, other):
		if isinstance(other, CommSelection):
			old = set(self.list)
			new = set(other.list)
			diff = new - old
			rmdiff = old - new

			for o in rmdiff:
				self.list.remove(o)

			for o in diff:
				self.list.append(o)
				#newly selected things must be sounded...
				sound = o.getType().getValue("selectionSound")
				Sound_PlaySound(sound)

			# did the selection actually change?
			if diff or rmdiff:
				self.fireEvent()

	def selectObject(self, obj, ignorekey):
		if not Input_IsKeyDown(KEY_SHIFT) and not ignorekey:
			self.clear(False)
		if obj == None:
			self.clear()
			self.fireEvent()
			return
		if obj not in self.list:
			obj.select()
			self.list.append(obj)
		elif not ignorekey:
			obj.unselect()
			self.list.remove(obj)

		self.fireEvent()

	def selectObjectAndRadius(self, obj, r=100):
		self.clear();

		if obj == None:
			return;

		obj.select();
		self.list.append(obj);

		t = obj.getType();
		for o in savage.getRadiusObjects(obj.objectId, r):
			if o.getType() == t:
				o.select()
				self.list.append(o)
		self.fireEvent()

	def send(self, onTeam=0):
		sel = [go.objectId for go in self.list]
		if onTeam > 0:
			sel = [go.objectId for go in self.list if go.getTeam() == onTeam]
		CL_SendSelection(sel)

	def containsPlayers(self):
		for go in self.list:
			if go.isPlayer():
				return True
		return False

	def containsUnits(self):
		for go in self.list:
			if go.getType().isUnitType():
				return True
		return False

	def filterUnitsOnly(self):
		for go in self.list:
			if not go.getType().isUnitType() or go.getType().isNPCType(): # We don't want no NPCs in our selection!
				go.unselect()
				self.list.remove(go)
		self.fireEvent()

	def getUnits(self, onTeam):
		return [go for go in self.list if go.getType().isUnitType() and go.getTeam() == onTeam]

	def addListener(self, l):
		self.listeners.append(l)

	def fireEvent(self):
		e = CommSelectionEvent(self)
		for l in self.listeners:
			 l.onSelection(e)

	# dead things aren't useful for our selections usually
	# if player REALLY wants to select them, they certainly can after this
	def onEvent(self, e):
		if e.eventType == 'obituary':
			deadguy = e.getTarget()

			if deadguy in self.list:
				self.list.remove(deadguy)
				deadguy.unselect()
				self.fireEvent()
				self.send()


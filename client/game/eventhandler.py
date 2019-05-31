# (c) 2010 savagerebirth.com
#
# A rather basic event handler with queueing
#
# Handles all the event types that can come from the engine, basically acting as
# an interface between the engine and the python code
#
# Poor event handler. (Fatty)
#
from silverback import *
import logging
from stackless import tasklet,channel,stackless
import threading
#import thread

class Event:
	def __init__(self):
		pass
	
class NotifyEvent(Event):
	def __init__(self, sc, f, s):
		self.string = s
		self.scope = sc
		self.fromstr = f

	def __str__(self):
		return self.scope+" "+self.fromstr+"> "+self.string

class VoteEvent(NotifyEvent):
	def __init__(self):
		NotifyEvent.__init__(self, "vote", "server", "A vote has been called.")


class GameEvent(Event):
	def __init__(self, etype, sid, tid):
		self.eventType = etype
		self.sourceId = sid
		self.targetId = tid

	def getSource(self):
		import savage
		return savage.getGameObject(self.sourceId)

	def getTarget(self):
		import savage
		return savage.getGameObject(self.targetId)

	def __str__(self):
		return "Game event '"+self.eventType+"'\nsource objId: "+str(self.sourceId)+"\ntarget objId: "+str(self.targetId)

class ResearchEvent(GameEvent):
	def __init__(self, etype, src, objtype, qid):
		GameEvent.__init__(self, etype, src, -1)
		self.objtype = objtype
		self.queueId = qid

class RequestEvent(GameEvent):
	def __init__(self, etype, src, param):
		GameEvent.__init__(self, etype, src, -1)
		self.parameter = param

class HttpEvent(Event):
	def __init__(self, handle, data, code):
		self.responseMessage = data
		self.handle = handle
		self.responseCode = code

	def __str__(self):
		return "Http event "+str(self.handle)+":\n"+self.responseMessage

class SystemEvent(Event):
	def __init__(self, param1, param2):
		self.param1 = param1
		self.param2 = param2

	def __str__(self):
		return "System event "+ str(self.param1)+ " "+str(self.param2)

class WaypointEvent(GameEvent):
	def __init__(self, etype, sid, tid, msg):
		GameEvent.__init__(self, etype, sid, tid)
		self.message = msg

class DemoEvent(Event):
	def __init__(self, time, frames, fps):
		self.time = time
		self.frames = frames
		self.fps = fps

class HistoryEvent(Event):
	def __init__(self, type):
		self.type = type

class CommanderEvent(GameEvent):
	def __init__(self, etype, sid, tid, x, y):
		GameEvent.__init__(self, etype, sid, tid)
		self.pos = (x, y)

class EventHandler:
	logger = logging.getLogger("silverback.eventhandler")
	def __init__(self):
		#events
		self.eventQueue = channel()
		self.eventQueue.preference = 1

		#listeners
		self.notifyListeners = []
		self.gameListeners = []
		self.httpListeners = []
		self.systemListeners = []
		self.voteListeners = []
		self.demoListeners = []
		self.historyListeners = []

		self.stop = threading.Event()
		self.queue_thread = threading.Thread(name="Event queue runner", target=self._run_queue)
		self.stop.clear()
		self.queue_thread.start()

	def _process_event(self, e):
		#check the type of e, get the correct list of listeners
		if isinstance(e, VoteEvent):
			listenerList = self.voteListeners
		elif isinstance(e, NotifyEvent):
			listenerList = self.notifyListeners
		elif isinstance(e, GameEvent):
			listenerList = self.gameListeners
		elif isinstance(e, HttpEvent):
			listenerList = self.httpListeners
		elif isinstance(e, SystemEvent):
			listenerList = self.systemListeners
		elif isinstance(e, DemoEvent):
			listenerList = self.demoListeners
		elif isinstance(e, HistoryEvent):
			listenerList = self.historyListeners

		#callback to all the listeners in the list
		for l in listenerList:
			try:
				l.onEvent(e)
			except BaseException as ex:
				try:
					import traceback;
					self.logger.error( traceback.format_exc());
				except ImportError:
					self.logger.error("EventHandler caught exception: "+str(ex)+"\n");

	def _run_queue(self):
		while not self.stop.is_set():
			e = self.eventQueue.receive()
			self._process_event(e)

	def _send_event(self, e):
		self.eventQueue.send(e)

	def send_event(self, e):
		#task = stackless.tasklet(self._send_event)(e)
		task = threading.Thread(name="send event", target=self._send_event, args=(e,))
		task.start()

	#runQueue is called by the engine every frame before gui logic
	#NOTE: this is deprecated in favor of the above _run_queue stackless thread method
	def runQueue(self):
		pass;
		"""
		for e in self.eventQueue:
			self._process_event(e)
		#clear it
		self.eventQueue = []
		"""

	def addNotifyListener(self, l):
		self.notifyListeners.append(l)

	def addGameListener(self, l):
		self.gameListeners.append(l)

	def addHttpListener(self, l):
		self.httpListeners.append(l)

	def addSystemListener(self, l):
		self.systemListeners.append(l)

	def addVoteListener(self, l):
		self.voteListeners.append(l)

	def addDemoListener(self, l):
		self.demoListeners.append(l)

	def addHistoryListener(self, l):
		self.historyListeners.append(l);

	def removeHttpListener(self, l):
		self.httpListeners.remove(l)

	def gameEvent(self, etype, sid, tid):
		e = GameEvent(etype, sid, tid);
		self.send_event(e)

	def waypointEvent(self, sid, tid, msg, etype="waypoint"):
		e = WaypointEvent(etype, sid, tid, msg)
		self.send_event(e)

	def notifyEvent(self, scope, fromstr, string):
		e = NotifyEvent(scope, fromstr, string)
		self.send_event(e)

	def httpEvent(self, handle, msgRe, code):
		e = HttpEvent(handle, msgRe, code)
		self.send_event(e)

	def systemEvent(self, p1, p2):
		e = SystemEvent(p1, p2)
		self.send_event(e)

	def voteEvent(self):
		e = VoteEvent()
		self.send_event(e)

	def researchEvent(self, etype, src, objtype, qid):
		e = ResearchEvent(etype, src, objtype, qid)
		self.send_event(e)

	def requestEvent(self, req, src, param):
		e = RequestEvent(req, src, param)
		self.send_event(e)

	def demoEvent(self, time, frames, fps):
		e = DemoEvent(time, frames, fps);
		self.send_event(e)

	def historyEvent(self, type):
		e = HistoryEvent(type);
		self.send_event(e)

	def commEvent(self, type, sid, tid, x, y):
		e = CommanderEvent(type, sid, tid, x, y);
		self.send_event(e)

#this class isn't required in python, but it makes debugging easy
class EventListener:
	def onEvent(self, e):
		con_println("I was called with "+str(e)+"\n")

#now we define a global event handler into the __main__ dictionary
#the engine will be looking for this
#as will all python code that needs to receive events from the engine
gblEventHandler = EventHandler()

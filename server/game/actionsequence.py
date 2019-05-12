# (c) 2011 savagerebirth.com
# defines ActionSequences and the handler that the engine uses as an interface

from stackless import tasklet,channel,stackless;
from collections import deque;
from silverback import *;

class SequenceHandler:
	def __init__(self):
		self.threadCount = 1;
		self.sequences = [];
		self.channel = channel();
		self.channel.preference = 1;

	def pump(self):
		while self.channel.balance < 0:
			self.channel.send(None);

		for seq in self.sequences:
			if seq.isDone() == True:
				self.sequences.remove(seq);
				seq.kill();

	#never call this directly, let ActionSequence call it
	def addSequence(self, seq):
		seq.threadId = self.threadCount;
		self.threadCount += 1;
		self.sequences.append(seq);
		seq.setup(seq);

gblSequenceHandler = SequenceHandler();

#helper function that will pre-empt infinite loops or excessively long-running tasklets
def stackless_frame():
	gblSequenceHandler.pump();
	stacklesslib.main.mainloop.pump()

class ActionSequence(tasklet):
	def __new__(self, *args):
		def handler(*args, **kwargs):
			try:
				args[0].pump();
			except Exception,e:
				try:
					import traceback;
					con_dprintln( "^r" + traceback.format_exc());
				except ImportError:
					con_dprintln("^rError "+str(e)+"\n");
		return tasklet.__new__(self, handler);

	def __init__(self, *args):
		self.actions = deque();
		self.pauseIt = False;
		self.stopFlag = False;
		self.threadId = -1;
		for action in args:
			action.setParent(self);
			self.actions.append(action);
		self.attach();

	def pump(self):
		if self.pauseIt is True:
			return;
		while self.isDone() is not True and self.stopFlag is not True:
			if self.actions:
				action = self.actions.popleft();
				action.run();
				if action.isDone() == False:
					self.actions.appendleft(action);
			nun = gblSequenceHandler.channel.receive();
		con_println("thread "+str(self.threadId)+" stopped\n");
		

	def pause(self):
		self.pauseIt = True;

	def resume(self):
		self.pauseIt = False;

	def attach(self):
		gblSequenceHandler.addSequence(self);

	def isDone(self):
		if len(self.actions) == 0 or self.stopFlag == True:
			return True;
		return False;

	def stop(self):
		self.stopFlag = True;


class ActionSequenceLoop(ActionSequence):
	def __init__(self, *args):
		ActionSequence.__init__(self, *args);
		self.cursor = 0;

	def pump(self):
		if self.pauseIt is True:
			return;
		while self.isDone() is not True and self.stopFlag is not True:
			if self.actions:
				action = self.actions[self.cursor];
				action.run();
				self.cursor += 1;
				if self.cursor >= len(self.actions):
					self.cursor = 0;
			gblSequenceHandler.channel.receive();



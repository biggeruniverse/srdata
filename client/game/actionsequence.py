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
			con_dprintln("sending on channel")
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
		seq.channel = self.channel
		seq.setup((seq,));

gblSequenceHandler = SequenceHandler();

#helper function that will pre-empt infinite loops or excessively long-running tasklets
def stackless_frame():
	gblSequenceHandler.pump();
	stacklesslib.main.mainloop.pump()

class ActionSequence(stackless.tasklet):
	#def __new__(self, *args):
	#	def handler(*args, **kwargs):
	#		try:
	#			args[0].pump();
	#		except Exception as e:
	#			try:
	#				import traceback;
	#				con_dprintln("AS handler: ^r" + traceback.format_exc()+"\n");
	#			except ImportError:
	#				con_dprintln("AS handler: ^rError "+str(e)+"\n");
	#	t = tasklet.__new__(self)
	#	t.bind(handler)
	#	return t

	def __init__(self, *args):
		super(ActionSequence, self).__init__(ActionSequence.handler)
		self.actions = deque();
		self.pauseIt = False;
		self.stopFlag = False;
		self.threadId = -1;
		self.channel = None

		for action in args:
			action.setParent(self);
			self.actions.append(action);
		self.attach()

	@classmethod
	def handler(args):
		try:
			con_dprintln("handler PUMPING\n")
			args[0].pump()
		except Exception as e:
			try:
				import traceback;
				con_dprintln("AS handler: ^r" + traceback.format_exc()+"\n")
			except ImportError:
				con_dprintln("AS handler: ^rError "+str(e)+"\n")

	def pump(self):
		if self.pauseIt is True:
			return;
		while self.isDone() is not True and self.stopFlag is not True:
			if self.actions:
				action = self.actions.popleft();
				action.run();
				if action.isDone() == False:
					self.actions.appendleft(action);
			nun = self.channel.receive();
		con_println("thread "+str(self.threadId)+" stopped\n");

	def run(self):
		con_dprintln("RUNNING")
		self.pump()
		

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



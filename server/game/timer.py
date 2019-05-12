# (c) 2011 savagerebirth.com

class Timer(tasklet):
	def __new__(self, *args):
		def handler(*args, **kwargs):
			try:
				args[0].check();
			except Exception,e:
				try:
					import traceback;
					con_dprintln( "^r" + traceback.format_exc());
				except ImportError:
					con_dprintln("^rError "+str(e)+"\n");
		return tasklet.__new__(self, handler);

	def __init__(self, l, t):
		self.listener = l
		self.time = Host_GetTime() + t;

		self.setup(self);

	def check(self):
		while self.time > Host_GetTime():
			nop = 1; # some NOPs
			nop = nop + 1;
			gblSequenceHandler.channel.receive();
		self.listener.run();


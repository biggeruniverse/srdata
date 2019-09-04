#(c) 2011 savagerebirth.com

def clock_driver(cl):
	cl.run()

class TickAction(Action):
	def __init__(self, clock):
		self.clock = clock
		self.until = 0
		super().__init__()

	def reset(self):
		self.until = 1000 + Host_Milliseconds()

	def run(self):
		pass

	def is_done(self):
		if self.until >= Host_Milliseconds():
			return False
		self.clock.tick()
		return True


class Clock(glass.GlassLabel):
	def __init__(self):
		glass.GlassLabel.__init__(self,"00:00 AM");
		self.thread = ActionSequence(TickAction(self))
		self.thread.set_loop(True)
		#self.thread = Timer(1.0, clock_driver, [self]);


	def tick(self):
		s = Host_GetTime() % 86400;
		hour = s // 3600;
		ampm = "AM";
		blink = ":";

		if hour >= 12:
			ampm = "PM";
			hour -= 12;
		if hour == 0:
			hour = 12;
		minute = (s // 60) % 60
		self.setCaption("%02d%s%02d %s" % (hour,blink,minute,ampm));
		#self.thread = Timer(1.0, clock_driver, [self]);

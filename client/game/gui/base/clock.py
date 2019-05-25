#(c) 2011 savagerebirth.com

class Clock(glass.GlassLabel):
	def __init__(self):
		glass.GlassLabel.__init__(self,"00:00 AM");
		self.thread = Timer(self, 1);


	def run(self):
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
		self.thread = Timer(self, 1);

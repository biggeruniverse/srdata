#(c) 2011 savagerebirth.com
# this is a basic action outline, gui actions extend from this
import silverback

class GuiAction(silverback.Action):
	def __init__(self, widget):
		silverback.Action.__init__(self);
		self.lasttime = Host_Milliseconds();
		self.widget = widget;

	def rateMult(self):
		nowtime = Host_Milliseconds();
		mult = float(nowtime-self.lasttime)/40.0; #25fps
		self.lasttime = nowtime;
		return mult;

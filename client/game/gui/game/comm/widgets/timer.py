
from silverback import *;
import glass;
import savage;

class CommTimer(DefaultContainer):

	def __init__(self):
		DefaultContainer.__init__(self);
		self.timer = DefaultLabel();
		self.timer.setFont(glass.GUI_GetFont(20));
		self.add(self.timer);
		self.setHeight(self.timer.getHeight());
		self.setY(screenHeightPct(.667));

	def frame(self):
		timelimit = cvar_getvalue("game_timeLimitSeconds");
		gametime = getGameTimeString(timelimit);
		if gametime != "":
			if timelimit < 45:
				gametime = "^900"+gametime;
			self.timer.setCaption("^icon ../../gui/standard/icons/timer^" + gametime);
		else:
			self.timer.setCaption("--:--:--");
		self.timer.adjustSize();

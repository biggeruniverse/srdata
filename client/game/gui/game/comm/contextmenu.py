#copyright (c) 2011 savagerebirth.com
#this file is used for the commhud

import glass;
import savage;
import math;

class ContextMenu(DefaultContainer):
	MAX_BUTTONS = 12;
	def __init__(self):
		DefaultContainer.__init__(self);
		#self.setSize((32+3)*4, (32+3)*3);
		
		self.object = None;
		self.currentButtons = [];
		self.context = commcontexts.emptycontext;
		self.lastContext = commcontexts.emptycontext;
		
		gblEventHandler.addGameListener(self);

	def onEvent(self, e):
		if e.eventType == "research_complete":
			self.buildContext(self.context);
	
	def rebuildMenu(self):
		pass;

	def buildContext(self, context):
		self.lastContext = self.context;

		self.context = context;
		self.context.object = self.object;
		self.clear();
		self.rebuildMenu();
		i = 0;
		for action, status in self.context.getContextActions().iteritems():
			button = self.context.getButtonAction(action);
			if status == Hidden:
				button.setVisible(0);
				button.setEnabled(0);
			elif status == Disabled:
				button.setVisible(1);
				button.setEnabled(0);
				button.setForegroundColor(tangoGrey5);
			elif status == Enabled:
				button.setVisible(1);
				button.setEnabled(1);
				button.setForegroundColor(white);

			button.setSize(48, 48);

			x = i % 4 * 50;
			y = i // 4 * 50;

			self.add(button, x, y);

			self.currentButtons.append(button);

			i += 1;
	
	def switchContexts(self, ctx):
		self.buildContext(ctx);

	def close(self):
		pass;

	class RebuildAction(Action):
		def __init__(self, menu, ctx):
			Action.__init__(self);
			self.menu = menu;
			self.ctx = ctx;
		
		def isDone(self):
			return True;
		
		def run(self):
			self.menu.buildContext(self.ctx);


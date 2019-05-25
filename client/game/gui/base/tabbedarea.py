#(c) 2012 savagerebirth.com

import glass;
import logging;

logger = logging.getLogger('gui');

class DefaultTabbedArea(glass.GlassTabbedArea):
	
	def __init__(self):
		glass.GlassTabbedArea.__init__(self);
		self.tabsList = OrderedDict();
		self.padding = 28
		self.pixelPerChar = 8;
		
	def addTab(self, tab, widget):			
		glass.GlassTabbedArea.addTab(self, tab, widget);
		self.tabsList[tab] = widget;
		self.checkLength();

	def removeTab(self, tab):
		glass.GlassTabbedArea.removeTab(self, self.tabsList.pop(tab));
		self.checkLength();

	def removeTabWithIndex(self, ind): 
		#glass.GlassTabbedArea_removeTabWithIndex(self, ind);
		#self.tabsList.remove(self.tabsList[ind]);
		#self.checkLength();
		logger.error("NotImplementedError: DefaultTabbedArea.removeTabWithIndex is not implemented yet.");

	def checkLength(self):
		length = 0;
		for tab in self.tabsList:
			length += len(tab);

		w = length * self.pixelPerChar + len(self.tabsList) * self.padding 	# Assuming 3 pixels per char 
															# and 5 pixels padding between 2 tabs

		if w > self.getWidth():
			# Calculate how much space per tab is okay:
			tabLen = int( ( ( self.getWidth() - (len(self.tabsList) * self.padding)) / len(self.tabsList) )  / self.pixelPerChar );
			newDict = OrderedDict();
			# Shorten the tab strings!
			for tabStr in self.tabsList:
				# Now the hacky part:
				tab = self.tabsList[tabStr];
				newStr = tabStr[:tabLen];
				newDict[newStr] = tab;
				glass.GlassTabbedArea.removeTab(self, tab);
			# If we have sucessfully removed all tabs, add them again!

			for tab in newDict:
				glass.GlassTabbedArea.addTab(self, tab, newDict[tab]);
			self.tabsList = newDict;
				

# (c) 2010 savagerebirth.com
# A subclass of GlassTablePlus, but with LISTS
#TODO setAlignment, just like GTP, should be trivial

import glass;

class GlassListPlus( GlassRowStack, glass.GlassListBox ):
	def __init__(self):
		GlassRowStack.__init__(self, glass.GlassListBox);
		self.setBackgroundColor(transparency);
	
	_add = glass.GlassListBox.addWidgetItem;

	def getItem(self, i, j):
		return str(self.getWidgetItem(i, glass.GlassRow).getColumn(j).getContent(glass.GlassLabel));

	#override to clean up held references to widgets that are gone
	def erase(self):
		glass.GlassListBox.erase(self);
		self.clear();
	
	def adjustWidthToPct(self, widthpct):
		height = self.getHeight();
		self.setSizePct(widthpct, 0);
		self.setHeight(height);
		self.adjustWidthTo(self.getWidth());
	
	def adjustWidthTo(self, targetWidth):
		#move all cells to the LHS, and remove all padding
		self.adjustSize();
		
		#determine how we need to scale everything
		sf = targetWidth / float(self.getWidth());
		if sf < 1:
			con_dprintln("^yWarning ^wGlassListPlus being compressed: this may produce dodgy GUI\n");
		self.setWidth(targetWidth);
		
		#finally re-position everything
		for rownum, row in enumerate(self):
			row.setWidth(targetWidth);
			for cell in self.iterrow(rownum):
				cell.setX( int(cell.getX() * sf));

# (c) 2010 savagerebirth.com
# A subclass of GlassTablePlus, but with LISTS
#TODO setAlignment, just like GTP, should be trivial

import glass;

class DefaultTableList( DefaultRowStack, glass.GlassListBox ):
	def __init__(self):
		DefaultRowStack.__init__(self, glass.GlassListBox);
		self.setBackgroundColor(transparency);
	
	_add = glass.GlassListBox.addWidgetItem;

	def getItem(self, i, j):
		return str(self.getWidgetItem(i, glass.GlassRow).getColumn(j).getContent(glass.GlassLabel));

	#override to clean up held references to widgets that are gone
	def erase(self):
		glass.GlassListBox.erase(self);
		self.clear();
	
	#this is so hacky	
	def adjustWidthToPct(self, widthpct):
		height = self.getHeight();
		self.setSizePct(widthpct, 0);
		self.setHeight(height);
		self.adjustWidthTo(self.getWidth());
	
	def adjustWidthTo(self, targetWidth):
		#move all cells to the LHS, and remove all padding
		self.adjustSize();
		colnum = self.getColumnCount() if self.getColumnCount()>0 else 1

		dw = (targetWidth - self.getWidth())//colnum;
	
		self.setWidth(targetWidth);	
		#finally re-position everything
		for rownum, row in enumerate(self):
			row.setWidth(targetWidth);
			for cell in self.iterrow(rownum):
				cell.setX( cell.getX() + dw);
				cell.setWidth(cell.getWidth() + dw);


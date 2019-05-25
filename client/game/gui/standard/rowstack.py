import glass;

class DefaultRowStack:
	def __init__(self, othercls):
		self.parentcls = othercls;
		othercls.__init__(self);
		self.rows = [];
		self.autoAdjust = True;
	
	def add( self, *dummyargs):
		raise AttributeError("Don't add rows manually, use addRow()"); 
	
	def _add(self, *dummyargs):
		#To be overloaded
		raise NotImplementedError("_add needs to be defined"); 
	
	def addRow( self, *inputs):
		row = glass.GlassRow();
		for widget in inputs:
			if isinstance(widget,(str,unicode)):
				widget = glass.GlassLabel(str(widget));
			row.add( widget );
		self._add(row);
		self.rows.append(row);
		if self.autoAdjust:
			self.adjustSize();
		return row;
	
	def clear(self):
		self.parentcls.clear(self);
		self.rows = [];
	
	def getRowCount(self):
		return len(self.rows);
	
	def getColumnCount(self):
		try:
			return max(row.getColumnCount() for row in self);
		except ValueError:
			return 0;
		
	def __iter__(self):
		return (row for row in self.rows);
	
	def iterrow(self, rowIndex):
		#iterates over the cells in a row
		row = self.rows[rowIndex];
		for j in xrange(row.getColumnCount()):
			yield row.getColumn(j);
	
	def itercol(self, colIndex):
		#iterates over the cells in a column
		for row in self.rows:
			yield row.getColumn(colIndex) if colIndex < row.getColumnCount() else None;
	
	def getCell(self, i, j):
		return self.rows[i].getColumn(j);
	
	def getWidget(self, i, j):
		return self.getCell(i, j).getContent();
	
	def adjustSize(self):
		#shrink to the smallest size possible
		y = 0;
		for rownum, row in enumerate(self):
			x = 0;
			height = 0;
			for cell in self.iterrow(rownum):
				widget = cell.getContent();
				widget.setPosition(0,0);
				width = widget.getWidth();
				height = max(height, widget.getHeight());
				cell.setX(x);
				cell.setSize(width, widget.getHeight());
				x += width;
			for cell in self.iterrow(rownum):
				cell.setHeight(height);
			row.setHeight(height);
			y += height;
		
		#now align all the columns
		x = 0;
		for colnum in xrange(self.getColumnCount()):
			width = 0;
			for cell in self.itercol(colnum):
				if cell == None:
					continue;
				cell.setX(x);
				width = max(width, cell.getWidth());
			x += width;
			for rownum, cell in enumerate(self.itercol(colnum)):
				if cell == None:
					continue;
				cell.setWidth(width);
				self.rows[rownum].setWidth(x);
		self.setSize(x, y);

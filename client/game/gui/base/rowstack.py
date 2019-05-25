
import tools;

class DefaultRowStack:
	def __init__(self, othercls):
		self.parentcls = othercls;
		othercls.__init__(self);
		
		self.rows = [];
		self.currentRow = None;
		self.columnDividers = False;
		self.alternateColumns = 0;
		self.padding = 5;
		self.autoAdjust = False;
		
	def getRowId(self, row):
		return self.rows[row].getId();
	
	def addIdToRow(self, id):
		self.currentRow.setUniqueId = id;

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

		if self.columnDividers:
			for i in xrange(self.getColumnCount()):
				cell = row.getColumn(i);
				cell.useFrame(0,1,0,0);

		row.setAlternate(self.alternateColumns);
		return row;
	
	# Start a new row, any widgets added with self.add will go into this row until nextRow is called again
	def nextRow(self, *widgets):
		
		self.currentRow = glass.GlassRow();
		self.rows.append(self.currentRow);
		
		for widget in widgets:
			self.add(widget);
		
		self._add(self.currentRow);
		
		return self.currentRow;
	
	def setPadding(self, padding):
		for row in self.rows:
			row.setpadding(padding);
			
		self.padding = padding;

	def useColumnDividers(self):
		self.columnDividers = True;
	
		for i in xrange(self.getColumnCount()-1):
			for cell in self.itercol(i):
				cell.useFrame(0,1,0,0);

	def setAlternateColor(self):
		self.alternateColumns = 1;
		for row in self.rows:
			row.setAlternate(1);

	# Adding a widget to the current row
	def add(self, widget):
		if self.currentRow is None:
			self.nextRow();
			
		if isinstance(widget,(str,unicode)):
			widget = glass.GlassLabel(str(widget));
		return self.currentRow.add(widget);

	def _add(self, *dummyargs):
		#To be overloaded
		raise NotImplementedError("_add needs to be defined"); 
	
	def clear(self):
		self.parentcls.clear(self);
		self.rows = [];
	
	def getRowCount(self):
		return len(self.rows);
	
	def getColumnCount(self):
		try:
			return max(row.getColumnCount() for row in self.rows);
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

	def getWidgetTyped(self, i, j, type):
		return self.getCell(i, j).getContentTyped(type);

	def setColumnWidth(self, c, w):
		for row in self:
			col = row.getColumn(c);
			if col != None:
				col.setWidth(w);
			else:
				con_println("^yTrying to set column width of a column that has columnspan!\n")
	
	def adjustSize(self):
		
		y = 0;
		widths = [0] * self.getColumnCount();

		for rownum, row in enumerate(self):
			x = 0;
			height = 5;
			for cnum,cell in enumerate(self.iterrow(rownum)):
				height = max(height, cell.getHeight());
				widths[cnum] = max(widths[cnum], cell.getWidth()/cell.getColumnSpan());

			for cell in self.iterrow(rownum):
				cell.setHeight(height);
			row.setHeight(height);
			y += height;
		
		#now align all the columns
		for rownum, row in enumerate(self):
			col = 0;
			while col < row.getColumnCount():
				cell = row.getColumn(col);
				cell.setX(sum(widths[0:col])); 
				cell.setWidth(sum(widths[col:col+cell.getColumnSpan()]));
				col += cell.getColumnSpan();

		self.setSize(sum(widths), y);
 

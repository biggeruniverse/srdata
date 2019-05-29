# (c) 2011 savagerebirth.com
# A subclass of GlassTable, to make life a little easier

import glass;
from silverback import *;

class DefaultTable(DefaultRowStack, glass.GlassTable):
    TOP = 0;
    CENTER = 1;
    BOTTOM = 2;
    
    def __init__(self):
        DefaultRowStack.__init__(self, glass.GlassTable);
        
        self.autoAdjust = True;
        self.stretchWidgets = False;
        self.horizontalJustification = glass.Graphics.CENTER;
        self.verticalJustification = self.CENTER;

        self.padding = 4;
    
    _add = glass.GlassTable.add;
    
    def getWidget(self, row, col, type=None):
        if type is None:
            return self.getCell(row, col).getContent();
        else:
            return self.getCell(row, col).getContent(type);
    
    def addRow( self, *inputWidgets):
        row = DefaultRowStack.addRow(self, *inputWidgets);
        if self.autoAdjust:
            self.adjustJustification();
        for j in range(row.getColumnCount()):
            cell = row.getColumn(j);
            cell.setAlignment(self.horizontalJustification);
        return row;
    
    def makeBlank( self):
        self.setBackgroundColor(transparency);
        self.setOpaque(False);
        self.setFrame(False);
        self.setAlternate(False);

    #override to clean up held references to widgets that are gone
    def erase(self):
        glass.GlassTable.erase(self);
        self.clear();
    
    def setCellPadding(self, padding):
        self.padding = padding;

    adjustSize = glass.GlassTable.adjustSize;

    def adjustWidthTo(self, width):
        self.adjustSizeTo(width, None);
    
    def adjustHeightTo(self, height):
        self.adjustSizeTo(None, height);
    
    def adjustSizeToPct(self, wpct, hpct):
        self.setSizePct(wpct, hpct);
        self.adjustSizeTo( self.getWidth(), self.getHeight() );
    
    def adjustSizeTo( self, targetWidth=None, targetHeight=None):
        #move all cells to the LHS, and remove all padding
        self.adjustSize();
        if targetWidth is None:
            targetWidth =  self.getWidth()  + (self.getColumnCount()+1)*self.padding;
        if targetHeight is None:
            targetHeight = self.getHeight() + (self.getRowCount()   +1)*self.padding;
        freeWidth  = targetWidth  - (1+self.getColumnCount())*self.padding;
        freeHeight = targetHeight - (1+self.getRowCount()   )*self.padding;
        sfx = freeWidth / float ( self.getWidth() );
        sfy = freeHeight / float( self.getHeight());
        
        #determine how we need to scale everything
        if sfx < 1 or sfy < 1:
            con_println("^yWarning ^wDefaultTable can't be compressed.\n");
            con_println("Scale Factors were "+ str(round(sfx,2)) +", "+ str(round(sfy, 2))+"\n");
            return False;
        self.setSize(targetWidth, targetHeight);
        
        y = self.padding;
        for rownum, row in enumerate(self):
            rh = int(row.getHeight() *sfy) + self.padding;
            
            x = self.padding;
            for colnum, cell in enumerate(self.iterrow(rownum)):
                if cell == None:
                    continue;
                cell.setX( x );
                cw = int( cell.getWidth()*sfx );
                cell.setSize(cw, rh);
                if self.stretchWidgets:
                    widget = cell.getContent();
                    widget.setSize(cw, rh);
                x += cw + self.padding;
            
            row.setSize(targetWidth, rh);
            row.setY( y );
            y += rh;
        
        if self.autoAdjust:
            self.adjustJustification();
        
    def adjustJustification(self):
        for rownum, row in enumerate(self):
            for cell in self.iterrow(rownum):
                widget = cell.getContent();
                cw, ch = cell.getWidth(), cell.getHeight();
                ww, wh = widget.getWidth(), widget.getHeight();
                if self.horizontalJustification == glass.Graphics.LEFT:
                    widget.setX(0);
                elif self.horizontalJustification == glass.Graphics.CENTER:
                    widget.setX((cw - ww)//2);
                elif self.horizontalJustification == glass.Graphics.RIGHT:
                    widget.setX(cw - ww);
                
                if self.verticalJustification == self.TOP:
                    widget.setY(0);
                elif self.verticalJustification == self.CENTER:
                    widget.setY((ch - wh)//2);
                elif self.verticalJustification == self.BOTTOM:
                    widget.setY(ch - wh);

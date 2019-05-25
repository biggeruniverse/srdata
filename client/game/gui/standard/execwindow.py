# (c) 2010 savagerebirth.com
# this file makes windows for executing python in-game


class ExecWindow(glass.GlassWindow):
	def __init__(self):
		glass.GlassWindow.__init__(self);
		self.setCaption("Python Executor");
		self.setSize(400, 250);
		self.setVisible(0);
		self.setPosition(50, 50);
		self.setBackgroundColor(glass.Color(0, 0, 0));
		self.inputfield = glass.GlassTextBox('con_println("\\n");');
		self.inputfield.setLineWrap(0);
		self.inputfield.setId('msg');
		self.inputfield.setSize(480, 180);
		self.inputfield.setOpaque(0);
		self.inputfield.setForegroundColor(white);
		self.inputfield.setFadeBottom(0);
		self.inputfield.setFadeTop(0);
		scroll = glass.GlassScrollArea(self.inputfield);
		scroll.setSize(480,180);
		scroll.setBackgroundColor(glass.Color(200,200,200));
		self.add(scroll, 10, 10);
		evalbutton = glass.GlassButton("Execute it!")
		evalbutton.setClickAction("execwindow.window.execContent();");
		self.add(evalbutton, 10, 200);
		closebutton = glass.GlassButton("Close")
		closebutton.setClickAction("execwindow.hideAllWindows();");
		self.add(closebutton, 330, 200);
		
		
	def execContent(self):
		text = [];
		for rownumber in range(self.inputfield.getNumberOfRows()):
			text.append( execwindow.window.inputfield.getTextRow(rownumber) );
		text = "\n".join(text);
		exec(text)
	
window = ExecWindow();

#show = glass.GlassButton("Python Executor");
#show.setPosition(screenWidth-show.getWidth(),screenHeight-show.getHeight());
#show.setClickAction("execwindow.showAllWindows();")



def newExecWindow( screen ):
	glass.GUI_ScreenAddWidget( screen, execwindow.window );
	#glass.GUI_ScreenAddWidget( screen, execwindow.show );

def hideAllWindows():
	execwindow.window.setVisible(0);

def showAllWindows():
	execwindow.window.setVisible(1);
	execwindow.window.inputfield.requestFocus();

"""
NB THIS WONT WORK WELL IF YOU MAKE MORE THAN ONE newExecWindow()

[17:33] <@BEARD> if I add my window to one screen - everything's fine
[17:33] <@BEARD> add it to two, and it... sort of works
[17:34] <@BEARD> but if I click it, or try to interact with it:
[17:34] <@BEARD> ^rGUI Exception: No focushandler set (did you add the widget to the gui?).
[17:36] <@BEARD> sorry, that's the button that I clicked that caused that

see trac http://dev.savagerebirth.com/trac/ticket/67

"""

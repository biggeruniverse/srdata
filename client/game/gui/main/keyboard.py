#(c) 2011 savagerebirth.com

class KeyboardWindow(DefaultWindow):
	SPACER = 1;
	KEYS_QWERTY = ['Esc',SPACER,'F1','F2','F3','F4',SPACER,'F5','F6','F7','F8',SPACER,'F9','F10','F11','F12',None,SPACER,None,None,None,SPACER,None,'PS','SL','Br','~','1','2','3','4','5','6','7','8','9','0','-','=','Backsp',SPACER,'Ins','Home','PgUp',SPACER,'NL', '/','*','-','Tab','Q','W','E','R','T','Y','U','I','O','P','[',']',"\\",SPACER,'Del','End','PgDn',SPACER,'7','8','9','+'];

	def __init__(self):
		pass;

	def update(self):
		pass;

	def build(self, set, mapping):
		x=0;
		y=20;
		for key in KEYS_QWERTY:
			if key is None:
				x+=32;
				continue;
			if key is SPACER:
				x+=16;
				continue;
			b = DefaultButton(key);
			b.addMouseListener(self);

			self.add(b, x,y);

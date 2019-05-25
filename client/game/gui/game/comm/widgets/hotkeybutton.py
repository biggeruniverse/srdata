# (c) 2012 savagerebirth.com

class HotKeyButton(DefaultWindow):
	BGIMAGE="gui/game/comm/hotkey.png"
	BGIMAGE="gui/game/images/transparent.s2g" # TODO
	def __init__(self, action, img):
		DefaultWindow.__init__(self)
		self.setFrameStyle("TrimmedEight")
		#self.setSize(int(screenHeight*0.0625),int(screenHeight*0.0625))
		self.name = action
		self.actor = None

		self.bg = DefaultLabel()
		self.bg.setImage(self.BGIMAGE)
		self.add(self.bg)
		self.bg.setSizePct(1,1)

		self.image = DefaultLabel()
		self.image.setImage(img)
		self.add(self.image)
		self.image.setSizePct(1,1)

		self.hotkey = getHotkeyForAction(action).capitalize()
		self.hotkeyLabel = DefaultLabel(self.hotkey)
		self.hotkeyLabel.setFont(fontSizeSmall)
		self.hotkeyLabel.setForegroundColor(tangoGreenLight)
		l = self.hotkeyLabel
		self.add(l, self.getWidth()-l.getWidth()-5, self.getHeight()-l.getHeight()-5)

		self.button = glass.ImageButton()
		self.button.setImage("gui/game/images/transparent.s2g")
		self.add(self.button)
		self.button.setId(action)
		self.button.setActionEventId(action)
		self.button.setSizePct(1,1)
		#self.button.setToolTip(self.name)
		
	def addActionListener(self, l):
		self.actor = l
		self.button.addActionListener(l)

	def activate(self):
		e = glass.ActionEvent(self, self.name)
		try:
			self.actor.actionResponse(e)
		except KeyError:
			pass;

	def setEnabled(self, b):
		DefaultWindow.setEnabled(self, b);
		self.button.setEnabled(b);
		# TODO: Disable hotkeys too

	def setForegroundColor(self, c):
		DefaultWindow.setForegroundColor(self, c);
		self.image.setForegroundColor(c);

	def setSize(self, w, h):
		DefaultContainer.setSize(self, w, h)
		self.button.setSizePct(1,1)
		self.image.setSizePct(1,1)
		self.bg.setSizePct(1,1)
		self.hotkeyLabel.setPosition(self.getWidth()-self.hotkeyLabel.getWidth(), self.getHeight()-self.hotkeyLabel.getHeight())


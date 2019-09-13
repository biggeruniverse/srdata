# (c) 2013 savagerebirth.com

import glass
import savage

class FocusIndicator(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self)

		self.maxSize = screenHeightPct(.25)
		self.images = [];
		self.csize=16;

		for i in range(4):
			img = DefaultImage()
			img.setImage("/game/images/reticle"+str(i)+".png", "gui")
			img.setSize(self.csize, self.csize)
			self.images.append(img)
			self.add(img)

	def update(self):
		player = savage.getLocalPlayer()
		w = player.getInventorySlot(player.getCurrentInventorySlotIndex())
		fp = 1.0

		if w is not None:
			fp = w.getValue("focusPenalty")
		f = player.getFocus()+fp
		f = 1.0-f

		if fp < 1.0:
			self.setVisible(True)
			d = self.csize*2+16
			self.setSize(int(self.maxSize*f)+d, int(self.maxSize*f)+d)

			self.setPosition(screenWidthPct(.5)-self.getWidth()//2, screenHeightPct(.5)-self.getHeight()//2+2)
			self.images[1].setPosition(self.getWidth()-self.csize, 0)
			self.images[2].setPosition(self.getWidth()-self.csize, self.getHeight()-self.csize)
			self.images[3].setPosition(0, self.getHeight()-self.csize)
		else:
			self.setVisible(False)


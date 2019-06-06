# (c) 2013 savagerebirth.com

import savage;
import glass;

class DirectionalIndicator(DefaultContainer):
	RADIUS=30
	def __init__(self):
		DefaultContainer.__init__(self)
		self.target = None

		self.setSize(screenHeightPct(.4),screenHeightPct(.4)) 
		self.RADIUS = screenHeightPct(.1290625)

		self.setVisible(False)
		self.fader = None
		self.indicatorImage = DefaultImage()
		self.indicatorImage.setImage("game/images/hit_indicator.png", "gui")
		self.indicatorImage.setForegroundColor(tangoRed);

		self.add(self.indicatorImage)
		self.indicatorImage.setSizePct(.6, .6)

		#hack
		#self.setBackgroundColor(tangoGreen)
		#self.setAlpha(255)
		#self.setVisible(True)
		#self.target = savage.getGameObject(166)

	def makeVisible(self):
		if self.fader is not None:
			self.fader.stop()
			self.fader = None
		self.setAlpha(255)
		self.setVisible(True)
		self.fader = ActionSequence(savage.WaitAction(2000), FadeOutAction(self))
	
	def makeInvisible(self):
		self.setAlpha(0)

	def setTarget(self, o):
		self.target = o
		self.makeVisible()

	def update(self):
		x,y = 0,0

		self.indicatorImage.setPosition(self.getWidth()//2-self.indicatorImage.getWidth()-2, 0)

		if self.target is not None:
			player = savage.getLocalPlayer()
			a = player.getAzimuthTo(self.target)

			angle = math.pi-a;
		
			x = math.sin(angle)*self.RADIUS+self.getWidth()/2
			y = math.cos(angle)*self.RADIUS+self.getHeight()/2

			self.indicatorImage.setPosition(int(x-self.indicatorImage.getWidth()/2), int(y-self.indicatorImage.getHeight()/2))
			self.indicatorImage.setRotation(a)


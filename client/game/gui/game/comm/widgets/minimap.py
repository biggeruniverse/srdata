
from silverback import *;
import glass;
import savage;

class CommMiniMap(DefaultContainer):
	
	def __init__(self):
		DefaultContainer.__init__(self);
		#self.setFrameStyle("Shadow");

		self.minimap = glass.GlassMiniMap();
		self.minimap.setSize(screenHeightPct(.25), screenHeightPct(.25));
		self.minimap.addMouseListener(self);
		self.add(self.minimap, 2, 12);

		self.setBackgroundColor( glass.Color(0,0,0,128));
		
		self.color = DefaultLabel();
		self.color.setImage("/gui/game/images/colorbar.tga");
		self.color.setSize(self.minimap.getWidth(), 10);
		self.color.addMouseListener(self);
		self.add(self.color, 2, 2);

		self.clear = DefaultImageButton();
		self.clear.setImage("canceltr.s2g");
		self.clear.setSize(16,16);
		self.clear.setClickAction("CL_MinimapClear()");
		self.add(self.clear, self.minimap.getWidth()+2, 12);
		
		self.hue = 0.0;
		self.val = 1.0;

		self.fit();
		self.setPosition(1, screenHeight - (self.getHeight()+1));

	def rebuild(self):
		self.minimap.setMap(cvar_get("world_overhead"));
		
	def onMouseClick(self, e):
		if e.widget == self.color:
			return;

		if e.button == MOUSE_LEFTBUTTON:
			w = e.widget.getWidth();
			h = e.widget.getHeight();

			wsize = World_GetGridSize()*100;

			mapx, mapy, z = savage.getLocalPlayer().getPosition();

			mapx = (e.x / float(w)) * wsize;
			mapy = wsize - (e.y / float(h)) * wsize;

			savage.getLocalPlayer().setPosition(Vec3(mapx, mapy, z));

	def onMouseMotion(self, e):
		pass;
	
	def onMousePress(self, e):
		w = e.widget.getWidth();
		h = e.widget.getHeight();
		x = e.x;
		y = e.y;

		if e.widget == self.color:
			return;

		wsize = World_GetGridSize()*100;

		x = int((x/float(w))*wsize);
		y = int((y/float(h))*wsize);

		if e.button == MOUSE_RIGHTBUTTON:
			CL_MinimapStartDraw(x,y,self.hue,self.val);
	
	def onMouseReleased(self, e):
		if e.widget == self.color:
			return;

		if e.button == MOUSE_RIGHTBUTTON:
			self.onMouseDrag(e);
			CL_MinimapEndDraw();
	
	def onMouseDrag(self, e):
		w = e.widget.getWidth();
		h = e.widget.getHeight();
		x = e.x;
		y = e.y;
		
		if e.widget == self.color:
			self.hue = x/float(w);
			self.val = 1.0-(y/float(h));
			return;
		
		wsize = World_GetGridSize()*100;

		x = int((x/float(w))*wsize);
		y = int((y/float(h))*wsize);

		if e.button == MOUSE_RIGHTBUTTON:
			CL_MinimapAddPoint(x,y,self.hue,self.val);

	def onMouseEnter(self, e):
		pass;
	
	def onMouseExit(self, e):
		pass;
 

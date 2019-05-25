# (c) 2011 savagerebirth.com

class OpenContextAction(GuiAction):
	def __init__(self, obj, x, y):
		self.obj = obj;
		self.x = x;
		self.y = y;
		return GuiAction.__init__(self, None);

	def run(self):
		if Input_IsKeyDown(KEY_MOUSE_RIGHTBUTTON):
			cm = commhud.contextmenu;
			ctx = self.determineContext(self.obj);
			ctx.object = self.obj;
			cm.buildContext( ctx );
			if self.x < cm.RADIUS:
				self.x = cm.RADIUS;
			elif self.x > screenWidth - cm.RADIUS:
				self.x = screenWidth - cm.RADIUS;
			if self.y < cm.RADIUS:
				self.y = cm.RADIUS;
			elif self.y > screenHeight - cm.RADIUS:
				self.y = screenHeight - cm.RADIUS;

			cm.setPosition( self.x-cm.RADIUS , self.y-cm.RADIUS );
			actions = cm.context.getContextActions();
			if len(actions) > 0:
				cm.setAlpha(0);
				cm.open();

	def isDone(self):
		return True;

	def determineContext(self, obj):
		cm = commhud.contextmenu;
		try:
			name = obj.getType().getName() if obj != None else None;
			ctx = commcontexts.contextDict[name];
		except KeyError:
			#if the key doesn't exist, because we haven't defined a context
			ctx = commcontexts.emptycontext;
		return ctx;

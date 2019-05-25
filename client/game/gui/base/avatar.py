#(c) 2012 savagerebirth.com

class Avatar(DefaultImage):
	URL = "http://savagerebirth.com/data/avatars/l/0/"
	QUERY_URL = "http://savagerebirth.com/api/user/"
	CACHE = "/cache/avatars/"
	def __init__(self, uname):
		DefaultImage.__init__(self)
		self.httpHandle = -1
		self.username = uname
		self.setImage("generic_avatar.png")
		self.userId = -1

		gblEventHandler.addHttpListener(self)
		self.update()

	def setUser(self, uname):
		self.username = uname
		self.userId = -1
		self.update()

	def update(self):
		if self.httpHandle != -1 or self.username is None:
			return
		if self.userId == -1:
			if cvar_get("auth_sessionid") != "":
				self.httpHandle = HTTP_Get(self.QUERY_URL+self.username)
		else:
			self.checkFileAndLoad()

	def onEvent(self, e):
		if e.handle == self.httpHandle:
			if self.userId == -1:
				dom = xml.dom.minidom.parseString(e.responseMessage);
				#TODO
			else:
				self.setImage("../../../cache/avatars/"+str(self.userId)+".jpg")
			self.httpHandle = -1

	def setImage(self, img):
		w = self.getWidth()
		h = self.getHeight()
		DefaultImage.setImage(self, img)
		self.setSize(w,h)
		

	def checkFileAndLoad(self):
		fn = "../../../cache/avatars/"+str(self.userId)+".jpg"
		if File_Exists(fn):
			#TODO: update cache if too old
			self.setImage(fn)
		else:
			self.httpHandle = HTTP_GetFile(self.URL+str(self.userId)+".jpg", self.CACHE+str(self.userId)+".jpg")
			

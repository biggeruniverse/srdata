# (c) 2011 savagerebirth.com
#
# Handle authentication of a user, let them know the results and set any requiste cvars

import xml.dom.minidom;
from silverback import *;
import savage;

def handleAuthXML(auth):
	sessIdNode = auth.getElementsByTagName("session")[0];

	cvar_set("auth_sessionid", sessIdNode.getAttribute("id"));
	
class AuthWindow(glass.GlassWindow):
	def __init__(self):
		glass.GlassWindow.__init__(self, "Login");
		self.httpHandle = -1;
		self.status=0;

		self.setSize(300, 150);

		lbl = glass.GlassLabel("Username");
		self.add(lbl, 10, 15);
		self.username = glass.GlassTextField("username");
		self.username.setWidthChars(23);
		self.username.setText(cvar_get("username"));
		self.username.setId("username");
		self.username.addKeyListener(self);
		self.add(self.username,100,10);
		lbl = glass.GlassLabel("Password");
		self.add(lbl, 10, 40);
		self.password = glass.GlassTextField("password");
		self.password.setId("password");
		self.password.setWidthChars(23);
		self.password.setHidden(1);
		self.password.setText(cvar_get("password"));
		self.password.addKeyListener(self);
		self.add(self.password,100,35);
		
		auto = glass.GlassCheckbox("Auto Login");
		auto.linkCvar("autologin");
		self.add(auto, 10, 65);
		
		ok = glass.GlassButton("Login");
		self.add(ok, 10, 105);
		ok.addActionListener(self);
		
		cancel = glass.GlassButton("Cancel");
		self.add(cancel, 180, 105);
		cancel.addActionListener(self);
		
		self.setVisible(0);
		gblEventHandler.addHttpListener(self);
	
	def startLogin(self):
		if cvar_get("auth_sessionid") == "":
			self.status=1;
			self.workingWindow(1);
			cvar_set("username", self.username.getText());
			cvar_set("password", self.password.getText());
		
			self.httpHandle = CL_Auth_Authenticate();
	
	def startLogout(self):
		self.status = 0;
		self.httpHandle = CL_Auth_Logout();
		self.workingWindow(1);
	
	def onAction(self, e):
		if e.widget.getCaption() == "Login":
			self.startLogin();
		elif e.widget.getCaption() == "Cancel":
			self.releaseModalFocus();
			self.setVisible(0);
	
	def onEvent(self,e):
		if e.handle == self.httpHandle:
			self.workingWindow(0);
			self.httpHandle = -1;
			
			if len(e.responseMessage)>0 and self.status==1 and e.responseCode == 202:
				cvar_set("auth_sessionid", "");
				
				handleAuthXML(xml.dom.minidom.parseString(e.responseMessage).getElementsByTagName("auth")[0]);
				
				if len(cvar_get("auth_sessionid")) >0:
					self.releaseModalFocus();
					self.setVisible(0);
					cvar_set("name", self.username.getText());
					gblEventHandler.notifyEvent("auth", "", "login");
			else:
				if cvar_get("auth_sessionid") != "":
					cvar_set("auth_sessionid", "");
					gblEventHandler.notifyEvent("auth", "", "logout");
	
	def onKeyPress(self, e):
		if e.key == glass.Key.ENTER:
			self.startLogin();
	def onKeyReleased(self, e):
		pass;


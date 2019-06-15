# (c) 2011-2014 savagerebirth.com

import mainmenu;
from silverback import *;
import glass;
import xml.dom.minidom;
import tools;
import threading;
import socket;
import struct;

class ServerlistSection(AbstractSection):
	
	def __init__(self):
		AbstractSection.__init__(self);
		self.list = DefaultTableList();
	   
		self.lastClickTime = 0;
		self.lastClickSelect = -1;
		self.httpHandle = -1;
		self.listCache = {}
		gblEventHandler.addHttpListener(self);
		gblEventHandler.addSystemListener(self);
		self.list.addMouseListener(self);
		self.list.setSelectionIndicator();
		self.stop = threading.Event();
		self.stop.clear();
		#self.refreshThread = threading.Thread(name="server refresh", target=self._refreshWhenVisible);
		#self.refreshThread.start();
		#self.pingThread = threading.Thread(name="ping refresh", target=self._refreshPingWhenVisible);
		#self.pingThread.start();

	def _refreshWhenVisible(self):
		while not self.stop.is_set():
			if self.isVisible() == True:
				self.refresh();
			stacklesslib.main.sleep(60.0)

	def _refreshPingWhenVisible(self):
		while not self.stop.is_set():
			if self.isVisible() == True:
				self.refreshPings();
			stacklesslib.main.sleep(15.0);
		

	def onShow(self):
		self.refresh();

		if isConnected():
			self.reconnectBar.setVisible(True);
			self.scroll.setY(85);
		else:
			self.reconnectBar.setVisible(False);
			self.scroll.setY(42);
		
	def create(self):
		
		self.setBackgroundColor(windowBackground);
		
		# Top area
		top = DefaultContainer();
		top.setSize(self.getWidth(), 35);
		top.setBackgroundColor(windowTop);
		top.setOpaque(True);
		self.add(top);
		
		refresh = MainIcon("refresh", 17, 17);
		refresh.setCaption("Refresh");
		refresh.addActionListener(self);
		top.add(refresh, 10, "center");
		
		filter = MainIcon("cog", 17, 17);
		top.add(filter, 33, "center");
		
		title = DefaultImage();
		title.setImage("txt_serverbrowser.png");
		top.add(title, "center", "center");
		
		connect = DefaultImageButton();
		connect.setCaption("Connect");
		connect.setImage("btn_connect.png");
		connect.addActionListener(self)
		top.add(connect, 10, "center", "right"); 

		# return to game stuff:

		self.reconnectBar = DefaultContainer();
		self.reconnectBar.setSize(self.getWidth(), 50);
		self.reconnectBar.setVisible(False);
		self.reconnectBar.setBackgroundColor(glass.Color(85, 21, 11));
		self.reconnectBar.setOpaque(True);
		self.add(self.reconnectBar, 0, 35);
		
		gameProgress = DefaultLabel("GAME IN PROGRESS");
		self.reconnectBar.add(gameProgress, "center");
		
		hr = DefaultImage();
		hr.setImage("divider.png");
		self.reconnectBar.add(hr, "center", gameProgress.getHeight() + 3);

		disconnectButton = DefaultButton("LEAVE");
		disconnectButton.setClickAction("""disconnect();mainmenu.modules['menu'].sectionStack['serverlist'].onShow();""");
		self.reconnectBar.add(disconnectButton, 10, 10);

		connectedMessage = DefaultLabel("You are currently connected to a server. Do you want to return?");
		connectedMessage.setFont(fontSizeSmall);
		self.reconnectBar.add(connectedMessage, "center", 27);
		
		returnButton = DefaultButton("RETURN");
		returnButton.setClickAction("spechud.setMode('lobby');GUI_ShowScreen('spechud')");
		self.reconnectBar.add(returnButton, 10, 10, "right");
		
		# The list bro
				
		self.list.padding = 5;
		self.list.setSelectionColor(glass.Color(70, 40, 40, 180));
		self.clearList();
		
		self.scroll = glass.GlassScrollArea(self.list);
		self.scroll.setSize(self.getWidth()-5, self.getHeight()-42);
		self.scroll.setBackgroundColor(transparency);
		self.add(self.scroll, 0, 42);
		
		#self.list.setWidth(self.scroll.getWidth());
		self.list.adjustWidthTo(self.scroll.getWidth()-20);

		self.serverCount = DefaultLabel("Total Servers: 0   "); 
		self.serverCount.setFont(fontSizeSmall);
		self.serverCount.setForegroundColor(tangoGrey3);
		self.add(self.serverCount, 5, 5, "right", "bottom");

		
	def clearList(self):
		self.list.erase();
		
		self.headingRow = self.list.nextRow("", "", "^lName", "^lGame Type", "^lPlayers", "^lMap   ", "^lPing");
		self.headingRow.setId("header");
		#self.headingRow.setBackgroundColor(glass.Color(70, 40, 40, 220));
		self.headingRow.setBaseColor(glass.Color(28,27,23));
		self.headingRow.setFocusable(False);
		
	def refresh(self):
		self.httpHandle = HTTP_Get(ApiUrl + "/serverlist/");
		#now do crappy newerth serverlist...
		f = File_Open("gamelist_full.dat", "rb")
		ip = [192,168,2,1]
		port=11235
		cursor=5
		length = File_Size(f)
		File_Read(f, 5)
		try:
			while cursor < length:
				official = "  ^222[XR]"
				ip[0] = struct.unpack("B", File_Read(f, 1))[0]
				ip[1] = struct.unpack("B", File_Read(f, 1))[0]
				ip[2] = struct.unpack("B", File_Read(f, 1))[0]
				ip[3] = struct.unpack("B", File_Read(f, 1))[0]
				if ip[0] != 0:
					port = struct.unpack("<H", File_Read(f, 2))[0]
				else:
					break
				address = "%d.%d.%d.%d:%d" % (ip[0], ip[1], ip[2], ip[3], port)
				if address not in self.listCache:
					row = self.list.nextRow( "", 
					  official,
					  address,
					  "N/A",
					  "0/0   ",
					  "N/A          ", 
					  "N/A"
					);
					row.setId(address);
					row.setBaseColor(glass.Color(28,27,23));
					row.setForegroundColor(glass.Color(19,13,13)); #used for alternating colors
					self.listCache[address] = row
				Host_GetInfo("%d.%d.%d.%d" % (ip[0], ip[1], ip[2], ip[3]), port)
		finally:
			File_Close(f)

	def _checkPing(self, serverlist):
		for server in serverlist:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
			sock.settimeout(0.1)
			try:
				thetime = Host_Milliseconds();
				host,port = str(server.getId()).split(':');
				#con_println("trying "+host+"...\n");
				#sock.connect((host, int(port)+1));
				data = struct.pack('!LBBL', 0, 5, 0xC6, socket.htonl(thetime));
				sock.sendto(data, (host, int(port)+1));
				msg = ""
				while len(msg) < 10:
					msg += sock.recv(10)
				#msg, addr = sock.recvfrom(10);
				meh, bsize, cmd, senttime = struct.unpack('<LBBL', msg);
				#con_println("ping for "+host+" is "+str(Host_Milliseconds()-senttime)+"\n");
				server.getColumn(6).getContent(glass.GlassLabel).setCaption(str(Host_Milliseconds()-senttime));
			except socket.timeout:
				server.getColumn(6).getContent(glass.GlassLabel).setCaption("999");
				#con_println("ping is >2500ms\n");
			except Exception as e:
				con_println("failed to connect: "+str(e)+"\n");
			#sock.shutdown(socket.SHUT_RDWR);
			sock.close();

	def refreshPings(self):
		threading.Thread(name="pinging thread", target=self._checkPing, args=(self.list,)).start()
			
		
	def onAction(self, e):
		if e.widget.getCaption() == "Refresh":
			self.refresh();   
		elif e.widget.getCaption() == "Connect":
			#XR servers require a different handshake, so it's something we need to know before connecting
			xr = 1 if self.list.getWidget(self.list.getSelected(), 1).getId() == "  ^222[XR]" else 0
			loading.setWorld(self.list.getWidget(self.list.getSelected(), 5).getId());			
			connect(self.list.getRowId(self.list.getSelected()), xr);

	def onEvent(self, e):
		
		if isinstance(e, SystemEvent):
			strings = {"world":"N/A", "gametype":"RTSS", "cnum":"0", "cmax":"0", "world":"eden2"}
			server = self.listCache[e.param1]
			#varlist = e.param2.split('ÿ')
			varlist = e.param2.split(chr(255))
			#con_println(str(e))
			for var in varlist[1:]:
				try:
					#con_println("var is "+str(var)+"\n")
					#name, value = var.split('þ')
					name, value = var.split(chr(254))
					strings[name] = value.strip()
				except Exception as ex:
					con_println(str(ex)+"\n")
					con_println(var+"\n")
			server.getColumn(2).getContent(glass.GlassLabel).setCaption(strings["name"])
			server.getColumn(3).getContent(glass.GlassLabel).setCaption(strings["gametype"])
			server.getColumn(4).getContent(glass.GlassLabel).setCaption(strings["cnum"]+"/"+strings["cmax"]+'    ')
			server.getColumn(5).getContent(glass.GlassLabel).setCaption(strings["world"])
			server.getColumn(5).getContent(glass.GlassLabel).setId(strings["world"])
			self.list.adjustWidthTo(self.scroll.getWidth()-20)
			return
		
		if e.handle == self.httpHandle:
			dom = xml.dom.minidom.parseString('<?xml version="1.0" encoding="UTF-8"?><_/>')	
			#self.clearList();
			self.httpHandle = -1;
			if e.responseCode != 404:
				dom = xml.dom.minidom.parseString(e.responseMessage);

			if len(dom.getElementsByTagName("servers")) > 0:
				servers = dom.getElementsByTagName("servers")[0];
				list = servers.getElementsByTagName("server");
				for server in list:
					official = "";
					if server.getAttribute("official") == "1":
						official = "^icon shield^";
					if str(server.getAttribute("address")) not in self.listCache:						
						row = self.list.nextRow( "", 
						  official,
						  server.getAttribute("name"),
						  server.getAttribute("map_type"),
						  server.getAttribute("num_players")+"/"+server.getAttribute("max_players"),
						  server.getAttribute("map_name"), 
						  "N/A"
						);
						row.setId(str(server.getAttribute("address")));
						row.setBaseColor(glass.Color(28,27,23));
						row.setForegroundColor(glass.Color(19,13,13)); #used for alternating colors
						self.listCache[str(server.getAttribute("address"))] = row
					else:
						row = self.listCache[str(server.getAttribute("address"))]
						row.getColumn(1).getContent(glass.GlassLabel).setCaption(official)
						row.getColumn(2).getContent(glass.GlassLabel).setCaption(server.getAttribute("name"))
						row.getColumn(3).getContent(glass.GlassLabel).setCaption(server.getAttribute("map_type"))
						row.getColumn(4).getContent(glass.GlassLabel).setCaption(server.getAttribute("num_players")+"/"+server.getAttribute("max_players"))
						row.getColumn(5).getContent(glass.GlassLabel).setCaption(server.getAttribute("map_name"))
			dom.unlink();


			self.list.useColumnDividers();
			self.list.setAlternateColor();
			self.headingRow.setAlternate(False);

			self.serverCount.setCaption("Total Servers: " + str(self.list.getRowCount()-1));

			#self.list.adjustSize();
			self.list.adjustWidthTo(self.scroll.getWidth()-10);
			#in case you need it later -serverlist.scr.getScrollbarWidth());
			HTTP_GetFile("http://masterserver.newerth.com/gamelist_full.dat", "gamelist_full.dat");
			
			

	def onMousePress(self, e):
		pass; 
		
	def onMouseReleased(self, e):
		pass; 
		
	def onMouseClick(self, e):
		if self.lastClickTime + 500 >= Host_Milliseconds() and self.list.getSelected() == self.lastClickSelect:
			loading.setWorld(self.list.getWidget(self.list.getSelected(), 5).getId());
			connect(self.list.getRowId(self.list.getSelected()));
		self.lastClickTime = Host_Milliseconds();
		self.lastClickSelect = self.list.getSelected();
	
mainmenu.modules["menu"].addSection("serverlist", ServerlistSection());

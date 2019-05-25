# (c) 2011 savagerebirth.com
import glass;
import xml;

#TODO ^icon loading^ animation
#TODO refresh button

def frame():
	serverlist.m.moveLabel();

def onShow():
	serverlist.m.getMotd();
	serverlist.httpHandle = HTTP_Get("http://savagerebirth.com/api/index.php/serverlist/");

class ServerListHandler:
	def __init__(self):
		pass;

	def onEvent(self, e):
		if e.handle == serverlist.httpHandle:
			serverlist.list.erase();
			serverlist.httpHandle = -1;
			servers = xml.dom.minidom.parseString(e.responseMessage).getElementsByTagName("servers")[0];
			list = servers.getElementsByTagName("server");
			for server in list:
				official = "";
				if server.getAttribute("official") == "1":
					official = "^icon shield^";
				serverlist.list.addRow(
				  server.getAttribute("name"),
				  server.getAttribute("address"),
				  server.getAttribute("num_players")+"/"+server.getAttribute("max_players"),
				  server.getAttribute("map_name"),
				  official
				);
				
			serverlist.list.adjustWidthTo(serverlist.scr.getWidth());
			#in case you need it later -serverlist.scr.getScrollbarWidth());

glass.GUI_CreateScreen("serverlist");

httpHandle = -1;
gblEventHandler.addHttpListener(ServerListHandler());

#build the viewer background
v = glass.GlassViewer();
v.showWorld(1);
v.setOpaque(0);
v.setEnabled(0);
v.setSizePct(1,.80);
v.setPositionPct(0,0);
v.setCameraPosition(4720,1830,297);
v.setCameraTarget(100,500,550);

glass.GUI_ScreenAddWidget("serverlist", v);

l = glass.GlassLabel();
l.setImage("/gui/standard/maintitle.png");
l.setSizePct(1,1);
glass.GUI_ScreenAddWidget("serverlist", l);

topstatus = GlassTopStatusBar();
glass.GUI_ScreenAddWidget("serverlist", topstatus);
gblEventHandler.addNotifyListener(topstatus);

#window
w = glass.GlassWindow("list");
w.setBackgroundColor(glass.Color(0,0,0,128));
w.setSizePct(.8,.35);
w.setPositionPct(0.1,0.325);
w.setTitleVisible(0);

glass.GUI_ScreenAddWidget("serverlist", w);

list = GlassListPlus();
scr = glass.GlassScrollArea(list);
w.add(scr);
scr.setSizePct(1, .8);

back = glass.GlassButton("Back");
w.add(back);
back.setClickAction("GUI_ShowScreen('mainmenu')");
back.setPositionPct(.10, .0);
back.setY( w.getHeight() - back.getHeight() - 5);

host = glass.GlassButton("Host Server");
w.add(host);
host.setClickAction("serverlist.hostServerWindow.showHostServerWindow()");
host.setPositionPct(0.6,0);
host.setY( w.getHeight() - host.getHeight() - 5);

connect = glass.GlassButton("Connect");
w.add(connect);
connect.setClickAction("connect(serverlist.list.getItem(serverlist.list.getSelected(), 1))");
connect.setPositionPct(0.8,0);
connect.setY( w.getHeight() - connect.getHeight() - 5);

irc = IRCChatBox();
irc.setSizePct(0.8,0.4);
irc.resize();
irc.setPositionPct(0.1,0.55);

#glass.GUI_ScreenAddWidget("serverlist",irc);

#motd#
m = MotdWindow();
m.setY(32);
glass.GUI_ScreenAddWidget("serverlist", m);

## buddies

blist = BuddyListGUI();
blist.setAlignment(glass.Graphics.CENTER);
blist.setPosition(screenWidth/2 - blist.getWidth()/2, screenHeight - blist.getHeight());
glass.GUI_ScreenAddWidget("serverlist",blist);

## "Host a server" window

hostServerWindow = HostServerWindow();
glass.GUI_ScreenAddWidget("serverlist", hostServerWindow);
hostServerWindow.setPositionPct(0.275, 0.25);

from silverback import *;
import logging;
import glass;

logger = logging.getLogger("gui");

class NotificationHandler(DefaultContainer):
	def __init__(self):
		DefaultContainer.__init__(self);
		self.setBackgroundColor(transparency);

		self.width = 327;
		self.setSize(self.width, 0);

		#gblEventHandler.addNotifyListener(self);
		# Let's run notifications through the XMPPHandler too
		gblXMPPHandler.addListener(self);

		#self.notificationQueue = [];

		self.notifications = OrderedDict(); # Not that it would matter...

		#self.maxNotifications = 5 # There will always be max. 6 old notifications,
								  # you can delete them manually tho.

	def insertNotification(self, notificationId, title, msg, command, arg):
		note = Notification(notificationId, title, msg, command, arg);
		#self.notificationQueue.append(note);
		self.notifications[notificationId] = note;
		self.add(note);
		self.update();

	def closeNotification(self, notificationId):
		note = self.notifications.pop(notificationId);
		note.setVisible(False); # Just in case...
		self.remove(note);
		self.update();

	def update(self):
		#if len(self.notificationQueue) > self.maxNotifications:
		#	self.notificationQueue.pop();
		# Rebuild the whole container:

		y = 0;
		self.setSize(self.width, y);

		for notificationId, note in self.notifications.items():			

			note.setVisible(True);
			note.setY(y);
			y += note.getHeight() + 10;

		self.setSize(327, len(self.notifications) * Notification.ACTUAL_HEIGHT);

	def onChatEvent(self, e):

		if e.scope.startswith("notify_"):
			if e.scope == "notify_close":
				self.closeNotification(e.fromstr); #Close the notification that sent the event.
			else:
				self.insertNotification(e.notificationId, e.title, e.string, e.command, e.arg);

		"""
		if e.scope == "notify_muc_invite":
			self.insertNotification("Chatroom Invite", e.fromstr + " invited you to the room " + e.room + "!", e.string, e.room);

		elif e.scope == "notify_friend_request":
			self.insertNotification("Friend Request", e.fromstr + " wants to be your new friend!", e.string, e.fromstr);

		elif e.scope == "notify_friend_accept":
			self.insertNotification("Friend Accepted", "You and " + e.fromstr + " are now friends!");

		elif e.scope == "notify_clan_invite":
			pass;

		elif e.scope == "notify_clan_accept":
			pass;

		elif e.scope == "notify_match_invite":
			self.insertNotification("Match Invite", e.string, e.room, e.fromstr);	

		elif e.scope == "notify_error":
			self.insertNotification(e.fromstr, e.string);

		elif e.scope == "notify_chat_reconnect":
			self.insertNotification(e.fromstr, e.string, e.room);


		elif e.scope == "chat_msg":

			# check if we have the chatwindow open:
			screen = glass.GUI_CurrentScreen()
			if screen == "mainmenu":
				if not glass.GUI_GetScreen(screen).findWidgetById("chat").isVisible():
					# if it's invisible, post a new notification
					command = "mainmenu.topBar.openChat()"
					self.insertNotification("Message received", e.fromstr + " send you a message!", command, "exec");
			elif screen == "hud" or screen == "commhud":
				#command = screen + ".topBar.openChat()"
				#self.insertNotification("Message received", e.fromstr + " send you a message!", command, "exec");
				pass; #todo
		"""


class Notification(DefaultContainer):

	ACTUAL_HEIGHT = 76; #The actual height is different from the one I can set as the framestyle adds a few pixels.

	def __init__(self, notificationId, title, msg, command = None, arg = None):
		DefaultContainer.__init__(self);

		self.notificationId = notificationId;
		self.title = title;
		self.msg = msg;
		self.arg = arg;
		self.command = command;

		self.setSize(327, Notification.ACTUAL_HEIGHT - 10);
		self.setBackgroundColor(transparency);

		content = DefaultWindow();
		content.setBackgroundColor(glass.Color(70, 21, 11, 180));
		content.setSize(300, 50)
		self.add(content, 8, 8);

		left = DefaultWindow();
		left.setBackgroundColor(glass.Color(0,0,0,220));
		self.add(left, 8, 8);
		left.setSize(50, 50);

		pic = DefaultImage();
		pic.setImage("todo.png");
		pic.setSize(left.getHeight(), left.getHeight());
		left.add(pic, 0,0);

		self.titleLabel = DefaultLabel(title);
		content.add(self.titleLabel, left.getWidth() + 10, 0);

		text = DefaultTextBox("");
		text.setSize(content.getWidth() - left.getWidth() - 20, 35);
		text.setBackgroundColor(transparency);
		text.setForegroundColor(glass.Color(211, 201, 168));
		text.setFont(fontSizeSmall);
		text.setEditable(0);
		text.setText(msg);
		content.add(text, self.titleLabel.getX(), 17);

		close = DefaultImageButton();
		close.setImage("icons/decline.png");
		close.setSize(24, 24);
		self.add(close, "right", "center");
		close.setCaption("Close");
		close.addActionListener(self);

		if self.command != None:
			close.setCaption("No");
			close.setY(5);

			accept = DefaultImageButton();
			accept.setImage("icons/accept.png");
			accept.setSize(24, 24);
			self.add(accept, close.getX(), 32);
			accept.setCaption("Yes");
			accept.addActionListener(self);

	def onAction(self, e):
		if e.widget.getCaption() == "Close":
			self.close();

		elif e.widget.getCaption() == "Yes":	

			task = stackless.tasklet(self.command);
			if self.arg != None:
				task.setup(self.arg, True);
			else:
				task.setup(True);
			self.close();		

		elif e.widget.getCaption() == "No":

			task = stackless.tasklet(self.command);
			if arg != None:
				task.setup(self.arg, False);
			else:
				task.setup(False);
			self.close();

	def close(self):
		gblXMPPHandler.chatEvent("notify_close", self.notificationId, self.title);

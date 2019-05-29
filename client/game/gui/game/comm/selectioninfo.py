
from silverback import *;
import savage;
import glass;
import tools;


class SelectionInfo(DefaultContainer):
	
	def __init__(self):
		DefaultContainer.__init__(self);

		self.object = None;
		self.currentSelection = None;

		self.setBackgroundColor( windowCommhud );
		self.setSize(145, 200);
		self.setVisible(False);

		self.name = DefaultLabel("biggeruniverse");
		self.add(self.name, "center" , 5); # center later on

		iconWindow = DefaultWindow();
		iconWindow.setFrameStyle("TrimmedEight");
		iconWindow.setSize(48, 48);
		
		self.icon = DefaultImageButton();
		self.icon.setId("icon");
		self.icon.imagePath = "";
		self.icon.setSize(48,48);
		self.icon.setImage("thiswasatriumph");
		self.icon.addActionListener(self);
		
		iconWindow.add(self.icon);

		self.add(iconWindow, 5, self.name.getHeight() + 8);
		#self.widgets.append(self.icon);

		infoContainer = DefaultContainer();
		infoContainer.setSize(85, 48);
		#infoContainer.setBackgroundColor(white);

		self.add(infoContainer, iconWindow.getWidth() + 8, iconWindow.getY());
		
		hpIcon = DefaultImage();
		hpIcon.setImage("todo.png");
		hpIcon.setSize(14, 14);
		infoContainer.add(hpIcon);

		self.bar = glass.GlassProgressBar();
		self.bar.setBackgroundColor(white);
		self.bar.setForegroundColor(glass.Color(255,21,22, 128));
		#self.bar.setForegroundColor(tools.HSLColor(0.33,0.8,0.66));
		self.bar.setSize(68, 14);
		self.bar.setBackgroundImage("gui/base/images/progress_bg.tga");
		infoContainer.add(self.bar, hpIcon.getWidth() + 2, 0);
		self.bar.setProgress(1);
		
		self.health = DefaultLabel();
		self.health.setCaption("0000/0000");
		self.health.setForegroundColor(glass.Color(255,237,237, 128));
		self.health.setFont(fontSizeSmall);
		infoContainer.add(self.health, "right", self.bar.getY() - 2);

		armorIcon = DefaultImage();
		armorIcon.setImage("todo.png");
		armorIcon.setSize(14, 14);
		infoContainer.add(armorIcon, 0, hpIcon.getHeight() + 2);

		self.armor = DefaultLabel("000 + 00");
		self.armor.setFont(fontSizeSmall);
		self.armor.setForegroundColor(tangoGrey3);
		infoContainer.add(self.armor, "right", armorIcon.getY());

		dmgIcon = DefaultImage(); 
		dmgIcon.setImage("todo.png");
		dmgIcon.setSize(14, 14);
		infoContainer.add(dmgIcon, 0, armorIcon.getY() + armorIcon.getHeight() + 2);

		self.damage = DefaultLabel("000 + 00");
		self.damage.setFont(fontSizeSmall);
		infoContainer.add(self.damage, "right", dmgIcon.getY());

		#self.widgets.append(self.name);

		## wee, inventory!

		self.inventoryWindow = DefaultWindow();
		self.inventoryWindow.setFrameStyle("TrimmedEight");
		self.inventoryWindow.setBackgroundColor(windowCommhud);
		self.inventoryWindow.setSize(self.getWidth() - 10, 32);

		slotSize = (self.inventoryWindow.getWidth() - 8) // 5;

		self.inventoryWindow.setHeight(slotSize);

		self.invSlots = [];

		for i in range(5):
			slot = DefaultImage();
			slot.imagePath = "";
			slot.setImage("gui/game/images/transparent.s2g");
			slot.setBackgroundColor(black);
			slot.setSize(slotSize, slotSize);
			self.inventoryWindow.add(slot, (slotSize + 2)*i);
			self.invSlots.append(slot);

		self.add(self.inventoryWindow, 5, iconWindow.getHeight() + iconWindow.getY() + 5);


		self.setHeight(self.inventoryWindow.getY() + self.inventoryWindow.getHeight() + 5);

	def rebuild(self):
		if self.object == None:
			self.hide();

		self.setVisible(True);
		ot = self.object.getType();
		self.icon.setImage(ot.getValue("icon")+".s2g");
		self.icon.setSize(48, 48);

		self.health.setCaption(str(self.object.getHealth()) + "/" + str(self.object.getMaxHealth()))
		self.health.setX( self.bar.getX() + (self.bar.getWidth() // 2 - self.health.getWidth() // 2) )
		self.bar.setProgress(self.object.getHealthPct());

		self.name.setCaption(ot.getValue("description"));
		self.armor.setVisible(True);
		self.damage.setVisible(True);

		if self.object.isPlayer():
			self.inventoryWindow.setVisible(True);
			self.name.setCaption(self.object.getFormattedName());
			self.updateInventory();

		elif ot.isUnitType():
			self.inventoryWindow.setVisible(False);
		elif ot.isBuildingType():
			self.inventoryWindow.setVisible(False);
		elif ot.isMine():
			self.inventoryWindow.setVisible(False);
			self.armor.setVisible(False);
			self.damage.setVisible(False);

		self.name.setX(self.getWidth() // 2 - self.name.getWidth() // 2);

		#self.armor.setCaption();
		#self.damage.setCaption();

	def updateInventory(self):

		for i in range(5):
			ot = self.object.getInventorySlot( i );
			slot = self.invSlots[i];
			w, h = slot.getWidth() , slot.getHeight();
			
			if ot != None:
				#slot.setVisible(True);
				slot.setImage(ot.getValue("icon")+".s2g");
			
			else: #empty slot
				slot.setImage("gui/game/images/transparent.s2g");
			slot.setSize( w, h);

	def hide(self):
		self.setVisible(False);
		self.object = None;

	def handleSelection(self):
		if self.currentSelection == None:
			self.hide()
			return;
		selectionList = self.currentSelection.list;
		if len(selectionList) == 1:
			self.object = selectionList[0];
			self.rebuild();
		else:
			self.hide();

	def onAction(self, e):
		CL_CenterCamera(int(self.object.getPosition()[0]), int(self.object.getPosition()[1]));


	def onSelection(self, e):
		self.currentSelection = e.selection;
		self.handleSelection();

		"""
		self.addInfo = DefaultContainer();	#Items/Research stuff
		self.addInfo.setSize(130, 28);
		self.addInfo.setBackgroundColor(glass.Color(60, 40, 40, 80));
		self.add(self.addInfo, 100, 60);
		#self.widgets.append(self.addInfo);

		self.items = [];
		for i in range(4):
			img = glass.GlassLabel("");
			img.setVisible(False);			
			img.setSize(24,24);
			self.items.append(img);
			self.addInfo.add(img, i*24+5,3);
		"""
		
	"""	
	def frame(self):
		self.clear(); # Make everything invisible.
		# I'm not sure what I think about the way that commwidget structure does it...
		# There are tons of setVisible() calls every frame in every widget (selection etc)
		for obj in commhud.selectionList:

			self.setPosition(int(obj.getScreenTopPosition()[0]),int(obj.getScreenTopPosition()[1]));
			# Have to position it like this, else it wouldn't be possible to open the contextmenu		
			if obj.getType().isBuildingType() or obj.getType().isWorkerType():

				self.icon.setImage(obj.getIcon());
				self.icon.setSize(80,80);
				self.name.setCaption(obj.getName());

				if obj.isBeingBuilt():
					hp = obj.getBuildProgress();
					value = str(int(hp*100))[:3] + "%";

				else:
					hp = obj.getHealthPct();
					value = str(obj.getHealth());
					i = 0;
					
					for item in savage.getLocalTeam().getResearch():						
						if obj == item.getBuilder():
							self.items[i].setImage(item.getType().getValue("icon")+".s2g");
							self.items[i].setSize(24,24);
							self.items[i].setVisible(True);

				self.setHealth(hp, value);

			elif obj.isPlayer():
				
				self.icon.setImage(obj.getIcon());
				self.icon.setSize(80,80);
				self.name.setCaption(obj.getFormattedName());
				self.setHealth(obj.getHealthPct(), str(obj.getHealth()));

				for i in range(4):
					item = obj.getInventorySlot(i+1);
					if item is not None:
						self.items[i].setImage(item.getValue("icon")+".s2g");
						self.items[i].setSize(24,24);
						self.items[i].setVisible(True);
					else:
						self.items[i].setVisible(False);
	"""


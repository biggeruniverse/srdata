
class InventoryWindow(DefaultContainer):

	def __init__(self):

		DefaultContainer.__init__(self)

		gblEventHandler.addGameListener(self);

		## INVENTORY ##

		self.setSize(screenHeightPct(0.35) + 10, screenHeightPct(0.055) + 10 );

		#self.setFrameStyle("SmallEight");
		self.setBackgroundColor(transparency);

		## AMMO ##

		self.ammoWindow = DefaultWindow();
		self.ammoWindow.setFrameStyle("SmallEight");
		self.ammoWindow.setBackgroundColor(glass.Color(0,0,0,150));
		self.add(self.ammoWindow, 5, 5);
		self.ammoWindow.setSize(self.getHeight() - 10, self.getHeight() - 10)

		self.ammoValue = DefaultLabel("999");
		self.ammoValue.setForegroundColor( white );
		self.ammoValue.setAlignment(2);
		self.ammoWindow.add(self.ammoValue, 0, "top");

		self.ammoGraphic = DefaultLabel();
		self.ammoGraphic.setImage("/gui/standard/icons/comm_crown.s2g");
		self.ammoGraphic.setSize( self.ammoWindow.getHeight() // 2  , self.ammoWindow.getHeight() // 2 );
		self.ammoWindow.add(self.ammoGraphic, "center", "bottom");

		equipmentWindow = DefaultWindow();
		equipmentWindow.setFrameStyle("SmallEight");
		equipmentWindow.setBackgroundColor(glass.Color(0,0,0,128));
		self.add(equipmentWindow, self.ammoWindow.getWidth() + 10, 5);
		equipmentWindow.setSize(self.getWidth() - self.ammoWindow.getWidth() - 15, self.getHeight() - 10);

		slotSize = (equipmentWindow.getWidth() - 12) // 5;
		
		self.inventorySlots = [];
		self.inventoryAmmos = [];
		for i in range(5):
			slot = DefaultLabel();

			slot.setSize( slotSize , slotSize);
			self.inventorySlots.append(slot);
			equipmentWindow.add(slot,2 + i * (slot.getWidth() + 3), "center");
			slot.setVisible(True);

			if i > 0 and i < 4:
				div = DefaultContainer();
				div.setSize(2, self.getHeight() - 4);
				div.setBackgroundColor(glass.Color(0,0,0, 50));
				self.add(div, equipmentWindow.getX() + slot.getX() + slot.getWidth() + 2, 2);


			ammo = DefaultLabel("999");
			ammo.setForegroundColor(white);
			ammo.setAlignment(2);
			ammo.setPosition( slot.getX() + slot.getWidth() - ammo.getWidth() - 1 , slot.getY() + slot.getHeight() - ammo.getHeight() - 1);
			
			self.inventoryAmmos.append(ammo);
			equipmentWindow.add(ammo);

		slot = self.inventorySlots[0];
		self.invselected = DefaultLabel();
		self.invselected.setImage("/gui/game/images/inventory_selected.s2g")
		self.invselected.setSize( slot.getWidth(), slot.getHeight() - 2);
		equipmentWindow.add(self.invselected, slot.getX(), slot.getY());

		

	def onEvent(self, e):
		if e.eventType == "inventory_changed":
			self.buildInventory();
		elif e.eventType == "ammo_changed":
			self.updateAmmo();

	def buildInventory(self):
		
		player = savage.getLocalPlayer();
		self.primaryRanged = None;
		
		for i in range(5):
			slot_objType = player.getInventorySlot( i );
			slot = self.inventorySlots[i];
			w, h = slot.getWidth() , slot.getHeight();
			
			if slot_objType != None:
				slot.setVisible(True);
				slot.setImage(slot_objType.getValue("icon")+".s2g");

				if self.primaryRanged == None and slot_objType.isWeaponType() :
					self.primaryRanged = i;
			
			else: #empty slot
				slot.setVisible(False);
			slot.setSize( w, h);
		
		if self.primaryRanged != None:
			slot_objType = player.getInventorySlot(self.primaryRanged);
			w, h = self.ammoGraphic.getWidth(), self.ammoGraphic.getHeight();
			if slot_objType.isManaWeapon():
				self.ammoGraphic.setImage( "/models/beast/items/icons/manarestore.s2g");
			else: #it must use ammo
				self.ammoGraphic.setImage( "/models/human/weapons/ranged/icons/generic_ammo.s2g" );
			self.ammoGraphic.setSize( w, h);
			#self.ammoValue.setVisible(True);
			#self.ammoGraphic.setVisible(True);
			self.ammoWindow.setVisible(True);
		else:
			#self.ammoValue.setVisible(False);
			#self.ammoGraphic.setVisible(False);
			self.ammoWindow.setVisible(False);

		self.updateAmmo();
		

	def updateSelection(self):
		
		player = savage.getLocalPlayer();
		currentSlotIndex = player.getCurrentInventorySlotIndex();
		slotWidget = self.inventorySlots[ currentSlotIndex ];
		self.invselected.setPosition( slotWidget.getX(), slotWidget.getY() );
	
	def updateAmmo(self):
		
		player = savage.getLocalPlayer();
		for i in range(5):
			ammo = self.inventoryAmmos[i] 

			if player.getInventorySlot(i) == None:
				ammo.setCaption("");
				continue

			ammoCount = player.getManaUsesSlot(i) if player.getInventorySlot(i).isManaWeapon() else player.getAmmoSlot(i);
			if ammoCount == None:
				ammoCount = '';
			elif ammoCount == 0 and player.getInventorySlot(i).isItemType():
				slot = self.inventorySlots[i];
				slot.setVisible(False);
			ammo.setCaption(str(ammoCount));
			if self.primaryRanged == i:
				self.ammoValue.setCaption(str(ammoCount));

		self.updateSelection();
		

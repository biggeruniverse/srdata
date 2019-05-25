# copyright (c) 2011 savagerebirth.com
# this file defines all the "contexts" used in the commhud and exists to minimise clutter

contextDict = {};

##Conventions
##Spell the context class referring to the object type as the name of the object type, but with first letters capitalised
##all lowercase for instances
##preserve underscores 

def addToQueue(otname, oid, x=0,y=0):
	ot = savage.getObjectType(otname);
	#we don't queue things that build themselves (gates)...
	if ot.getValue("selfBuild") == 1:
		CL_RequestPurchase(otname, -1);
	else:
		gblQueue.addResearch(savage.ResearchItem(ot.typeId, oid,x,y));

def buildContextsIfNeeded():
	if len(commcontexts.contextDict) == 0:
		cd = commcontexts.contextDict;
		cd[None] = commcontexts.emptycontext;
		cd["validation"] = commcontexts.ValidationContext();
		cd["global"] = commcontexts.GlobalContext();
		dc = commcontexts.DestroyContext();
		ut = commcontexts.UpgradedTower();
		hp = commcontexts.HumanPlayer();
		cd["human_nomad"] = cd["human_savage"] = cd["human_legionnaire"] = cd["human_ballista"] = cd["human_catapult"] = hp;
		hs = commcontexts.HumanStronghold();
		cd["human_stronghold"] = cd["human_stronghold2"] = cd["human_stronghold3"] = hs;
		cd["human_garrison"] = commcontexts.HumanGarrison();
		cd["human_siege"] = commcontexts.HumanSiege();
		cd["human_monastery"] = commcontexts.HumanMonastery();
		cd["human_magnetic_factory"] = cd["human_electric_factory"] = cd["human_chemical_factory"] = dc;
		cd["human_arrow_tower"] = commcontexts.HumanArrowTower();
		cd["human_chemical_tower"] = cd["human_electric_tower"] = ut;
		cd["human_magnetic_tower"] = dc;
		cd["human_arsenal"] = commcontexts.HumanArsenal();
		cd["human_research_center"] = commcontexts.HumanResearchCenter();
		cd["human_laboratory"] = commcontexts.HumanLaboratory();
		cd["human_worker"] = commcontexts.Worker();
		cd["human_build"] = commcontexts.HumanBuild();
		

		bp = commcontexts.BeastPlayer();
		cd["beast_scavenger"] = cd["beast_stalker"] = cd["beast_predator"] = cd["beast_summoner"] = cd["beast_behemoth"] = bp;
		bl = commcontexts.BeastLair();
		cd["beast_lair"] = cd["beast_lair2"] = cd["beast_lair3"] = bl;
		cd["beast_sublair"] = commcontexts.BeastSublair();
		cd["beast_nexus"] = commcontexts.BeastNexus();
		cd["beast_arcana"] = commcontexts.BeastArcana();
		cd["beast_alchema"] = commcontexts.BeastAlchema();
		cd["beast_charmshrine"] = commcontexts.BeastCharmshrine();
		cd["beast_sanctuary"] = commcontexts.BeastSanctuary();
		cd["beast_entropy_shrine"] = commcontexts.BeastEntropyShrine();
		cd["beast_strata_shrine"] = commcontexts.BeastStrataShrine();
		cd["beast_fire_shrine"] = commcontexts.BeastFireShrine();
		cd["beast_spire"] = commcontexts.BeastSpire();
		cd["beast_entropy_spire"] = cd["beast_strata_spire"] = cd["beast_fire_spire"] = ut;
		cd["beast_gateway"] = commcontexts.BeastGateway();
		cd["beast_worker"] = commcontexts.Worker(); 
		cd["beast_build"] = commcontexts.BeastBuild();

global Context;

class Context:
	otnames = [];
	def __init__(self, go):
		self.object = go;
		self.actions = [];
		self.buttons = OrderedDict();
		#make some buttons
		for otname in self.otnames:
			ot = savage.getObjectType(otname);
			actionName = "Research "+ot.getValue("description");
			icon = ot.getValue("icon")+".s2g";
			self.createAction(actionName,icon);
	
	def createAction(self, name, image):
		self.actions.append(name);
		b = HotKeyButton(name, image);
		b.addActionListener(self);
		self.buttons[name] = b;
	
	def getContextActions(self):
		data = OrderedDict([(action, Enabled) for action in self.actions]);
		team = savage.getLocalTeam();
		#use Enabled, Disabled, or Hidden
		if self.otnames != []:
			for i, action in enumerate(self.actions[:-1]):
				ot = savage.getObjectType( self.otnames[i] );
				item = savage.ResearchItem(ot.typeId, 0, 0, 0);
				if item.areTechRequirementsMet() == False:
					data[action] = Disabled;
				if ot in team.getWeapons() or ot in team.getUnits() or ot in team.getItems():
					data[action] = Hidden;
				elif ot in team.getUpgrades():
					data[action] = Hidden;
				elif ot in [ri.objtype for ri in team.getResearch()] or gblQueue.contains(ot.typeId):
					if not ot.isWorkerType() and not ot.isBuildingType():
						data[action] = Hidden;

		return data;
		
	def getButtonList(self):
		return self.buttons.values();
		
	def getButtonAction(self, action):
		return self.buttons[action];
		
	def onAction(self, e):
		response = self.actionResponse(e);
		if response == None:
			#commhud.getActiveContextMenu(self).close();
			pass;
		else: #return True or something
			#don't close the menu
			pass;
	
	def actionResponse(self, e):
		if e.action == "Destroy":
			cm = commhud.getActiveContextMenu(self);
			cd = commcontexts.contextDict;			
			cm.switchContexts(cd["validation"]);
			return True;
		elif e.action == "Build":
			commhud.toolBox.tabContainer.setSelectedTab(1);
			return True;
		elif e.action == "Goto" or e.action == "Follow" or e.action == "Attack":
			CL_PickLocation(000);
			return True;
		else:
			try:
				otname = self.otnames[self.actions.index(e.action)];
				commcontexts.addToQueue(otname,self.object.objectId);
			except:
				con_println("^yYou should be handling '"+str(e)+"'!\n");

## Contexts for both races ##

class EmptyContext(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build", "/gui/standard/comm/build_order.s2g");
		self.createAction("Move", "/gui/standard/comm/move_order.s2g");
		self.createAction("Follow", "/gui/standard/comm/follow_icon.s2g");
		
	def getContextActions(self):
		data = OrderedDict([(action, Enabled) for action in self.actions
]);
		team = savage.getLocalTeam();
		teamNum = team.teamId;
		
		builders = commhud.selection.getUnits(teamNum)
		if len(builders) == 0:
			data["Build"] = Disabled;
		
		return data;
		
	def actionResponse(self,e):
		if e.action == "Move":
			"""
			x, y = commhud.getActiveContextMenu(self).coords;
			teamNum = savage.getLocalTeam().teamId;
			commhud.selection.send(teamNum)
			CL_OrderWaypoint(x,y);
			"""
			# We need some kind of CommanderMode that asks for coords. I'm sure there already
			# is one somewhere deep inside all that code!
			
		elif e.action == "Build":
			"""
			team = savage.getLocalTeam();
			builders = commhud.selection.getUnits(team.teamId)
			if len(builders) > 0:
				commhud.selection.setSelection(builders)
				commhud.selection.send()
				cm = commhud.getActiveContextMenu(self);
				cd = commcontexts.contextDict;
				key = "human_build" if team.getRace() == "human" else "beast_build";
				cm.switchContexts(cd[key]);
				return True;
			"""
			commhud.toolBox.tabContainer.setSelectedTab("Build");

		elif e.action == "Follow":
			"""
			x, y = commhud.getActiveContextMenu(self).coords;
			obj = savage.getObjectUnder(x,y);
			if obj is not None:
				teamNum = savage.getLocalTeam().teamId;
				commhud.selection.send(teamNum)
				CL_OrderWaypoint(x,y,obj.objectId);
			"""
			# See "Move"					

emptycontext = EmptyContext();
#this is the exception, all other contexts are made elsewhere

class ValidationContext(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Yes", "/gui/standard/yes.s2g");
		#self.createAction("","/gui/game/images/transparent.s2g"); # big wants a space between Yes and No
		# Can't get it to load the transparent.s2g image :(
		self.createAction("No", "/gui/standard/cancel.s2g");
		
	def actionResponse(self, e):
		cm = commhud.getActiveContextMenu(self);
		if e.action == "Yes":
			CL_RequestDestroy(cm.lastContext.object.objectId);
			cm.switchContexts(cm.lastContext);
		elif e.action == "No":
			cm.switchContexts(cm.lastContext);

class GlobalContext(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Global Return", "/gui/game/images/guard.s2g");
		self.createAction("Global Redstone", "weneedmoreredstone");
		self.createAction("Global Gold", "weneedmoregold");

		# More stuff to come!

	def actionResponse(self, e):
		if e.action == "Global Return":
			team = savage.getLocalTeam();
			x, y, z = team.getCommandCenter().getPosition();
			CL_OrderWaypoint(x,y);
			CL_SendVoiceChat( 0, 3);

class DestroyContext(Context): 
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g"); 

class UpgradedTower(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Attack", "/gui/standard/comm/attack_icon.s2g"); 
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g"); 
			
class Worker(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build", "/gui/standard/comm/build_order.s2g");
		self.createAction("Goto", "/gui/standard/comm/move_order.s2g");
		self.createAction("Follow", "/gui/standard/comm/follow_icon.s2g");
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

## Human Contexts ##


class HumanPlayer(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build", "/gui/standard/comm/build_order.s2g");
		#self.createAction("Goto", "/gui/standard/comm/move_order.s2g");
		self.createAction("Follow", "/gui/standard/comm/follow_icon.s2g");
		self.createAction("Promote", "/gui/game/images/promote.s2g");
		self.createAction("Demote", "/gui/game/images/demote_human.s2g");
		self.createAction("Gold", "/gui/standard/icons/gold/gold_icon.s2g");
		self.createAction("Elecbuff", "/models/human/items/icons/electrify.s2g");
		self.createAction("Shieldbuff","/models/human/items/icons/magneticshield.s2g");
		self.createAction("Chembuff", "/models/human/items/icons/speedboost.s2g");

	def getContextActions(self):
		data = OrderedDict([(action, Enabled) for action in self.actions]);
		team = savage.getLocalTeam();
		#use Enabled, Disabled, or Hidden

		# This is not good, but too tired to change it right now, TODO
		if self.object.isOfficer():
			data["Promote"] = Hidden;
		else:
			data["Demote"] = Hidden;

		if self.object.getType().isSiegeType(): 
			data["Elecbuff"] = data["Shieldbuff"] = data["Chembuff"] = Hidden;
		if team.getResources()["magnetic"] < 80:
			data["Shieldbuff"] = Disabled;
		if team.getResources()["electric"] < 80:
			data["Elecbuff"] = Disabled;
		if team.getResources()["chemical"] < 80:
			data["Chembuff"] = Disabled;

		return data;

		
	def actionResponse(self, e):
		if e.action == "Promote":
			CL_RequestPromote(self.object.objectId);
		elif e.action == "Demote":
			CL_RequestDemote(self.object.objectId);
		elif e.action == "Gold":
			CL_RequestGiveGold(self.object.objectId, 100);
		elif e.action == "Elecbuff":
			CL_RequestActivatePowerup(self.object.objectId, "human_electrify");
		elif e.action == "Shieldbuff":
			CL_RequestActivatePowerup(self.object.objectId, "human_magnetic_shield");
		elif e.action == "Chembuff":
			CL_RequestActivatePowerup(self.object.objectId, "human_adrenaline");
		else:
			Context.actionResponse(self, e);
		cm = commhud.getActiveContextMenu(self);
		cm.buildContext(cm.context);

class HumanStronghold(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build Worker", "/gui/standard/icons/human/human_worker.s2g");
		self.createAction("Upgrade Stronghold", "/gui/standard/comm/upgrade_stronghold.s2g"); 
		self.createAction("Research Savage", "/gui/standard/icons/human/human_savage.s2g"); 
		self.createAction("Research Legionnaire", "/gui/standard/icons/human/human_legionnaire.s2g"); 
	
	def getContextActions(self):
		data = Context.getContextActions(self);
		team = savage.getLocalTeam();
		name = self.object.getType().getName();		

		if team.atMaxWorkers():
			data["Build Worker"] = Disabled;
		else:
			data["Build Worker"] = Enabled;
		
		level = "2" if self.object.getType().getName() == "human_stronghold" else "3";
		item = savage.ResearchItem(savage.getObjectType("human_stronghold" + level).typeId, 0, 0, 0);
		if item.areTechRequirementsMet() == False:
			data["Upgrade Stronghold"] = Disabled;
		if (name == "human_stronghold3" or
		    "human_stronghold3" in team.getResearch() or
		    "human_stronghold2" in team.getResearch() ):
			data["Upgrade Stronghold"] = Hidden;
	
		sav = savage.getObjectType("human_savage");
		
		if sav in team.getUnits():
			data["Research Savage"] = Hidden;
		elif self.object.getType().getName() == "human_stronghold" or sav in team.getResearch():
			data["Research Savage"] = Disabled;
		# we will add it to the ActionSequence queue, so it doesn't matter if it's affordable
		
		lego = savage.getObjectType("human_legionnaire");
		
		if lego in team.getUnits():
			data["Research Legionnaire"] = Hidden;
		elif self.object.getType().getName() != "human_stronghold3" or lego in team.getResearch():
			data["Research Legionnaire"] = Disabled;
		#later we add to the queue if it's chosen
		
		return data;
	
	def actionResponse(self, e):
		if e.action == "Build Worker":
			commcontexts.addToQueue("human_worker",self.object.objectId);
			return True;
		
		elif e.action == "Upgrade Stronghold":
			level = "2" if self.object.getType().getName() == "human_stronghold" else "3";
			commcontexts.addToQueue("human_stronghold"+level,self.object.objectId);
		
		elif e.action == "Research Savage":
			commcontexts.addToQueue("human_savage",self.object.objectId);
		
		elif e.action == "Research Legionnaire":
			commcontexts.addToQueue("human_legionnaire",self.object.objectId);

class HumanGarrison(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build Worker", "/gui/standard/icons/human/human_worker.s2g");
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g"); 
	
	def getContextActions(self):
		data = Context.getContextActions(self);
		team = savage.getLocalTeam();
		
		if team.atMaxWorkers():
			data["Build Worker"] = Disabled;
		return data;
	
	def actionResponse(self, e):		
		if e.action == "Build Worker":
			commcontexts.addToQueue("human_worker",self.object.objectId);
			return True;		
		elif e.action == "Destroy":
			cm = commhud.getActiveContextMenu(self);
			cd = commcontexts.contextDict;			
			cm.switchContexts(cd["validation"]);
			return True;
			

class HumanSiege(Context):	
	otnames = ["human_ballista","human_catapult"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class HumanMonastery(Context):
	otnames = ["human_medic","human_potion","human_revive"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class HumanArrowTower(Context):
	otnames = ["human_chemical_tower","human_electric_tower","human_magnetic_tower"];
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g"); 

class HumanArsenal(Context):
	otnames = ["human_crossbow","human_sniperbow","human_scattergun","human_repeater","human_coilrifle","human_discharger","human_fluxgun","human_pulsegun","human_incinerator","human_mortar","human_launcher"];
	def __init__(self):
		Context.__init__(self, None);	
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g"); 

class HumanResearchCenter(Context):
	otnames = ["human_medkit","human_ammo_pack","human_motion_sensor","human_immobilizer","human_disruptor","human_relocater","human_demo_pack","human_landmine"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class HumanLaboratory(Context):
	otnames = ["human_catapult_splash", "human_ammo_carry", "human_building_hp"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g"); 

class HumanBuild(Context):
	otnames = ["human_garrison","human_arsenal","human_research_center","human_siege","human_electric_factory","human_chemical_factory","human_magnetic_factory","human_arrow_tower","human_monastery","human_laboratory", "human_goldmine"];
	def __init__(self):
		Context.__init__(self, None);

		# Alright, we need no cancel action when we stick to the standard-rts layout:
		#self.createAction("Cancel", "/gui/standard/comm/cancel.s2g");
		#TODO this isn't very generic, a less-hardcodey solution might be more satisfying	
		
	def actionResponse(self, e):
		"""
		See in __init__, no real need for that if we stick to the rts layout.
		if e.action == "Cancel":
			cm = commhud.getActiveContextMenu(self);
			cm.switchContexts(cm.lastContext);
			return True;
		"""
		#else:
		teamNum = savage.getLocalPlayer().getTeam();
		builders = commhud.selection.getUnits(teamNum)
		commhud.selection.setSelection(builders)
		commhud.selection.send()
		otname = self.otnames[self.actions.index(e.action)];
		CL_RequestPurchase(otname, savage.getLocalPlayer().objectId);
		#do we need to send these things through the queue?

## Beast Contexts ## 

class BeastPlayer(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build", "/gui/standard/comm/build_order.s2g");
		#self.createAction("Goto", "/gui/standard/comm/move_order.s2g");
		self.createAction("Follow", "/gui/standard/comm/follow_icon.s2g");
		self.createAction("Promote", "/gui/game/images/promote_beast.s2g");
		self.createAction("Demote", "/gui/game/images/demote_beast.s2g");
		self.createAction("Gold", "/gui/standard/icons/gold/gold_icon.s2g");
		self.createAction("Firebuff", "/models/beast/items/icons/fireshield.s2g");
		self.createAction("Heal", "/models/beasts/items/icons/manarestore.s2g");

	def getContextActions(self):
		data = OrderedDict([(action, Enabled) for action in self.actions]);
		team = savage.getLocalTeam();
		#use Enabled, Disabled, or Hidden
		if self.object.isOfficer():
			data["Promote"] = Hidden;
		else:
			data["Demote"] = Hidden;
		if self.object.getType().isSiegeType(): 
			data["Firebuff"] = data["Heal"] = Hidden;

		# Are those values correct? I don't know...
		if team.getResources()["fire"] < 80:
			data["Firebuff"] = Disabled;
		if team.getResources()["strata"] < 80:
			data["Heal"] = Disabled;
		return data;

		
	def actionResponse(self, e):
		if e.action == "Promote":
			CL_RequestPromote(self.object.objectId);
		elif e.action == "Demote":
			CL_RequestDemote(self.object.objectId);
		elif e.action == "Gold":
			CL_RequestGiveGold(self.object.objectId, 100);
		elif e.action == "Firebuff":
			CL_RequestActivatePowerup(self.object.objectId, "beast_fire_shield");
		elif e.action == "Heal":
			CL_RequestActivatePowerup(self.object.objectId, "beast_recharge");
		else:
			Context.actionResponse(self, e);
		cm = commhud.getActiveContextMenu(self);
		cm.buildContext(cm.context);


class BeastLair(Context):
	otnames = [];
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build Worker", "/gui/standard/icons/beast/beast_worker.s2g");
		self.createAction("Upgrade Lair", "/gui/standard/comm/upgrade_stronghold.s2g"); 
		self.createAction("Research Stalker", "/gui/standard/icons/beast/beast_stalker.s2g"); 
		self.createAction("Research Predator", "/gui/standard/icons/beast/beast_predator.s2g"); 
		
	def getContextActions(self):
		data = Context.getContextActions(self);
		team = savage.getLocalTeam();
		name = self.object.getType().getName();
		
		if team.atMaxWorkers():
			data["Build Worker"] = Disabled;
		
		level = "2" if self.object.getType().getName() == "beast_lair" else "3";
		item = savage.ResearchItem(savage.getObjectType("beast_lair" + level).typeId, 0, 0, 0);
		if item.areTechRequirementsMet() == False:
			data["Upgrade Lair"] = Disabled;		
		if (name == "beast_lair3" or "beast_lair3" in team.getResearch() or "beast_lair2" in team.getResearch() ):			
			data["Upgrade Lair"] = Hidden;

		stalker = savage.getObjectType("beast_stalker");
		
		if stalker in team.getUnits():
			data["Research Stalker"] = Hidden;
		elif self.object.getType().getName() == "beast_lair" or stalker in team.getResearch():
			data["Research Stalker"] = Disabled;
		
		pred = savage.getObjectType("beast_predator");
		
		if pred in team.getUnits():
			data["Research Predator"] = Hidden;
		elif self.object.getType().getName() != "beast_lair3" or pred in team.getResearch():
			data["Research Predator"] = Disabled;
		
		return data;

	def actionResponse(self, e):
		if e.action == "Build Worker":
			commcontexts.addToQueue("beast_worker",self.object.objectId);
			return True;
		
		elif e.action == "Upgrade Lair":
			level = "2" if self.object.getType().getName() == "beast_lair" else "3";
			commcontexts.addToQueue("beast_lair"+level,self.object.objectId);
		
		elif e.action == "Research Stalker":
			commcontexts.addToQueue("beast_stalker",self.object.objectId);
		
		elif e.action == "Research Predator":
			commcontexts.addToQueue("beast_predator",self.object.objectId);

class BeastSublair(Context):
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Build Worker", "/gui/standard/icons/beast/beast_worker.s2g");
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g"); 
	def getContextActions(self):
		data = Context.getContextActions(self);
		team = savage.getLocalTeam();
		
		if team.atMaxWorkers():
			data["Build Worker"] = Disabled;
		return data;
	
	def actionResponse(self, e):
		if e.action == "Build Worker":
			commcontexts.addToQueue("beast_worker",self.object.objectId);
			return True;
		elif e.action == "Destroy":
			cm = commhud.getActiveContextMenu(self);
			cd = commcontexts.contextDict;			
			cm.switchContexts(cd["validation"]);
			return True;

class BeastNexus(Context):
	otnames = ["beast_poison","beast_rabid","beast_vampire"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastAlchema(Context):
	otnames = ["beast_tempest_range", "beast_building_hp", "beast_sac_splash", "beast_gate"];
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastArcana(Context):
	otnames = ["beast_mana_stone","beast_stamina_boost","beast_tracking_sense","beast_snare","beast_protect","beast_camouflage","beast_immolate","beast_fire_trap"];
	def __init__(self):
		Context.__init__(self, None);
		#HARDCODE TODO use team.getAllItems()?
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastCharmshrine(Context):
	otnames = ["beast_summoner","beast_behemoth"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastSanctuary(Context):
	otnames = ["beast_medic","beast_shield","beast_revive"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastEntropyShrine(Context):
	otnames = ["beast_entropy1","beast_entropy2","beast_entropy3","beast_gateway"];
	def __init__(self):
		Context.__init__(self, None);
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastStrataShrine(Context):
	otnames = ["beast_strata1","beast_strata2","beast_strata3"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastFireShrine(Context):
	otnames = ["beast_fire1","beast_fire2","beast_fire3"];
	def __init__(self):
		Context.__init__(self, None);		
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastSpire(Context):
	otnames = ["beast_entropy_spire","beast_strata_spire","beast_fire_spire"];
	def __init__(self):
		Context.__init__(self, None);	
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");

class BeastGateway(Context):
	def __init__(self):
		Context.__init__(self, None);	
		self.createAction("Destroy", "/gui/standard/comm/demolish.s2g");		

class BeastBuild(Context):
	otnames = ["beast_sublair","beast_nexus","beast_arcana","beast_charmshrine","beast_fire_shrine","beast_strata_shrine","beast_entropy_shrine","beast_spire","beast_sanctuary","beast_alchema", "beast_goldmine"];
	def __init__(self):
		Context.__init__(self, None);
		#self.createAction("Cancel", "/gui/standard/comm/cancel.s2g");
		
	def actionResponse(self, e):
		"""
		See HumanBuild...
		if e.action == "Cancel":
			cm = commhud.getActiveContextMenu(self);
			cm.switchContexts(cm.lastContext);
			return True;
		"""
		#else:
		teamNum = savage.getLocalPlayer().getTeam();
		builders = commhud.selection.getUnits(teamNum);
		commhud.selection.setSelection(builders)
		commhud.selection.send()
		otname = self.otnames[self.actions.index(e.action)];
		CL_RequestPurchase(otname, savage.getLocalPlayer().objectId);


# (c) 2011 savagerebirth.com

import savage;

class NoticesEventHandler(EventListener):
	def __init__(self):
		pass;

	def onEvent(self, e):
		if isinstance(e, NotifyEvent):
			con_println("notice! "+str(e)+"\n");

		elif e.eventType == "research_complete":
			objtype = savage.ObjectType(e.objtype);
			obj = savage.getGameObject(e.sourceId);
			team = savage.Team(obj.getTeam());
			if objtype.isBuildingType():
				if objtype.getName() == "beast_sublair":
					Sound_PlaySound(savage.getSound("beast_sublair_constructed"));
				elif objtype.getName() == "human_garrison":
					Sound_PlaySound(savage.getSound("human_garrison_constructed"));
				else:
					Sound_PlaySound(savage.getSound(team.getRace()+"_new_building"));
		
			
			elif objtype.isWeaponType():
				Sound_PlaySound(savage.getSound(team.getRace()+"_new_weapon"));
			elif objtype.isItemType():
				Sound_PlaySound(savage.getSound(team.getRace()+"_new_item"));
			elif objtype.isUnitType() and not objtype.isWorkerType():
				Sound_PlaySound(savage.getSound(team.getRace()+"_new_unit"));



neh = NoticesEventHandler();
gblEventHandler.addGameListener(neh);
gblEventHandler.addNotifyListener(neh);

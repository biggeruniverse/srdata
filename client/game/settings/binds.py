#copyright 2011 savagerebirth.com
#this file defines functions for used for binds
#Format:
#<Profile Name>_<Bind Name>_<Up or Down>, where bindname has any spaces removed
#this file MUST be execmodded

####Player
## Motion

def Player_MoveForward_Down():
	move_forward(1);
def Player_MoveForward_Up():
	move_forward(0);

def Player_MoveBackward_Down():
	move_back(1);
def Player_MoveBackward_Up():
	move_back(0);

def Player_MoveLeft_Down():
	move_left(1);
def Player_MoveLeft_Up():
	move_left(0);

def Player_MoveRight_Down():
	move_right(1);
def Player_MoveRight_Up():
	move_right(0);

def Player_Jump_Down():
	jump(1);
def Player_Jump_Up():
	jump(0);

def Player_Sprint_Down():
	button(4,1);
def Player_Sprint_Up():
	button(4,0);

##ACTIONS

def Player_AttackAction_Down():
	button(1,1);
def Player_AttackAction_Up():
	button(1,0);

def Player_BlockLeap_Down():
	if cvar_getvalue("cl_blockleapswitch") == 1:
		savage.getLocalPlayer().switchInventorySlot(0);
	button(2,1);
def Player_BlockLeap_Up():
	button(2,0);

def Player_RapidAttack_Down():
	button(6,1);
def Player_RapidAttack_Up():
	button(6,0);

def Player_AutoAttack_Down():
	if isbuttondown(6):
		button(6,0);
	else:
		button(6,1);
def Player_AutoAttack_Up():
	pass; #TODO

##UTILITIES

def Player_SelectPrimary_Down():
	savage.getLocalPlayer().switchInventorySlot(0);
def Player_SelectPrimary_Up():
	pass;

def Player_SelectSecondary_Down():
	savage.getLocalPlayer().switchInventorySlot(1);
def Player_SelectSecondary_Up():
	pass;

def Player_SelectItem1_Down():
	savage.getLocalPlayer().switchInventorySlot(2);
def Player_SelectItem1_Up():
	pass;

def Player_SelectItem2_Down():
	savage.getLocalPlayer().switchInventorySlot(3);
def Player_SelectItem2_Up():
	pass;

def Player_SelectItem3_Down():
	savage.getLocalPlayer().switchInventorySlot(4);
def Player_SelectItem3_Up():
	pass;

def Player_SelectItemPrevious_Down():
	savage.getLocalPlayer().scrollInventorySlot(-1);
def Player_SelectItemPrevious_Up():
	pass;

def Player_SelectItemNext_Down():
	savage.getLocalPlayer().scrollInventorySlot(1);
def Player_SelectItemNext_Up():
	pass;

##INTERACTION

def Player_EnterBuilding_Down():
	button(3,1);
def Player_EnterBuilding_Up():
	button(3,0);

def Player_OfficerMark_Down():
	CL_SendOfficerCommand();
def Player_OfficerMark_Up():
	pass;

def Player_OfficerMarkLast_Down():
	p = savage.getLocalPlayer();
	if p.isOfficer():
		CL_SendOfficerObjectCommand(hud.crosshair.getLastObject());
	else:
		o = hud.crosshair.lastObject;
		if o is not None and o.getTeam() != p.getTeam():
			if o.getType().isCharacterType():
				CL_SendVoiceChat(1, 3);
			elif o.getType().isWorkerType():
				CL_SendVoiceChat(4, 4);
			elif o.getType().isSiegeType():
				CL_SendVoiceChat(1, 7);

def Player_OfficerMarkLast_Up():
	pass;

def Player_EjectFromSiege_Down():
	CL_RequestEject(); #TODO mouse mode may need to be updated (e.g. ballista -> nomad)
def Player_EjectFromSiege_Up():
	pass;

def Player_UnitSelection_Down():
	CL_RequestLoadout();
def Player_UnitSelection_Up():
	pass;

def Player_RequestBuff1_Down():
	t = savage.Team(savage.getLocalPlayer().getTeam()).getRace();
	if t == "human":
		CL_RequestPowerup("human_electrify");
	elif t == "beast":
		CL_RequestPowerup("beast_fire_shield");

def Player_RequestBuff1_Up():
	pass;

def Player_RequestBuff2_Down():
	t = savage.Team(savage.getLocalPlayer().getTeam()).getRace();
	if t == "human":
		CL_RequestPowerup("human_magnetic_shield");
	elif t == "beast":
		CL_RequestPowerup("beast_recharge");

def Player_RequestBuff2_Up():
	pass;

def Player_RequestBuff3_Down():
	t = savage.Team(savage.getLocalPlayer().getTeam()).getRace();
	if t == "human":
		CL_RequestPowerup("human_adrenaline");

def Player_RequestBuff3_Up():
	pass;

def Player_Zoom_Down():
	cvar_setvalue("cl_zoomfov", 20);
def Player_Zoom_Up():
	cvar_setvalue("cl_zoomfov", cvar_getvalue("cl_fov"));

##COMMUNICATION

def Player_VoteYes_Down():
	hud.voteWindow.castVote('yes'); #TODO cast yes on the visible vote window only
def Player_VoteYes_Up():
	pass;

def Player_VoteNo_Down():
	hud.voteWindow.castVote('no');  #TODO cast no on the visible vote window only, we could be in SPECHUD for example
def Player_VoteNo_Up():
	pass;

def Player_IgnoreVote_Down():
	hud.voteWindow.hide();
def Player_IgnoreVote_Up():
	pass;

def Player_ChatAll_Down():
	pass;
def Player_ChatAll_Up():
	hud.chatBox.activate("all"); #TODO whichever chat box is needed

def Player_ChatTeam_Down():
	pass;
def Player_ChatTeam_Up():
	hud.chatBox.activate("team"); #TODO whichever chat box is needed

def Player_ChatCommander_Down():
	pass;
def Player_ChatCommander_Up():
	hud.chatBox.activate("comm"); #TODO whichever chat box is needed

def Player_ChatSquad_Down():
	pass;
def Player_ChatSquad_Up():
	hud.chatBox.activate("squad"); #TODO whichever chat box is needed

def Player_ChatClan_Down():
	pass;
def Player_ChatClan_Up():
	hud.chatBox.activate("clan"); #TODO whichever chat box is needed

def Player_VoiceChat_Down():
	hud.voiceChat.newVoiceChat(); #TODO whichever voice chat box is needed
def Player_VoiceChat_Up():
	pass;

def Player_ShowChatHistory_Down():
	hud.chatBox.showHistory(1);
def Player_ShowChatHistory_Up():
	hud.chatBox.showHistory(0);

def Player_Ready_Down():
	CL_RequestReady();
def Player_Ready_Up():
	pass;

## GUI

def Player_ShowScoreboard_Down():
	hud.scoreboard.setVisible(True); #TODO handle other scoreboards
def Player_ShowScoreboard_Up():
	hud.scoreboard.setVisible(False); #TODO handle other scoreboards

def Player_ShowAccuracy_Down():
	pass; #TODO
def Player_ShowAccuracy_Up():
	pass; #TODO

def Player_ShowResearch_Down():
	pass; #TODO
def Player_ShowResearch_Up():
	pass; #TODO

def Player_ShowGraphics_Down():
	if hud.topBar.graphicspanel.isVisible():
		hud.topBar.setVisible(False);
		hud.topBar.graphicspanel.hide();		
	else:
		hud.topBar.graphicspanel.show();
		hud.topBar.setVisible(True);
def Player_ShowGraphics_Up():
	pass; #TODO

def Player_ToggleResources_Down():
	cvar_setvalue("gui_showTeamStatus",1-cvar_getvalue("gui_showTeamStatus"));
def Player_ToggleResources_Up():
	pass;

def Player_ToggleMinimap_Down():
	hud.minimap.setVisible(1-int(hud.minimap.isVisible()));
def Player_ToggleMinimap_Up():
	pass;

def Player_ToggleMinimapSize_Down():
	pass; #TODO
def Player_ToggleMinimapSize_Up():
	pass; #TODO

def Player_Screenshot_Down():
	screenshot();
def Player_Screenshot_Up():
	pass;

def Player_ReturnToLobby_Down():
	# For now, I'll put the topbar code in here, have to change the names and all the stuff,
	# maybe call it Player_ShowIngameTopbar_Down() or something like that, TODO
	if glass.GUI_CurrentScreen() == "hud":
		hud.topBar.setVisible(not hud.topBar.isVisible());
	elif glass.GUI_CurrentScreen() == "loadout":
		# There's currently no topbar in the loadout screen. Not sure if we should add one tho.
		CL_RequestLobby();
def Player_ReturnToLobby_Up():
	pass;

## and now the COMMANDER BINDS
## POINT OF VIEW
def Comm_ScrollUp_Down():
	jump(1);
def Comm_ScrollUp_Up():
	jump(0);

def Comm_ScrollDown_Down():
	crouch(1);
def Comm_ScrollDown_Up():
	crouch(0);

def Comm_ScrollLeft_Down():
	move_left(1);
def Comm_ScrollLeft_Up():
	move_left(0);

def Comm_ScrollRight_Down():
	move_right(1);
def Comm_ScrollRight_Up():
	move_right(0);

def Comm_ZoomIn_Down():
	val = max(cvar_getvalue("cl_zoomfov")-5, 50);
	cvar_setvalue("cl_zoomfov", val);
	val = min(-35, cvar_getvalue("cl_cmdr_camtiltx")+3);
	cvar_setvalue("cl_cmdr_camtiltx", val);
def Comm_ZoomIn_Up():
	pass;

def Comm_ZoomOut_Down():
	val = min(cvar_getvalue("cl_zoomfov")+5, 90);
	cvar_setvalue("cl_zoomfov", val);
	val = max(-64, cvar_getvalue("cl_cmdr_camtiltx")-3);
	cvar_setvalue("cl_cmdr_camtiltx", val);
def Comm_ZoomOut_Up():
	pass;

def Comm_RotateViewCCW_Down():
	CL_RotateCamera(5);
def Comm_RotateViewCCW_Up():
	pass;

def Comm_RotateViewCW_Down():
	CL_RotateCamera(-5);
def Comm_RotateViewCW_Up():
	pass;

def Comm_DefaultView_Down():
	CL_RotateCameraTo(0);
def Comm_DefaultView_Up():
	pass;

## COMMUNICATION

def Comm_VoteYes_Down():
	commhud.voteWindow.castVote('yes');
def Comm_VoteYes_Up():
	pass;

def Comm_VoteNo_Down():
	commhud.voteWindow.castVote('no');
def Comm_VoteNo_Up():
	pass;

def Comm_IgnoreVote_Down():
	commhud.voteWindow.hide();
def Comm_IgnoreVote_Up():
	pass;

def Comm_ChatAll_Down():
	pass;

def Comm_ChatAll_Up():
	commhud.chatBox.activate('all');

def Comm_ChatTeam_Down():
	pass;
	
def Comm_ChatTeam_Up():
	commhud.chatBox.activate('team');

def Comm_VoiceChat_Down():
	commhud.voiceChat.newVoiceChat();
def Comm_VoiceChat_Up():
	pass;

def Comm_ShowChatHistory_Down():
	commhud.chatBox.showHistory(1);
def Comm_ShowChatHistory_Up():
	commhud.chatBox.showHistory(0);

def Comm_Ready_Down():
	CL_RequestReady();
def Comm_Ready_Up():
	pass;

##ACTIONS

def Comm_RotateBuildingCCW_Down():
	CL_RotateBuilding(10);
def Comm_RotateBuildingCCW_Up():
	CL_RotateBuilding(0);

def Comm_RotateBuildingCW_Down():
	CL_RotateBuilding(-10);
def Comm_RotateBuildingCW_Up():
	CL_RotateBuilding(0);


##SHORTCUTS

def Comm_GotoBase_Down():
	pass; #TODO centre camera on savage.getLocalTeam().getCommandCenter()
def Comm_GotoBase_Up():
	pass;

def Comm_GotoIdleWorker_Down():
	pass; #TODO
def Comm_GotoIdleWorker_Up():
	pass;

def Comm_GotoLastMessage_Down():
	pass;
def Comm_GotoLastMessage_Up():
	pass;

def Comm_GotoOfficers_Down():
	pass;
def Comm_GotoOfficers_Up():
	pass;

def Comm_GotoOfficer1_Down():
	pass;
def Comm_GotoOfficer1_Up():
	pass;

def Comm_GotoOfficer2_Down():
	pass;
def Comm_GotoOfficer2_Up():
	pass;

def Comm_GotoOfficer3_Down():
	pass;
def Comm_GotoOfficer3_Up():
	pass;

## GUI

def Comm_ShowScoreboard_Down():
	commhud.scoreboard.setVisible(True); 
def Comm_ShowScoreboard_Up():
	commhud.scoreboard.setVisible(False); 
def Comm_ShowUnitList_Down():
	commhud.rosterWindow.toggle();
def Comm_ShowUnitList_Up():
	pass;

def Comm_ToggleResearch_Down():
	if commhud.researchWindow.isVisible():
		commhud.researchWindow.close(); 
	else:
		commhud.researchWindow.open();
def Comm_ToggleResearch_Up():
	pass;

def Comm_ToggleMinimap_Down():
	pass;
def Comm_ToggleMinimap_Up():
	pass;

def Comm_ToggleMinimapSize_Down():
	pass;
def Comm_ToggleMinimapSize_Up():
	pass;

def Comm_Screenshot_Down():
	screenshot();
def Comm_Screenshot_Up():
	pass;

def Comm_ShowGraphics_Down():
	if commhud.topBar.graphicspanel.isVisible():
		commhud.topBar.setVisible(False);
		commhud.topBar.graphicspanel.hide();		
	else:
		commhud.topBar.graphicspanel.show();
		commhud.topBar.setVisible(True);
def Comm_ShowGraphics_Up():
	pass; #TODO

def Comm_ShowTopbar_Down():
	# For now, I'll put the topbar code in here, have to change the names and all the stuff,
	# maybe call it Player_ShowIngameTopbar_Down() or something like that, TODO
	if CL_CommanderMode() == CMDR_PLACING_OBJECT or CL_CommanderMode() == CMDR_PLACING_LINK:
		return;
	else:
		commhud.topBar.setVisible(not commhud.topBar.isVisible());

def Comm_ShowTopbar_Up():
	pass;
	
#### Spectator

## Motion

def Spec_MoveForward_Down():
	move_forward(1);
def Spec_MoveForward_Up():
	move_forward(0);

def Spec_MoveBackward_Down():
	move_back(1);
def Spec_MoveBackward_Up():
	move_back(0);

def Spec_MoveLeft_Down():
	move_left(1);
def Spec_MoveLeft_Up():
	move_left(0);

def Spec_MoveRight_Down():
	move_right(1);
def Spec_MoveRight_Up():
	move_right(0);

def Spec_MoveUp_Down():
	jump(1);
def Spec_MoveUp_Up():
	jump(0);

def Spec_MoveFaster_Down():
	button(4,1);
def Spec_MoveFaster_Up():
	button(4,0);

##COMMUNICATION

def Spec_VoteYes_Down():
	spechud.voteWindow.castVote('yes'); #TODO cast yes on the visible vote window only
def Spec_VoteYes_Up():
	pass;

def Spec_VoteNo_Down():
	spechud.voteWindow.castVote('no');  #TODO cast no on the visible vote window only, we could be in SPECHUD for example
def Spec_VoteNo_Up():
	pass;

def Spec_IgnoreVote_Down():
	spechud.voteWindow.hide();
def Spec_IgnoreVote_Up():
	pass;

def Spec_ChatAll_Down():
	pass;
def Spec_ChatAll_Up():
	if spechud.hud.isVisible():
		spechud.chatBox.activate("all");
	elif spechud.lobby.isVisible():
		spechud.lobby.chatBox.activate("all");

def Spec_ChatTeam_Down():
	pass;
def Spec_ChatTeam_Up():
	if spechud.hud.isVisible():
		spechud.chatBox.activate("team");
	elif spechud.lobby.isVisible():
		spechud.lobby.chatBox.activate("team");

def Spec_VoiceChat_Down():
	spechud.voiceChat.newVoiceChat(); #TODO whichever voice chat box is needed
def Spec_VoiceChat_Up():
	pass;

def Spec_ShowChatHistory_Down():
	spechud.chatBox.showHistory(True);
def Spec_ShowChatHistory_Up():
	spechud.chatBox.showHistory(False);

## GUI

def Spec_ShowScoreboard_Down():
	spechud.scoreboard.setVisible(True); 
def Spec_ShowScoreboard_Up():
	spechud.scoreboard.setVisible(False); 

def Spec_ShowResearch_Down():
	spechud.researchinfowindow1.open();
	spechud.researchinfowindow2.open();
def Spec_ShowResearch_Up():
	spechud.researchinfowindow1.close();
	spechud.researchinfowindow2.close();

def Spec_ShowGraphics_Down():
	if spechud.topBar.graphicspanel.isVisible():
		spechud.topBar.setVisible(False);
		spechud.topBar.graphicspanel.hide();		
	else:
		spechud.topBar.graphicspanel.show();
		spechud.topBar.setVisible(True);
def Spec_ShowGraphics_Up():
	pass; #TODO

def Spec_ToggleMinimap_Down():
	spechud.minimap.setVisible(not spechud.minimap.isVisible());
def Spec_ToggleMinimap_Up():
	pass;

def Spec_ToggleMinimapSize_Down():
	pass; #TODO
def Spec_ToggleMinimapSize_Up():
	pass; #TODO

def Spec_Screenshot_Down():
	screenshot();
def Spec_Screenshot_Up():
	pass;

def Spec_ReturnToLobby_Down():
	CL_RequestLobby();
def Spec_ReturnToLobby_Up():
	pass;

def Spec_UnitSelection_Down():
	CL_RequestLoadout();
def Spec_UnitSelection_Up():
	pass;


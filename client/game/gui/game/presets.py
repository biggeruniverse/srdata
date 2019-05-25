# copyright (c) 2011 savagerebirth.com
# this module handles loadout presets

from silverback import *;
import savage;
import math;
import re;

class Preset():
	PRESET_PATTERN = re.compile(r"""
	(?P<key>\w+)
	:(?P<value>\w+)
	(:
		(?P<quantity>\w+)
	)?
	""",re.VERBOSE);
	
	PRESET_NAME_FILTER = re.compile(r"[a-zA-Z]");
	
	def __init__( self, filepath ):
		data = {};
		file = File_Open( filepath , "r");
		for line in File_ReadLines(file):
			match = self.PRESET_PATTERN.match(line).groupdict();
			if match["quantity"] == None:
				data[match["key"]] = match["value"];
			else:
				data[match["key"]] = ( match["value"], int(match["quantity"]) );
		File_Close(file);
		
		self.race, self.unit = data["race"], data["unit"];
		self.name = "";
		for char in data["name"]:
			self.name += char if self.PRESET_NAME_FILTER.match(char) != None else " "
		self.items = [];
		
		slot = 0;
		while str(slot) in data:
			self.items.append( data[ str(slot)] );
			slot += 1;
		
	def request( self ):
		if self.unit != "":
			CL_RequestUnit( self.unit );
		
		i=0;
		for item in self.items:
			type, quantity = item[0], item[1];
			if type != "":
				CL_RequestGiveback(i);
				for j in range(quantity):
					CL_RequestGive( type );
			i += 1;

class PresetWindow( glass.GlassWindow ):
	def __init__(self):
		#FIXME the dropmenu isn't clickable when it's dropped down and the window
		
		glass.GlassWindow.__init__(self);
		
		self.input = glass.GlassTextField();
		self.input.setSizePct(0.18,0);
		self.input.setHeight(inputLineHeight);
		
		self.setWidth( self.input.getWidth() + 20);
		
		self.dropdown = glass.GlassDropMenu();
		self.dropdown.setWidth( self.input.getWidth() );
		self.dropdown.addSelectionListener(self);
		self.add( self.dropdown, 10 , 10 );
		self.add( self.input, 10, self.dropdown.getY() + self.dropdown.getHeight() + 10 );
		
		self.action = glass.GlassButton("Action!");
		self.add( self.action, 10, self.input.getY() + self.input.getHeight() + 10 );
		
		self.cancel = glass.GlassButton("Cancel");
		self.cancel.setClickAction("gblPresetManager.window.close()");
		self.add( self.cancel, self.getWidth() - self.cancel.getWidth() - 10, self.action.getY() );
		
		self.setHeight( self.getTitleBarHeight() + 10 + self.action.getY() + self.action.getHeight() );

	def show( self, typenm):
		if typenm == "new":
			self.setCaption("New Preset");
			self.dropdown.setVisible(0);
			self.input.setVisible(1);
			self.input.setText("New Preset");
			self.action.setCaption("Create");
			
			self.action.setClickAction( """
if gblPresetManager.window.input.getText() != '':
	gblPresetManager.newPreset(gblPresetManager.window.input.getText() );
	gblPresetManager.window.close(); """);
		elif typenm == "rename":
			self.setCaption("Rename Preset");
			self.dropdown.setVisible(1);
			self.input.setVisible(1);
			self.input.setText("New Name");
			self.action.setCaption("Rename");
			
			self.action.setClickAction( """
if gblPresetManager.window.input.getText() != '':
	gblPresetManager.renamePreset( gblPresetManager.selectedPreset.name , gblPresetManager.window.input.getText() );
	gblPresetManager.window.close();
""" );
			
			self.dropdown.clear();
			for presetName in gblPresetManager.dict.keys():
				self.dropdown.addOption(presetName, presetName);
			
		elif typenm == "delete":
			self.setCaption("Delete Preset");
			self.dropdown.setVisible(1);
			self.input.setVisible(0);
			self.action.setCaption("Delete");
			
			self.action.setClickAction("""
gblPresetManager.deletePreset( gblPresetManager.selectedPreset.name );
gblPresetManager.window.close();
""");
			self.dropdown.clear();
			for presetName in gblPresetManager.dict.keys():
				self.dropdown.addOption(presetName,presetName);
			
		self.setVisible(1);
		self.requestModalFocus();
		self.centerWindow();

	def onValueChanged(self,e):
		if e.widget.getSelectedValue() == None:
			gblPresetManager.selectedPreset = gblPresetManager.EMPTY_PRESET;
		else:
			gblPresetManager.selectedPreset = gblPresetManager.dict[e.widget.getSelectedValue()];

	def close(self):
		self.releaseModalFocus();
		self.setVisible(0);



class PresetManager( glass.GlassContainer ):
	EMPTY_PRESET_NAME = "__None__";

	def __init__(self):
		glass.GlassContainer.__init__(self);
		
		self.label = glass.GlassLabel("Presets: ");
		self.add(self.label);
		
		self.new = glass.ImageButton("new", "/gui/standard/icons/plus.s2g");
		self.new.setClickAction("gblPresetManager.window.show('new')");
		self.add(self.new);
		
		self.delete = glass.ImageButton("delete", "/gui/standard/icons/minus.s2g");
		self.delete.setClickAction("gblPresetManager.window.show('delete')");
		self.add(self.delete);
		
		self.dropdown = glass.GlassDropMenu();
		self.dropdown.addSelectionListener(self);
		self.add(self.dropdown);
		
		self.window = PresetWindow();
		self.window.centerWindow();
		self.window.setVisible(0);
		
		self.dict = OrderedDict();
		self.currentPreset = self.EMPTY_PRESET;
		self.selectedPreset = self.EMPTY_PRESET;
		
		self.label.setX(0);
		self.new.setX( self.label.getX() + self.label.getWidth() );
		self.dropdown.setX( self.new.getX() + self.new.getWidth() + 4);
		self.delete.setX( self.dropdown.getX() + self.dropdown.getWidth() + 4);
		self.setWidth( self.delete.getX() + self.delete.getWidth()); 
		
		widgets = (self.label, self.new, self.dropdown, self.delete);
		heights = [w.getHeight() for w in widgets];
		self.setHeight( max(*heights) );
		
		for w in widgets:
			y = self.getHeight() - w.getHeight();
			w.setY( y//2 );
	
	def reloadPresets(self):
		self.dict = OrderedDict();
		paths = File_ListFiles("/presets","*.prs",0);
		for path in paths:
			preset = Preset(path);
			self.dict[preset.name] = preset;
			
		#POSSIBLY NEEDED sort the ordered dictionary by key alphabetically

		self.dropdown.clear();
		teamNo = savage.getLocalPlayer().getTeam();
		raceName = savage.Team( teamNo ).getRace();
		availablePresets = [preset for preset in self.dict.itervalues() if preset.race == raceName];
		self.dropdown.addOption("None", self.EMPTY_PRESET_NAME);
		self.dropdown.setSelectedValue("None");
		#select the EMPTY_PRESET option for consistency
		for preset in availablePresets:
			self.dropdown.addOption(preset.name, preset.name);
			self.window.dropdown.addOption(preset.name, preset.name);
	
	def onValueChanged(self, e):
		value = e.widget.getSelectedValue();
		if value != self.EMPTY_PRESET_NAME:
			self.requestPreset( value );
		else:
			self.currentPreset = self.EMPTY_PRESET;
	
	def newPreset( self, name):
		filteredname = "";
		for char in name:
			filteredname += char if Preset.PRESET_NAME_FILTER.match(char) else "_";
		name = filteredname;
		file = File_Open( "/presets/"+name+".prs", "w");
		File_Write(file, "name:"+name+"\r\n");
		
		player = savage.getLocalPlayer();
		unit = player.getType().getName();
		race = savage.Team( player.getTeam() ).getRace();

		File_Write(file, "race:"+race+"\r\n");
		File_Write(file, "unit:"+unit+"\r\n");
		
		for i in range(5): #well, modders won't like this
			slot_objType = player.getInventorySlot(i);
			ammo = player.getAmmoSlot(i);
			name = slot_objType.getName() if slot_objType != None else "";
			File_Write(file, str(i) + ":" + name);
			if ammo != None:
				quantity = int(math.ceil(ammo/slot_objType.getValue("ammoStart")));
			else: 
				quantity = 1;
			File_Write(file, ":"+str(quantity) + "\r\n");
		
		File_Close(file);

		self.reloadPresets();
	
	def deletePreset( self, name):
		if name == self.EMPTY_PRESET_NAME:
			return;
		filteredname = "";
		for char in name:
			filteredname += char if Preset.PRESET_NAME_FILTER.match(char) else "_";
		name = filteredname;
		File_Delete("/presets/"+name+".prs");
		self.reloadPresets();
		#delete the file, and reload the presets? or just delete the file and edit the ordered dict
		
	def renamePreset( self, oldname, newname):
		if oldname == self.EMPTY_PRESET_NAME:
			return;
		#if this is called, it will load/request the preset too
		#it'd probably be easier to rename the file and reload everything
		self.requestPreset(oldname);
		self.deletePreset(oldname);
		self.newPreset(newname);
	
	def requestPreset( self, name):
		preset = self.dict[name];
		preset.request();
		self.currentPreset = preset;
		
	def execute(self):
		#called from loadout.onShow()
		if self.currentPreset != self.EMPTY_PRESET:
			self.currentPreset.request();

class EMPTY_PRESET:
	name = PresetManager.EMPTY_PRESET_NAME;

PresetManager.EMPTY_PRESET = EMPTY_PRESET;

gblPresetManager = PresetManager();

#copyright 2011 savagerebirth.com
#this file bind actions to key numbers
#for special keys, see http://guichan.sourceforge.net/api/0.8.1/classgcn_1_1Key.html#e6310e95e8749f3310c6ddf06a423b64
#single letters or characters can be converted to (ascii) numbers by using ord()
#left, right, middle mouse is 200, 201, 202 respectively
#REMEMBER to denote an tuple of length 1 add a trailing comma
#the empty tuple is ()

player = {
	"Move Forward":					[glass.Key.UP, ord("W")], 
	"Move Backward":				[glass.Key.DOWN, ord("S")],
	"Move Left":					[glass.Key.LEFT, ord("A")],
	"Move Right":					[glass.Key.RIGHT, ord("D")],
	"Jump":							[glass.Key.SPACE, glass.Key.LEFT_CONTROL,glass.Key.RIGHT_CONTROL],
	"Sprint":						[glass.Key.LEFT_SHIFT],
	
	"Attack / Action":				[200], #left mouse
	"Block / Leap":					[201], #right mouse
	"Rapid Attack":					[ord("R")],
	"Auto-Attack Toggle":			[glass.Key.PAGE_DOWN],
	
	"Select Primary Weapon":		[ord("1")],
	"Select Secondary Weapon":		[ord("2")],
	"Select Item 1":				[ord("3")],
	"Select Item 2":				[ord("4")],
	"Select Item 3":				[ord("5")],
	"Select Next Item/Weapon":		[], #TODO MouseWheelUp
	"Select Previous Item/Weapon":	[], #TODO MouseWheelDown
	
	"Enter Building":				[ord("E")],
	"Officer Mark":					[ord("F")],
	"Officer Mark Last Enemy":		[ord("G")],
	"Eject from Siege":				[ord("X")],
	"Unit Selection":				[ord("L")],
	"Request Buff 1":				[],
	"Request Buff 2":				[],
	"Request Buff 3":				[],
	"Zoom":							[ord("Z")],
	
	"Vote Yes":						[glass.Key.F1],
	"Vote No":						[glass.Key.F2],
	"Ignore Vote":					[glass.Key.F3],
	"Chat (All)":					[ord("T")],
	"Chat (Team)":					[ord("Y")],
	"Chat (Commander)":				[ord("U")],
	"Chat (Squad)":					[ord("I")],
	"Voice Chat":					[ord("V")],
	"Show Chat History":			[ord("B")],
	
	"Show Scoreboard":				[glass.Key.TAB],
	"Show Accuracy":				[glass.Key.END],
	"Show Research" :				[],
	"Show Graphics Options":		[glass.Key.DELETE],
	"Toggle Resources":				[],
	"Toggle Minimap":				[ord("M")],
	"Toggle Minimap Size":			[ord("N")],
	"Screenshot":					[glass.Key.F9],
	"Return to Lobby":				[glass.Key.ESCAPE]
	
};

comm = {
	"Scroll Up":					[glass.Key.UP, ord("W")],
	"Scroll Down":					[glass.Key.DOWN, ord("S")],
	"Scroll Left":					[glass.Key.LEFT, ord("A")],
	"Scroll Right":					[glass.Key.RIGHT, ord("D")],
	"Zoom In":						[], #TODO MouseWheelUp
	"Zoom Out":						[], #TODO MouseWheelDown
	"Rotate View CCW":				[ord(",")],
	"Rotate View CW":				[ord(".")],
	"Default View":					[glass.Key.END],
	
	"Vote Yes":						[glass.Key.F1],
	"Vote No":						[glass.Key.F2],
	"Hide Vote":					[glass.Key.F3],
	"Chat (All)":					[ord("T")],
	"Chat (Team)":					[ord("Y")],
	"Voice Chat":					[ord("V")],
	"Show Chat History":			[ord("H")],
	
	"Rotate Building CCW":			[ord("Q")],
	"Rotate Building CW":			[ord("E")],
	
	"Go To Base":					[glass.Key.HOME],
	"Go To Idle Worker":			[ord("I")],
	"Go To Last Message":			[glass.Key.SPACE],
	"Go To Officers":				[],
	"Go To Officer 1":				[],
	"Go To Officer 2":				[],
	"Go To Officer 3":				[],
	
	"Show Scoreboard":				[glass.Key.TAB],
	"Show Unit List":				[glass.Key.TAB],
	"Toggle Research":				[ord("R")],
	"Toggle Minimap":				[ord("M")],
	"Toggle Minimap Size":			[ord("N")],
	"Screenshot":					[glass.Key.F9]
	
};

spec = {
	"Move Forward":					[glass.Key.UP, ord("W")], 
	"Move Backward":				[glass.Key.DOWN, ord("S")],
	"Move Left":					[glass.Key.LEFT, ord("A")],
	"Move Right":					[glass.Key.RIGHT, ord("D")],
	"Move Up":						[glass.Key.SPACE, glass.Key.LEFT_CONTROL,glass.Key.RIGHT_CONTROL],
	"Move Faster":					[glass.Key.LEFT_SHIFT],	
		
	"Vote Yes":						[glass.Key.F1],
	"Vote No":						[glass.Key.F2],
	"Ignore Vote":					[glass.Key.F3],
	"Chat (All)":					[ord("T")],
	"Chat (Team)":					[ord("Y")],
	"Voice Chat":					[ord("V")],
	"Show Chat History":			[ord("B")],
	
	"Show Scoreboard":				[glass.Key.TAB],
	"Show Research" :				[ord("R")],
	"Show Graphics Options":		[glass.Key.DELETE],
	"Toggle Minimap":				[ord("M")],
	"Toggle Minimap Size":			[ord("N")],
	"Screenshot":					[glass.Key.F9],
	"Return to Lobby":				[glass.Key.ESCAPE],
	"Unit Selection":				[ord("L")]
	
};

maps = [player, comm, spec];
#this is what actually gets used. note the order!

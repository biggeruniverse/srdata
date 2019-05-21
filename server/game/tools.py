#(c) 2010 savagerebirth.com

#from threading import Thread;
from silverback import *;
import time;
dumpstring = "";

def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named);
	return type('Enum', (), enums);

def printList( list ):
	for item in list:
		con_println("^g"+ item + "\n" );

def writeList( list, filename = "writeListOutput.txt"):
	#NB this dumpstring is local to writeList()
	dumpstring = "writeList output:\n"
	list = map( lambda x: str(x) , list);
	dumpstring += "\n".join(list);
	try:
		f = open(filename, "w");
		f.write(dumpstring);
	except:
		con_println("^rError: writeList() either couldn't open or write to " +filename +"\n");
	finally:
		f.close();
  

def dirOutput(string, console, file):
	global dumpstring;
	if console: con_println(string);
	if file: dumpstring += string;

def consoledir( obj = None, console = True, file = False, filename = "filedir.txt" ):
	if obj == "silverback":
		import silverback;
		obj = silverback;
	elif obj == "savage":
		try:
			import savage;
			obj = savage;
		except ImportError:
			con_println("^yWarning savage.txt not written - savage module not loaded yet");
			obj = None; 

	elif obj == None:
		dirOutput("consoledir() called without an argument - maybe use tools.printList(dir())?\n", console, file);
		return;
	
	global dumpstring;
	dumpstring = "";
	
	try:
		objName = obj.__name__;
	except AttributeError:
		objName = "Something without a __name__";
	
	dirOutput("\n === consoledir() called to inspect ^y%s^w ===\n\n" % objName , console, file );
	
	names = dir(obj);
	
	for name in names:
		typestring = type(getattr(obj, name)).__name__;
		
		try: typeformatted = colorLookup[ typestring ];
		except KeyError: typeformatted = "^r%s : " % typestring;
		dirOutput( "%s%s\n" % (typeformatted, name) , console, file );
	
	if file:
		try:
			f = open(filename, "w");
			#I don't seem to be able to let filename include a folder without the above line causing an error
			#e.g. filename = "myfolder/myfile.txt";
			f.write(dumpstring);
		finally:
			f.close();

glassProperties = ["Graphics", "ImageButton","Color", "Key"];

def glassInfoDump():
	global glassProperties;
	import glass;
	itemsToParse = dir(glass);
	
	for widgettype in itemsToParse:
		if (widgettype.startswith("Glass") and widgettype.find("swig") == -1) or widgettype in glassProperties:
			consoledir(obj = getattr(glass, widgettype), console = False, file = True, filename = widgettype+".txt");

def silverbackInfoDump():
		consoledir("silverback", console = False, file = True, filename = "silverback.txt");
	
def savageInfoDump():
	#WARNING if you call this before game.dll /savage module is loaded BAD STUFF WILL HAPPEN
	#TODO consoledir() the other classes too
	consoledir( "savage", console = False, file = True, filename = "savage.txt");
	
def APIInfoDump():
	#WARNING if you call this before game.dll /savage module is loaded BAD STUFF WILL HAPPEN
	silverbackInfoDump();
	savageInfoDump();

"""
^r - a type not in the lookup dict
^y - functions / methods / things you can call;
do a test with callable(); ?
^c - tuples and lists
^589 - dictionaries 
^g - strings
^m - numbers
^w booleans
^666 anything else
"""

colorLookup = {
	"classobj"      : "^yClass     : ",
	"function"      : "^yFunction  : ",
	"instancemethod": "^yMethod    : ",
	"method-wrapper": "^yMethod    : ",
	"method_descriptor": "^yMethod    : ",
	"builtin_function_or_method": "^yFunc/Meth : ",
	"str"           : "^gString    : ",
	"int"           : "^mInteger   : ",
	"float"         : "^mFloat     : ",
	"list"          : "^cList      : ",
	"tuple"         : "^cTuple     : ",
	"bool"          : "^wBoolean   : ",
	"dict"          : "^589Dictionary: ",
	"dictproxy"     : "^589Dictionary: ",
	"module"		: "^985Module    : ",
	"NoneType"      : "^666None      : ",
	"type"          : "^666Type      : ",
};

def showImportPaths():
	import sys;
	printList( sys.path );

def widgetInfoDump( widget, name = None ):
	if name != None: con_println("Widget Location for "+str(name)+"\n");
	con_println("X: " + str(widget.getX()) + " Y: " + str(widget.getY()) +"\n");
	con_println("Width: " + str(widget.getWidth()) + " Height: " + str(widget.getHeight()) +"\n");

colorCodes = {
	"r": "922",
	"g": "090",
	"b": "009",
	"c": "099",
	"m": "909",
	"y": "990",
	"k": "000",
	"w": "999",
}

def savColorToGlass( color, alpha = 255):
	import glass;
	if color.startswith("^"):
		color = color[1:]
	
	if color in colorCodes:
		color = colorCodes[color];
	
	return glass.Color( int(color[0]) * 255//10, int(color[1]) * 255//10, int(color[2]) * 255//10, alpha);
	
def glassColorToSav( r = 0, g = 0, b = 0 ):
	output = "^";
	if isinstance(r, glass.Color):
		r = r.r;
		g = r.g;
		b = r.b;

	for component in [r,g,b]:
		value = str(component * 10 // 255.0);
		if value == "10": value = "9";
		output += value;
	return output;

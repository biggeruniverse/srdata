#(c) 2010 savagerebirth.com

#from threading import Thread;
from silverback import *;
from types import FrameType;
import time;
import colorsys;
import gc;

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
	elif obj == "yeti":
		try:
			import yeti;
			obj = yeti;
		except ImportError:
			con_println("^yWarning yeti.txt not written - yeti module not loaded yet");
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

def yetiInfoDump():
	consoledir("yeti", console = False, file = True, filename = "yeti.txt");

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
	con_println("isVisible: "+str(widget.isVisible())+"\n");
	con_println("Alpha: "+str(widget.getAlpha())+"\n");

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
	import glass;
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
	

def HSLColor( h, s, l, alpha= 255):
	if h > 1:  h /= 360.0
	if s > 1:  s /= 255.0
	if l > 1:  l /= 255.0
	import glass;
	r, g, b = colorsys.hls_to_rgb(h,l,s)
	return glass.Color(int(r*255),int(g*255),int(b*255),alpha);

def run_gc():
	import gc;
	con_dprintln("running GC...\n");

	gc.set_debug(gc.DEBUG_SAVEALL);

	gc.collect(0);

	con_dprintln("uncollected:\n");

	for i,o in enumerate(gc.garbage):
        	con_dprintln(str(i)+". "+str(type(o))+"\n");

# from an ActiveState Python recipe for finding cyclic references

def recurseCycles(objects, obj, start, all, path, progress):
	if progress:
		con_println("%d\n", len(all));	

	all[id(obj)] = None;

	referents = gc.get_referents(obj);
	for referent in referents:
		if referent is start:
			for i, step in enumerate(path):
				next = path[(i + 1) % len(path)];
				con_println("    %s -- " % str(type(step)));
				if isinstance(step, dict):
					for key, val in step.items():
						if val is next:
							con_println("[%s]" % repr(key));
							break;
						if key is next:
							con_println("[key] = %s" % repr(val));
							break;
				elif isinstance(step, list):
					con_println("[%d]" % step.index(next));
				elif isinstance(step, tuple):
					con_println("[%d]" % list(step).index(next));
				else:
					con_println(repr(step));
				con_println(" ->\n");
			con_println("\n");
		elif referent is objects or isinstance(referent, FrameType):
			continue;
		elif id(referent) not in all:
			recurseCycles(objects, referent, start, all, path + [obj], progress);

def printCycles(objs, progress=False):
	con_println("Printing cyclical references:\n");
	for obj in objs:
		con_println("Examining: %r\n" % obj);
		recurseCycles(objs, obj, obj, {}, [], progress);


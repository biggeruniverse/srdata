from silverback import *;
import gc;

con_dprintln("running GC...\n");

gc.set_debug(gc.DEBUG_SAVEALL);

gc.collect();

con_dprintln("uncollected:\n");

for i,o in enumerate(gc.garbage):
	con_dprintln(str(i)+". "+str(type(o))+"\n");
	for r in gc.get_referrers(o):
		con_dprintln("    "+str(type(r))+"\n");

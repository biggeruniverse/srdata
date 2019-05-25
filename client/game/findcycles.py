import gc;
import tools;

if gc.isenabled():
	con_println("yes we are\n");
else:
	con_println("no we are not\n");

tools.printCycles(gc.garbage, True);

con_println("GC has trash:\n");

for obj in gc.garbage:
	referents = gc.get_referents(obj);

	con_println("object %r has %d refcount\n" % repr(obj), len(referents));
	for ref in referents:
		con_println("object "+str(ref)+"\n");

# (c) 2010 savagerebirth.com
#
# Various defines and globals for savage module

resourceNames = ["NULL", "stone", "gold", "electric", "magnetic", "chemical", "fire", "strata", "entropy"];

def getLocalTeam():
	return savage.Team(savage.getLocalPlayer().getTeam());

def registerRefCommand(cl):
	return savage.registerCommandHandler(cl.CMD, cl.__name__, cl.DESCRIPTION, cl.GROUPS);

def getResourceId(name):
	for i,n in enumerate(savage.resourceNames):
		if n == name:
			return i;
	return 0;

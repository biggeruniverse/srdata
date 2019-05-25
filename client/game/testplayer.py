# (c) 2010 savagerebirth.com
#
# Just a small scratch file for testing various game API
#

from silverback import *;
import savage;

player = savage.getLocalPlayer();
#player = savage.getPlayerByName("big");

con_println("my health is: "+str(player.getHealth())+"\n");

con_println("I am a "+player.getType().getValue("description")+"\n");
con_println("I am on team "+str(player.getTeam())+"\n");

con_println("My weapons stats are as follows:\n");

statsList = player.getAccuracy();

for k in statsList[0].keys():
	con_println(k+": "+str(statsList[0][k])+" "+str(statsList[1][k])+" "+str(statsList[2][k])+"\n");

player.clearInventory();

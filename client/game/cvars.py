# (c) 2010 savagerebirth.com
# cvars used by the gui that are NOT hardcoded

#cl_blockleapswitch, was _block_switch
#if 1, the bindAction "Block / Leap" will always block, even if an item or ranged weapon is selected
cvar_register("cl_blockLeapSwitch",CVAR_SAVECONFIG ,"1");

#cl_showfpsserver
#if 1, the fps windows will show server fps, provided cl_showfps is 1
cvar_register("cl_showfpsserver",CVAR_SAVECONFIG,"0");
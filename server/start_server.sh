#!/bin/sh

######################################################
######################################################
##          Savage: Rebirth Startup Script          ##
##                                                  ##
##            (c) 2012 savagerebirth.com            ##
######################################################
######################################################

uid=`id -r -u`
gid=`id -r -g`
base=`dirname $0`

if [ "$uid" -eq "0" ] || [ "$gid" -eq "0" ]; then
	echo "Running as root is dangerous!"
	echo "Run as a non-privileged user to avoid root attacks"
	exit 1
fi

while :; do

	echo "Starting from $base"
	echo "Starting server..."

	cd $base
	LD_LIBRARY_PATH=libs/ ./savage.bin

	echo
	echo "Restarting in 10 seconds, ctrl-c to end"
	sleep 10
done

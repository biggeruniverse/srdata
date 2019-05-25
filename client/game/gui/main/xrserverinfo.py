# (c) 2011-2014 savagerebirth.com

from silverback import *;
import struct
import socket

sock = None

def Init():
	xrserverinfo.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	xrserverinfo.sock.setblocking(0)
	xrserverinfo.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def GetInfo(address, port, extended=True):
	packet = ""
	
	if extended is True:
		packet = struct.pack("!BI", 0xCE, 0x80000000 | Host_Milliseconds())
	else:
		packet = struct.pack("!BI", 0xC8, Host_Milliseconds())
		
	xrserverinfo.sock.sendto(packet, (address, port))

def ProcessPackets():
	msg=""
	con_println("checkmsg\n");
	try:
		msg, fromaddr = xrserverinfo.sock.recvfrom(2048)
	except:
		con_println("will check again\n")
	else:
		con_println("gotmsg "+msg+"\n")
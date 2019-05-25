# (c) 2011 savagerebirth.com

import savage;
import math;
from vectors import Vec3;

class Zone:
	def __init__(self, i):
		self.zoneId = i;
		self.listeners = [];

	def getName(self):
		return savage.zone_getname(self.zoneId);

	def addListener(self, obj):
		self.listeners.append(obj);

	def _onObjectEnter(self, obj):
		for l in self.listeners:
			l.onEnter(obj);

	def _onObjectExit(self, obj):
		for l in self.listeners:
			l.onExit(obj);


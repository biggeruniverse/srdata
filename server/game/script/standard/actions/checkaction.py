# (c) 2013 savagerebirth.com

from silverback import *

class CheckAction(Action):
	def __init__(self, obj, value):
		self.obj = obj
		self.value = value
		return Action.__init__(self)

	def run(self):
		if self.obj is not self.value:
			self.parent.stop()

	def is_done(self):
		return True


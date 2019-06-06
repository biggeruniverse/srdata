# (c) 2011 savagerebirth.com

class ActivateAction(Action):
	def __init__(self, obj):
		self.obj = obj
		return super().__init__()

	def run(self):
		self.obj.setState("activate")


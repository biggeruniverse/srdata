class human_relocater_trigger(GameItem):
	def onUse(self, user, target):
		user.teleport(user.getLink());
		user.getLink().die();

"""
@use
!teleport target link
!die link

#@use
#!toss target 20 1.0
###!teleport target base

##@toss
##!setstate self idle 10000 activate

##@activate
##!teleport owner here
##!die self
"""


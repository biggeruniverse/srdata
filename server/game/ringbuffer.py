# (c) 2010 savagerbirth.com
#
# A simple ring buffer implementation
#

class RingBuffer:
	def __init__(self,size_max):
		self.max = size_max
		self.data = []
		#the index of the oldest item in the buffer - where the buffer 'starts'
		self.cur=0
	
	def append(self,x):
		"""append an element at the end of the buffer"""
		if len(self.data) == self.max:
			self.data[self.cur]=x
			self.cur=(self.cur+1) % self.max
		else:
			self.data.append(x)

	def remove(self):
		"""removes the oldest item from the buffer"""
		return self.data.pop(self.cur)

	def get(self):
		""" return a list of elements from the oldest to the newest"""
		return self.data[self.cur:]+self.data[:self.cur]
	
	def __str__(self):
		"""Useful for debugging"""
		strlist = [ repr(item) for item in self.get() ];
		return("^g" + "\n^m".join( strlist ));
		


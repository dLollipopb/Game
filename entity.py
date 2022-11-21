class Entity:
	def __init__(self):
		self.tags=[]
	def __del__(self):
		delTags(self)
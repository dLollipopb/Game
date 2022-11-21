class Tags:
	def __init__(self):
		pass
class Tag:
	def __init__(self,name):
		self.objs=set()
tags=Tags()

def createTag(name):
	if not name in tags.__dict__:
		tags.__dict__[name]=set()

def addTag(name,obj):
	global tags
	if not "tags" in obj.__dict__:
		obj.tags=[]
	if not name in tags.__dict__:
		tags.__dict__[name]=set()
	tags.__dict__[name]|={obj}
	obj.tags.append(tags.__dict__[name])

def delTags(obj):
	global tags
	if "tags" in obj.__dict__:
		for i in obj.tags:
			i-={obj}
		obj.tags=set()
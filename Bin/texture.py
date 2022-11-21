import pygame,os

class Texture:
	def __init__(self):
		self.tex=None
		self.w=0
		self.h=0
		self.name="unknown"
	def load(self,path,name="unknown"):
		self.tex=pygame.image.load(path)
		self.w,self.h=self.tex.get_size()
		self.name=name
	def __str__(self):
		return "Texture("+self.name+")"
class Textures:
	def __init__(self):
		self.tex=[]
	def __call__(self,name):
		for i in self.tex:
			if i.name==name:
				return i
		raise Exception("Texture not found")
	def loadFromPath(self,path):
		if not os.path.exists(path):
			raise Exception("Path not found")
		for i in os.listdir(path):
			tex=Texture()
			tex.load(path+str("/")+i,i)
			self.tex.append(tex)
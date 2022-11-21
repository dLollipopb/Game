import pygame,sys
from tags import *

class Camera:
	def __init__(self):
		self.x=0.0
		self.y=0.0
		self.zoom=0.0
		createTag("movable")
		addTag("movable",self)
	def drawTexture(self,scr,obj):
		scr.blit(obj.tex.tex,(int(obj.x-self.x),int(obj.y-self.y)))

class Window:
	def __init__(self,settings):
		self.tags=[]
		createTag("simulated")
		createTag("draw")
		createTag("event")
		createTag("keydown")
		createTag("keyup")
		createTag("mousedown")
		createTag("movable")
		self.w=settings['width']
		self.h=settings['height']
		self.flags=0
		if settings["resizable"]:
			self.flags|=pygame.RESIZABLE
		self.scr=pygame.display.set_mode((self.w,self.h),self.flags)
		self.shouldclose=False
		self.clock=pygame.time.Clock()
		self.color=(0,0,0)
		self.camera=Camera()
	def close(self):
		self.shouldclose=True
	def loop(self):
		while not self.shouldclose:
			dt=self.clock.tick(60)/1000.0
			for i in tags.simulated:
				i.run(dt)
			for i in pygame.event.get():
				if i.type==pygame.QUIT:
					self.close()
				if i.type==pygame.KEYDOWN:
					for j in tags.keydown:
						j.keydown(i.key)
				if i.type==pygame.KEYUP:
					for j in tags.keyup:
						j.keyup(i.key)
				if i.type==pygame.MOUSEBUTTONDOWN:
					for j in tags.mousedown:
						j.mousedown(i.button)
			self.scr.fill(self.color)
			for i in sorted(tags.draw,key=lambda i:i.drawpriority,reverse=True):
				i.draw(self.scr,self.camera)
			pygame.display.flip()
		pygame.quit()
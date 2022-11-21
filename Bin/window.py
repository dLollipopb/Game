import pygame,sys
from tags import *

class Camera:
	def __init__(self,win):
		self.x=0.0
		self.y=0.0
		self.zoom=1.0
		self.win=win
		createTag("movable")
		addTag("movable",self)
	def getAbsoluteSize(self,size):
		return size*self.zoom
	def getWindowPos(self,x,y):
		return (int((x-self.x)*self.zoom+self.win.w/2.0),int((y-self.y)*self.zoom+self.win.h/2.0))
	def getAbsolutePos(self,x,y):
		return (float(x)-self.win.w/2.0)/self.zoom+self.x,(float(y)-self.win.h/2.0)/self.zoom+self.y
	def drawTexture(self,scr,obj):
		size=(int(obj.tex.w*self.zoom),int(obj.tex.h*self.zoom))
		scr.blit(pygame.transform.scale(obj.tex.tex,size),self.getWindowPos(obj.x,obj.y))

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
		self.camera=Camera(self)
	def close(self):
		self.shouldclose=True
	def loop(self):
		while not self.shouldclose:
			dt=self.clock.tick(60)/1000.0
			for i in tags.simulated:
				i.run(dt,self.camera)
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
import pygame,sys

class Window:
	def __init__(self,settings):
		self.w=settings['width']
		self.h=settings['height']
		self.flags=0
		if settings["resizable"]:
			self.flags|=pygame.RESIZABLE
		self.scr=pygame.display.set_mode((self.w,self.h),self.flags)
		self.shouldclose=False
		self.drawing|=set()
	def draw(self,obj):
		self.drawing|={obj}
	def undraw(self,obj):
		self.drawing-={obj}
	def close(self):
		self.shouldclose=True
	def loop(self):
		while not self.shouldclose:
			for i in pygame.event.get():
				if i.type==pygame.QUIT:
					self.close()
			pygame.display.flip()
		pygame.quit()
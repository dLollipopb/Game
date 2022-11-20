import pygame,sys

class Window:
	def __init__(self,w,h):
		self.w=w
		self.h=h
		self.flags=0
		self.scr=None
	def resizable(self,t):
		if t:
			self.flags|=pygame.RESIZABLE
		else::
			self.flags-=pygame.RESIZABLE
	def create(self):
		self.scr=pygame.display.set_mode((w,h),self.flags)
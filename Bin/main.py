import pygame,sys,math
from settings import settings
from window import Window
from tags import *
from texture import *

win=Window(settings)
textures=Textures()
textures.loadFromPath("../Resources/Textures/coridors")
textures.loadFromPath("../Resources/Textures/interface")
textures.loadFromPath("../Resources/Textures/rooms")

class KeyEscape:
	def __init__(self):
		pass
	def keydown(self,key):
		if key==pygame.K_ESCAPE:
			win.close()

keyesc=KeyEscape()
addTag("keydown",keyesc)

class ConnectedTile:
	def update(self,right,down,left,up):
		tex=self.connectedtiletex
		if right.__class__==Room:
			tex+="1"
		else:
			tex+="0"
		if down.__class__==Room:
			tex+="1"
		else:
			tex+="0"
		if left.__class__==Room:
			tex+="1"
		else:
			tex+="0"
		if up.__class__==Room:
			tex+="1"
		else:
			tex+="0"
		self.tex=textures(tex+".png")

class Room(ConnectedTile):
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.drawpriority=10
		self.connectedtiletex="s_rooms_"
		self.tex=textures(self.connectedtiletex+"0000.png")
		addTag("draw",self)
	def remove(self):
		delTags(self)
	def draw(self,scr,camera):
		camera.drawTexture(scr,self)

class CameraMoving:
	def __init__(self,camera):
		self.tags=[]
		self.camera=camera
		self.ux=0.0
		self.uy=0.0
		self.kd=False
		self.ks=False
		self.ka=False
		self.kw=False
		self.speed=1000.0
		addTag("keydown",self)
		addTag("mousedown",self)
		addTag("keyup",self)
		addTag("simulated",self)
	def run(self,dt,camera):
		if self.kd:
			self.ux+=dt*self.speed/self.camera.zoom
		if self.ks:
			self.uy+=dt*self.speed/self.camera.zoom
		if self.ka:
			self.ux-=dt*self.speed/self.camera.zoom
		if self.kw:
			self.uy-=dt*self.speed/self.camera.zoom
		self.camera.x+=self.ux*dt
		self.camera.y+=self.uy*dt
		self.ux*=0.9
		self.uy*=0.9
	def mousedown(self,button):
		if button==4:
			self.camera.zoom*=1.1
		if button==5:
			self.camera.zoom/=1.1
	def keydown(self,key):
		if key==pygame.K_d or key==pygame.K_RIGHT:
			self.kd=True
		if key==pygame.K_s or key==pygame.K_DOWN:
			self.ks=True
		if key==pygame.K_a or key==pygame.K_LEFT:
			self.ka=True
		if key==pygame.K_w or key==pygame.K_UP:
			self.kw=True
	def keyup(self,key):
		if key==pygame.K_d or key==pygame.K_RIGHT:
			self.kd=False
		if key==pygame.K_s or key==pygame.K_DOWN:
			self.ks=False
		if key==pygame.K_a or key==pygame.K_LEFT:
			self.ka=False
		if key==pygame.K_w or key==pygame.K_UP:
			self.kw=False

class ConstructionGrid:
	def __init__(self):
		self.grid={}
	def update(self,x,y):
		if (int(x),int(y)) in self.grid:
			side=[]
			if (int(x+1),int(y)) in self.grid:
				side.append(self.grid[(int(x+1),int(y))])
			else:
				side.append(None)
			if (int(x),int(y+1)) in self.grid:
				side.append(self.grid[(int(x),int(y+1))])
			else:
				side.append(None)
			if (int(x-1),int(y)) in self.grid:
				side.append(self.grid[(int(x-1),int(y))])
			else:
				side.append(None)
			if (int(x),int(y-1)) in self.grid:
				side.append(self.grid[(int(x),int(y-1))])
			else:
				side.append(None)
			self.grid[(int(x),int(y))].update(*side)
	def add(self,x,y,obj):
		if not (int(x),int(y)) in self.grid:
			self.grid[(int(x),int(y))]=obj
			self.update(int(x),int(y))
			self.update(int(x+1),int(y))
			self.update(int(x),int(y+1))
			self.update(int(x-1),int(y))
			self.update(int(x),int(y-1))
	def remove(self,x,y):
		if (int(x),int(y)) in self.grid:
			self.grid[(int(x),int(y))].remove()
			del self.grid[(int(x),int(y))]
			self.update(int(x+1),int(y))
			self.update(int(x),int(y+1))
			self.update(int(x-1),int(y))
			self.update(int(x),int(y-1))
	def exist(self,x,y):
		return (int(x),int(y)) in self.grid

class Building:
	def __init__(self,grid):
		self.x=0.0
		self.y=0.0
		self.cellsize=160.0
		self.textures=[textures("s_marker_construction_0.png"),
		textures("s_marker_construction_1.png"),textures("s_marker_construction_2.png")]
		self.tex=self.textures[1]
		addTag("mousedown",self)
		addTag("draw",self)
		addTag("simulated",self)
		self.drawpriority=0
		self.grid=grid
	def run(self,dt,camera):
		mx,my=pygame.mouse.get_pos()
		mx,my=camera.getAbsolutePos(mx,my)
		mx=int(mx//self.cellsize)*self.cellsize
		my=int(my//self.cellsize)*self.cellsize
		if self.grid.exist(mx/self.cellsize,my/self.cellsize):
			if self.tex.name!="s_marker_construction_2.png":
				self.tex=self.textures[2]
		else:
			if self.tex.name!="s_marker_construction_1.png":
				self.tex=self.textures[1]
	def mousedown(self,button):
		if button==1:
			x,y=self.x/self.cellsize,self.y/self.cellsize
			if not self.grid.exist(x,y):
				room=Room(self.x,self.y)
				grid.add(x,y,room)
		if button==3:
			x,y=self.x/self.cellsize,self.y/self.cellsize
			if self.grid.exist(x,y):
				grid.remove(x,y)
	def draw(self,scr,camera):
		mx,my=pygame.mouse.get_pos()
		mx,my=camera.getAbsolutePos(mx,my)
		mx=int(mx//self.cellsize)*self.cellsize
		my=int(my//self.cellsize)*self.cellsize
		self.x=mx
		self.y=my
		camera.drawTexture(scr,self)

grid=ConstructionGrid()
building=Building(grid)

camera_moving=CameraMoving(win.camera)
win.color=(0x29,0x1D,0x2B)

win.loop()
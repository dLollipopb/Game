import pygame,sys
from settings import settings
from window import Window

win=Window(settings['width'],settings['height'])
print pygame.RESIZABLE
while True:
	for i in pygame.event.get():
		if i.type==pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.flip()
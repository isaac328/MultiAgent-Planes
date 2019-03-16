import pygame
from pygame.locals import *
from plane import Plane


WINDOWWIDTH = 740
WINDOWHEIGHT = 580
FPS = 30



def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption('Plane Simulation')

	runSimulation()



def runSimulation():
	planes = [Plane(100, 100, 300, 1)]
	while True:
		# go through events
		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return True


		DISPLAYSURF.fill((0,0,0))
		for plane in planes:
			plane.move()
			pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (int(plane.x), int(plane.y)), 2)
		pygame.display.update()
		FPSCLOCK.tick(FPS)




if __name__ == '__main__':
	main()
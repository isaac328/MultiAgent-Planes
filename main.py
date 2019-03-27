import pygame
from pygame.locals import *
from plane import Plane
import math


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
	# the current planes in the simulation
	planes = [Plane(100, 100, 0, 1), Plane(400, 300, 240, 1)]
	while True:
		# go through events
		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return True
				# testing
				if event.key == K_t:
					planes[0].turn(40)

		DISPLAYSURF.fill((0,0,0))

		for plane1 in planes:
			for plane2 in planes:
				
				if plane1 is plane2:
					continue
				
				dist = math.sqrt((plane1.x - plane2.x)**2 + (plane1.y - plane2.y)**2)
				if dist <= plane1.exclusion_zone * 1.2:
					x_diff = plane1.x - plane2.x
					y_diff = plane1.y - plane2.y

					# if plane 2 is to the left and above plane 1
					if x_diff > 0 and y_diff > 0:
						pass
					# if plane 2 is to the right and above plane 1
					elif x_diff < 0 and y_diff > 0:
						pass
					# if plane 2 is to the left and below plane 1
					elif x_diff > 0 and y_diff < 0:
						pass
					# if plane 2 is to the right and below plane 1
					elif x_diff < 0 and y_diff < 0:
						pass

					

		
		for plane in planes:
			plane.move()
			pygame.draw.circle(DISPLAYSURF, (226, 57, 31), (int(plane.x), int(plane.y)), plane.exclusion_zone)
			pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (int(plane.x), int(plane.y)), 2)




		pygame.display.update()
		FPSCLOCK.tick(FPS)




if __name__ == '__main__':
	main()
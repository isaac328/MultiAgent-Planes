import pygame
from pygame.locals import *
from plane import Plane
import math
import random


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


def onSegment(p, q, r):
	if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
	   return True
	return False
  
#Q To find orientation of ordered triplet (p, q, r). 
#Q The function returns following values 
#Q 0 --> p, q and r are colinear 
#Q 1 --> Clockwise 
#Q 2 --> Counterclockwise 
def orientation(p, q, r):
	# See https://www.geeksforgeeks.org/orientation-3-ordered-points/ 
	# for details of below formula. 
	val = (q[1] - p[1]) * (r[0] - q[0]) -  (q[0] - p[0]) * (r[1] - q[1])
	if (val == 0):
		return 0  # colinear 
  
	if (val > 0):
		return 1
	else: 
		return 2 # clock or counterclock wise 
  
# The main function that returns true if line segment 'p1q1' 
# and 'p2q2' intersect. 
def doIntersect(p1, q1, p2, q2):
	# Find the four orientations needed for general and 
	# special cases 
	o1 = orientation(p1, q1, p2) 
	o2 = orientation(p1, q1, q2) 
	o3 = orientation(p2, q2, p1) 
	o4 = orientation(p2, q2, q1) 
  
	# General case 
	if (o1 != o2 and o3 != o4):
		return True
  
	# Special Cases 
	# p1, q1 and p2 are colinear and p2 lies on segment p1q1 
	if (o1 == 0 and onSegment(p1, p2, q1)):
		return True
  
	# p1, q1 and q2 are colinear and q2 lies on segment p1q1 
	if (o2 == 0 and onSegment(p1, q2, q1)):
		return True 
  
	# p2, q2 and p1 are colinear and p1 lies on segment p2q2 
	if (o3 == 0 and onSegment(p2, p1, q2)):
		return True 
  
	# p2, q2 and q1 are colinear and q1 lies on segment p2q2 
	if (o4 == 0 and onSegment(p2, q1, q2)):
		return True 
  
	return False # Doesn't fall in any of the above cases 



def runSimulation():
	# the current planes in the simulation
	#planes = [Plane(100, 100, 0, 1, (500,100)), Plane(400, 300, 240, 1, (200, 10))]
	planes = [Plane(50, 500, -55, 1, (500, 50)), Plane(500, 500, -85, 1, (20, 20))]
	#planes = [Plane(random.randint(0, 500), random.randint(0, 500), random.randint(0, 360), 1, (random.randint(0,500), random.randint(0,500))) for _ in range(10)]
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
			intersecting = False

			plane_1_x = plane1.x + (500 * math.cos(math.radians(plane1.heading)))
			plane_1_y = plane1.y + (500 * math.sin(math.radians(plane1.heading)))
			for plane2 in planes:

				if plane1 is plane2:
					continue

				# if plane1.turning_degrees > 0 or plane2.turning_degrees > 0:
				# 	continue

				plane_2_x = plane2.x + (500 * math.cos(math.radians(plane2.heading)))
				plane_2_y = plane2.y + (500 * math.sin(math.radians(plane2.heading)))

				dist = math.sqrt((plane1.x - plane2.x)**2 + (plane1.y - plane2.y)**2)
				if dist <= plane1.exclusion_zone * 2.2 and doIntersect((plane1.x, plane1.y), (plane_1_x, plane_1_y), (plane2.x, plane2.y), (plane_2_x, plane_2_y)):
					intersecting = True

					if orientation((plane1.x, plane1.y), (plane_1_x, plane_1_y), (plane2.x, plane2.y)) == 1:
						plane1.turn(-1)
						if orientation((plane2.x, plane2.y), (plane_2_x, plane_2_y), (plane1.x, plane1.y)) == 1:
							plane2.turn(1)
						elif orientation((plane2.x, plane2.y), (plane_2_x, plane_2_y), (plane1.x, plane1.y)) == 2:
							plane2.turn(-1)
					elif orientation((plane1.x, plane1.y), (plane_1_x, plane_1_y), (plane2.x, plane2.y)) == 2:
						plane1.turn(1)
						if orientation((plane2.x, plane2.y), (plane_2_x, plane_2_y), (plane1.x, plane1.y)) == 1:
							plane2.turn(1)
						elif orientation((plane2.x, plane2.y), (plane_2_x, plane_2_y), (plane1.x, plane1.y)) == 2:
							plane2.turn(-1)
			
			if not intersecting:
				if not onSegment((plane1.x, plane1.y), (plane_1_x, plane_1_y), plane1.target):
					if orientation((plane1.x, plane1.y), (plane_1_x, plane_1_y), plane1.target) == 1:
						plane1.turn(-1)
					elif orientation((plane1.x, plane1.y), (plane_1_x, plane_1_y), plane1.target) == 2:
						plane1.turn(1)
			

					

		
		for plane in planes:
			plane.move()
			# pygame.draw.circle(DISPLAYSURF, (226, 57, 31), (int(plane.x), int(plane.y)), plane.exclusion_zone)
			pygame.draw.circle(DISPLAYSURF, (0,0,255), plane.target, 5)
			pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (int(plane.x), int(plane.y)), 2)
			pygame.draw.line(DISPLAYSURF, (0, 255, 0), (plane.x, plane.y), (plane.x + (1000*math.cos(math.radians(plane.heading))), plane.y + (1000 * math.sin(math.radians(plane.heading)))))




		pygame.display.update()
		FPSCLOCK.tick(FPS)




if __name__ == '__main__':
	main()
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


# function to determine whether r is on the line segment
# between p and q
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
	#planes = [Plane(100, 100, 0, 1, (500,100)), Plane(400, 300, 240, 1, (200, 10))] # one plane coming into the path of another
	planes = [Plane(50, 500, -55, 1, (500, 50)), Plane(500, 500, -85, 1, (20, 20))] # intersection paths
	#planes = [Plane(100, 100, 0, 1, (500, 100)), Plane(500, 100, 180, 1, (100, 100))] # head on collision
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

		# go through all the planes currently in the simulation
		for plane1 in planes:
			# flag for if this plane (plane1) is on an intersecting path with another plane
			# set to false by default
			intersecting = False

			# These are the coordinates of a point on the path of the plane
			# Basically this is a point 500 pixels ahead of the plane on its current path
			# I use this to draw a line from the plane to this point, which is how the 
			# direction line (green line) is drawn. Also used to determine if two planes 
			# are on intersecting paths.
			plane1_x_high = plane1.x + (500 * math.cos(math.radians(plane1.heading)))
			plane1_y_high = plane1.y + (500 * math.sin(math.radians(plane1.heading)))

			# These are the coordinates of a point behind the plane path on the edge of the exclusion zone
			# we use this point as the beginning of the line segment instead of the actual coordinates of the plane
			# so that the planes do not get too close to each other and stay out of each others's exclusion zones
			plane1_x_low = plane1.x - (plane1.exclusion_zone * math.cos(math.radians(plane1.heading)))
			plane1_y_low = plane1.y - (plane1.exclusion_zone * math.sin(math.radians(plane1.heading)))

			# now we have to go through every other plane and check if theyre intersecting
			for plane2 in planes:
				
				# if the two planes are the same, obviously they cant be intersecting
				if plane1 is plane2:
					continue

				# if plane1.turning_degrees > 0 or plane2.turning_degrees > 0:
				# 	continue

				# same thing as above, a point on the path of plane2 which is used for 
				# drawing plane2's direction and checking for intersecting paths
				plane2_x_high = plane2.x + (500 * math.cos(math.radians(plane2.heading)))
				plane2_y_high = plane2.y + (500 * math.sin(math.radians(plane2.heading)))

				# same thing as above, a point on the path behind plane2, halfway out the exclusion zone
				plane2_x_low = plane2.x - (plane2.exclusion_zone * math.cos(math.radians(plane2.heading)))
				plane2_y_low = plane2.y - (plane2.exclusion_zone * math.sin(math.radians(plane2.heading)))

				# the straight line distance between the two planes
				dist = math.sqrt((plane1.x - plane2.x)**2 + (plane1.y - plane2.y)**2)

				# so now we need to check whether the two planes are intersecting or not
				# first thing we check is whether the two planes are within the exlusion zones
				# the exclusion zone says that no two planes can come within x distance of each other
				# obviously if they are within that distance then they need to move apart
				# The second thing we check is if the two planes are on intersecting paths
				# This is done by creating two line segments, one for each plane. 
				# the line segments end points are the two points we calculated earlier
				# if these line segments are intersecting then we know the planes are on an intersecting course.
				if dist <= plane1.exclusion_zone * 2.2 and doIntersect((plane1_x_low, plane1_y_low), (plane1_x_high, plane1_y_high), (plane2_x_low, plane2_y_low), (plane2_x_high, plane2_y_high)):
					# set the intersecting flag as true because we now found two planes that are intersecting
					intersecting = True

					# now we need to find the orientation of the two planes in relation to each other
					# this will determine which direction each planes moves
					# First we determine the orientation of plane 2 to plane 1.
					# We create the line segment for plane 1 (representing its flight path) and check whether plane2
					# is on the right or left side of the line segment. 
					# note that at this point we know that the two are on intersecting paths
					# so we wont get a scenario where plane 2 is actually moving away from plane 1. 
					# If the orientation is equal to 1, then plane2 is to the right of plane1
					if orientation((plane1_x_low, plane1_y_low), (plane1_x_high, plane1_y_high), (plane2_x_low, plane2_y_low)) == 1:
						# thus, plane 1 needs to turn left to avoid plane 2
						plane1.turn(-1)
						# now we determine the orientation of plane1 to plane2 and move it accordingly
						# if plane 1 is to the right of plane2
						if orientation((plane2_x_low, plane2_y_low), (plane2_x_high, plane2_y_high), (plane1_x_low, plane1_y_low)) == 1:
							plane2.turn(1)
						# if plane1 is to the left of plane two
						elif orientation((plane2_x_low, plane2_y_low), (plane2_x_high, plane2_y_high), (plane1_x_low, plane1_y_low)) == 2:
							plane2.turn(-1)
					# else if plane 2 is to the left of plane1
					elif orientation((plane1_x_low, plane1_y_low), (plane1_x_high, plane1_y_high), (plane2_x_low, plane2_y_low)) == 2:
						# turn right
						plane1.turn(1)
						# determine orientation of plane1 to plane 2
						if orientation((plane2_x_low, plane2_y_low), (plane2_x_high, plane2_y_high), (plane1_x_low, plane1_y_low)) == 1:
							plane2.turn(1)
						elif orientation((plane2_x_low, plane2_y_low), (plane2_x_high, plane2_y_high), (plane1_x_low, plane1_y_low)) == 2:
							plane2.turn(-1)
					# if the planes are on a direct (head on) path with each other
					# this still needs to be worked out as it isnt working right now
					elif orientation((plane1_x_low, plane1_y_low), (plane1_x_high, plane1_y_high), (plane2_x_low, plane2_y_low)) == 0:
						plane1.turn(-1)
						plane2.turn(-1)
			
			# if we checked against all other planes and plane1 is not an an intersecting path with any of them
			# we need to make sure that the plane is on its correct course to its target location
			if not intersecting:
				# so first check if the plane is not on the correct course to its target
				if not onSegment((plane1.x, plane1.y), (plane1_x_high, plane1_y_high), plane1.target):
					# if it is not, find out where the target is in relation to the current path of the plane
					# if it is to the right of the plane
					if orientation((plane1.x, plane1.y), (plane1_x_high, plane1_y_high), plane1.target) == 1:
						# turn the plane left
						plane1.turn(-1)
					# if it is to the left of the plane
					elif orientation((plane1.x, plane1.y), (plane1_x_high, plane1_y_high), plane1.target) == 2:
						# turn the plane right
						plane1.turn(1)
			

					

		# loop for drawing the planes on screen
		for plane in planes:

			plane1_x_high = plane.x + (500 * math.cos(math.radians(plane.heading)))
			plane1_y_high = plane.y + (500 * math.sin(math.radians(plane.heading)))

			plane1_x_low = plane.x - (plane.exclusion_zone * math.cos(math.radians(plane.heading)))
			plane1_y_low = plane.y - (plane.exclusion_zone * math.sin(math.radians(plane.heading)))

			# move the plane
			plane.move()
			# draw a circle for the exlusion zone of the plane
			pygame.draw.circle(DISPLAYSURF, (226, 57, 31), (int(plane.x), int(plane.y)), plane.exclusion_zone)
			# draw a circle for the planes target
			pygame.draw.circle(DISPLAYSURF, (0,0,255), plane.target, 5)
			# draw a circle for the actual plane
			pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (int(plane.x), int(plane.y)), 2)
			# draw a line for the path of the plane
			pygame.draw.line(DISPLAYSURF, (0, 255, 0), (plane1_x_low, plane1_y_low), (plane1_x_high, plane1_y_high))




		pygame.display.update()
		FPSCLOCK.tick(FPS)




if __name__ == '__main__':
	main()
import math


# class representation of a plane
class Plane:
	# initialize the plane
	# ------------ Parameters ----------------------
	# x       : x-coordinate of the plane
	# y       : y-coordinate of the plane
	# heading : current heading (direction) of the plane. Ranges from 0-360. 0 is directly right
	# speed   : speed of the plane. currently the only value that works well is 1
	#
	# ----------- Other Values ------------------------
	# turning_degrees : The number of degrees the plane needs to turn. Default value is 0
	# exclusion_zone  : The area in which no other planes are allowed to enter. 
	#       For example, if exclusion_zone is set at 50, no other planes can come within 50 pixels of this plane
	def __init__(self, x, y, heading, speed, target):
		self.x = x
		self.y = y
		self.heading = heading
		self.speed = speed
		self.turning_degrees = 0
		self.exclusion_zone = 100
		self.target = target

	# move the plane. executes every frame. If the plane needs to turn (turning_degrees != 0) that happens as well
	def move(self):
		# check if the plane needs to turn
		if self.turning_degrees > 0:
			self.heading += 1
			self.turning_degrees -= 1
		elif self.turning_degrees < 0:
			self.heading -= 1
			self.turning_degrees += 1

		# calculate the new coordinates of the plane
		self.x = self.x + (self.speed * math.cos(math.radians(self.heading)))
		self.y = self.y + (self.speed * math.sin(math.radians(self.heading)))

	def draw(self):
		pass

	# turn the plane. values range from [-180, 180]. Positive values turn right, negative values left
	def turn(self, degrees):
		self.turning_degrees = degrees
	

	
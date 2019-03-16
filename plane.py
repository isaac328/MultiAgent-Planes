import math

class Plane:
	def __init__(self, x, y, heading, speed):
		self.x = x
		self.y = y
		self.heading = math.radians(heading)
		self.speed = speed

	def move(self):
		self.x = self.x + (self.speed * math.cos(self.heading))
		self.y = self.y + (self.speed * math.sin(self.heading))

	def draw(self):
		pass
	

	
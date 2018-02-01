from auto_orientation import get_orientation
from sense_hat import SenseHat
import time

RED = [255, 0, 0]  # Red
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]  # White

_1 = [0, 5, ]
_2 = [0, 2, ]

s = SenseHat().clear()

class LED_indicator():
	"""docstring for LED_indicator"""
	def __init__(self, No):
		self.x = No[0]
		self.y = No[1]
		self.Sense = SenseHat()
		# self.Sense.clear()
		self.Sense.set_rotation(get_orientation(), False)
		self.Sense.set_pixel(self.x, self.y, WHITE)

	def set_online(self):
		self.Sense.set_pixel(self.x, self.y, GREEN)

	def set_error(self):
		self.Sense.set_pixel(self.x, self.y, YELLOW)

	def set_logged_in(self):
		self.Sense.set_pixel(self.x, self.y, BLUE)

	def set_offline(self):
		self.Sense.set_pixel(self.x, self.y, RED)

if __name__ == '__main__':
	a = LED_indicator(_1)
	a.set_error()

	b = LED_indicator(_2)
	b.set_online()

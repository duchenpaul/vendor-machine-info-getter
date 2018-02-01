#!/usr/bin/python
from sense_hat import SenseHat
sense = SenseHat()
raw = sense.get_accelerometer_raw()


x=raw['x']
y=raw['y']
z=raw['z']


def in_range(input, mid_num):
	max=mid_num + .5
	min=mid_num - .5
	if  input >=min and input <=max:
		return 1
	else:
		return 0

def get_orientation():
	if in_range(x, 0) and in_range(y, 1) and in_range(z, 0):
		orientation = 0
	elif in_range(x, -1) and in_range(y, 0) and in_range(z, 0):
		orientation = 90
	elif in_range(x, 0) and in_range(y, -1) and in_range(z, 0):
		orientation = 180
	elif in_range(x, 1) and in_range(y, 0) and in_range(z, 0):
		orientation = 270
	else:
		orientation=180
	pass
	return orientation
pass



sense.rotation = get_orientation()
# sense.show_letter("i")

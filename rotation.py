import numpy as np
import math
import transformations as t
from model import middle_sorted as leds

def rotation_matrix(axis, theta):
    axis = axis/math.sqrt(np.dot(axis,axis))
    a = math.cos(theta/2)
    b,c,d = -axis*math.sin(theta/2)
    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                     [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                     [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

if __name__ == '__main__':
	v = np.array([[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0]])
	v.shape = (3, -1)

	axis = np.array([0,0,1])
	theta = math.radians(90)
	m = rotation_matrix(axis,theta)

	# m = np.matrix(m)

	print(np.reshape(np.dot(m,v), (-1, 3)))

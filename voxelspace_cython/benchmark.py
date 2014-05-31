import numpy as np
from model import middle_sorted as leds
from voxelspace import VoxelSpace

leds = np.pad(leds, (0,1), 'constant', constant_values=1)[:-1]
voxels = VoxelSpace()
voxels.load('data/voxelspaces/basic-10x10x10')

def benchmark():
	p = voxels.getpixels(leds)
	# print 'CYTHON'
	# print p
	# print p.shape

def test():
	pass

	# def _getpixels(xyz):
	# 	return tuple(voxels.getpixels(*xyz))

	# def assert_pixel(xyz, color):
	# 	assert _getpixels(xyz) == color

	# assert_pixel((0, 0, 0), (255.0, 0.0, 0.0))
	# assert_pixel((4.5, 0, 0), (127.5, 127.5, 0.0))
	# assert_pixel((5, 0, 0), (0.0, 255.0, 0.0))
	# assert_pixel((0, 4.5, 0), (127.5, 0.0, 127.5))
	# assert_pixel((0, 5, 0), (0.0, 0.0, 255.0))
	# assert_pixel((0, 0, 0.5), (127.5, 127.5, 127.5))
	# assert_pixel((0, 0, 1), (0.0, 255.0, 255.0))
	# assert_pixel((4.5, 4.5, 0), (127.5, 127.5, 127.5))
	# assert_pixel((4.5, 4.5, 0.5), (95.625, 95.625, 159.375))

import os
from os.path import join, dirname
import json
import Image
import numpy as np

from getpixel import getpixels as getpixels_cython

class JsonError(Exception):
	pass

class VoxelSpace(object):
	def __init__(self):
		pass
		# self.images = []

	def setbounds(self, xyz0, xyz1):
		x0, y0, z0 = map(lambda i: float(i), xyz0)
		x1, y1, z1 = map(lambda i: float(i), xyz1)
		self.range_x = (x0, x1)
		self.range_y = (y0, y1)
		self.range_z = (z0, z1)

	def load(self, settings_file):
		voxelspace_folder = dirname(settings_file)
		with open(settings_file) as f:
			try:
				self.settings = json.load(f)
			except ValueError:
				raise JsonError()

		self.setbounds(*self.settings['bounds'])

		layers = join(voxelspace_folder, 'layers')
		filenames = map(lambda name: join(layers, name), sorted(os.listdir(layers)))

		width, height = self.settings['layer_size']
		depth = len(filenames)

		self.voxels = np.zeros((height, width, depth, 3), dtype='float32')

		for z, filename in enumerate(filenames):
			img = Image.open(filename)
			img = img.resize((width, height), Image.BILINEAR)
			self.voxels[:,:,z] = np.asarray(img, dtype=np.float32)[:,:,:3]

	def getpixels(self, leds):
		return getpixels_cython(leds, self.voxels, self.range_x[0], self.range_x[1], self.range_y[0], self.range_y[1], self.range_z[0], self.range_z[1])
		# return np.asarray(getpixels_cython(leds, self.voxels, self.range_x[0], self.range_x[1], self.range_y[0], self.range_y[1], self.range_z[0], self.range_z[1]), dtype=np.float32)
#		return [self.getpixel(x, y, z) for x, y, z, _ in leds]


if __name__ == '__main__':
	from random import random
	self = VoxelSpace()
	self.load('../data/voxelspaces/basic-10x10x10')

	def make_assert(xyz):
		print 'assert_pixel(%r, %r)' % (xyz, tuple(self.getpixel(*xyz)))

	def _getpixel(xyz):
		return tuple(self.getpixel(*xyz))

	def assert_pixel(xyz, color):
		assert _getpixel(xyz) == color

	assert_pixel((0, 0, 0), (255.0, 0.0, 0.0))
	assert_pixel((4.5, 0, 0), (127.5, 127.5, 0.0))
	assert_pixel((5, 0, 0), (0.0, 255.0, 0.0))
	assert_pixel((0, 4.5, 0), (127.5, 0.0, 127.5))
	assert_pixel((0, 5, 0), (0.0, 0.0, 255.0))
	assert_pixel((0, 0, 0.5), (127.5, 127.5, 127.5))
	assert_pixel((0, 0, 1), (0.0, 255.0, 255.0))
	assert_pixel((4.5, 4.5, 0), (127.5, 127.5, 127.5))
	assert_pixel((4.5, 4.5, 0.5), (95.625, 95.625, 159.375))

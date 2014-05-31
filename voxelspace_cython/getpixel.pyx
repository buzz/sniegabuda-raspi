cimport cython
import numpy as np
cimport numpy as cnp


cnp.import_array()

DTYPE = np.float32
ctypedef cnp.float32_t DTYPE_t

cdef inline double maprange(double a0, double a1, double b0, double b1, double s):
	return  b0 + ((s - a0) * (b1 - b0) / (a1 - a0))

# cdef cnp.ndarray[DTYPE_t, ndim=1] interpolate(cnp.ndarray[DTYPE_t, ndim=1] a, cnp.ndarray[DTYPE_t, ndim=1] b, double s):
# 	return a * (1-s) + b * s

# def lookup(v, max):
# 	v %= max
# 	v0 = int(v)
# 	v1 = (v0 + 1) % max
# 	vr = v - v0
# 	return v0, v1, vr

# cdef cnp.ndarray[DTYPE_t] getpixel(cnp.ndarray[DTYPE_t, ndim=4] voxels, double xin, double yin, double zin, double range_x0, double range_x1, double range_y0, double range_y1, double range_z0, double range_z1):

# 	cdef unsigned int height = voxels.shape[0]
# 	cdef unsigned int width  = voxels.shape[1]
# 	cdef unsigned int depth  = voxels.shape[2]

# 	cdef double x = maprange(range_x0, range_x1, 0, width,  xin)
# 	cdef double y = maprange(range_y0, range_y1, 0, height, yin)
# 	cdef double z = maprange(range_z0, range_z1, 0, depth,  zin)

# 	# lookup inlining
# 	cdef double x_mod = x % width
# 	cdef unsigned int x0 = <unsigned int> x_mod
# 	cdef unsigned int x1 = (x0 + 1) % width
# 	cdef double xr = x_mod - x0

# 	cdef double y_mod = y % height
# 	cdef unsigned int y0 = <unsigned int> y_mod
# 	cdef unsigned int y1 = (y0 + 1) % height
# 	cdef double yr = y_mod - y0

# 	cdef double z_mod = z % depth
# 	cdef unsigned int z0 = <unsigned int> z_mod
# 	cdef unsigned int z1 = (z0 + 1) % depth
# 	cdef double zr = z_mod - z0

# 	cdef cnp.ndarray[DTYPE_t] v000 = voxels[y0, x0, z0]
# 	cdef cnp.ndarray[DTYPE_t] v010 = voxels[y0, x1, z0]
# 	cdef cnp.ndarray[DTYPE_t] v100 = voxels[y1, x0, z0]
# 	cdef cnp.ndarray[DTYPE_t] v110 = voxels[y1, x1, z0]

# 	cdef cnp.ndarray[DTYPE_t] v001 = voxels[y0, x0, z1]
# 	cdef cnp.ndarray[DTYPE_t] v011 = voxels[y0, x1, z1]
# 	cdef cnp.ndarray[DTYPE_t] v101 = voxels[y1, x0, z1]
# 	cdef cnp.ndarray[DTYPE_t] v111 = voxels[y1, x1, z1]

# 	cdef cnp.ndarray[DTYPE_t] color_a0 = v000 * (1.0-xr) + v010 * xr
# 	cdef cnp.ndarray[DTYPE_t] color_a1 = v100 * (1.0-xr) + v110 * xr
# 	cdef cnp.ndarray[DTYPE_t] color_z0 = color_a0 * (1.0-yr) + color_a1 * yr
# 	color_a0 = v001 * (1.0-xr) + v011 * xr
# 	color_a1 = v101 * (1.0-xr) + v111 * xr
# 	cdef cnp.ndarray[DTYPE_t] color_z1 = color_a0 * (1.0-yr) + color_a1 * yr
# 	return color_z0 * (1.0-zr) + color_z1 * zr

@cython.boundscheck(False)
@cython.wraparound(False)
def getpixels(cnp.ndarray[double, ndim=2] leds, cnp.ndarray[DTYPE_t, ndim=4] voxels, double range_x0, double range_x1, double range_y0, double range_y1, double range_z0, double range_z1):
	ret = []
	cdef cnp.ndarray[double] led
	cdef unsigned int height = voxels.shape[0]
	cdef unsigned int width  = voxels.shape[1]
	cdef unsigned int depth  = voxels.shape[2]

	cdef double _mod
	cdef unsigned int x0
	cdef unsigned int x1
	cdef unsigned int y0
	cdef unsigned int y1
	cdef unsigned int z0
	cdef unsigned int z1
	cdef double xr
	cdef double yr
	cdef double zr
	cdef double v000r
	cdef double v000g
	cdef double v000b
	cdef double v010r
	cdef double v010g
	cdef double v010b
	cdef double v100r
	cdef double v100g
	cdef double v100b
	cdef double v110r
	cdef double v110g
	cdef double v110b
	cdef double v001r
	cdef double v001g
	cdef double v001b
	cdef double v011r
	cdef double v011g
	cdef double v011b
	cdef double v101r
	cdef double v101g
	cdef double v101b
	cdef double v111r
	cdef double v111g
	cdef double v111b
	cdef double color_a0r
	cdef double color_a0g
	cdef double color_a0b
	cdef double color_a1r
	cdef double color_a1g
	cdef double color_a1b
	cdef double color_z0r
	cdef double color_z0g
	cdef double color_z0b
	cdef double color_z1r
	cdef double color_z1g
	cdef double color_z1b
	cdef double revxr
	cdef double revyr
	cdef double revzr

	for i from 0 <= i < 105:

		led = leds[i]

		# inlining lookup
		_mod = maprange(range_x0, range_x1, 0, width,  led[0]) % width
		x0 = <unsigned int> _mod
		x1 = (x0 + 1) % width
		xr = _mod - x0

		_mod = maprange(range_y0, range_y1, 0, height, led[1]) % height
		y0 = <unsigned int> _mod
		y1 = (y0 + 1) % height
		yr = _mod - y0

		_mod = maprange(range_z0, range_z1, 0, depth,  led[2]) % depth
		z0 = <unsigned int> _mod
		z1 = (z0 + 1) % depth
		zr = _mod - z0

		v000r = voxels[y0, x0, z0, 0]
		v000g = voxels[y0, x0, z0, 1]
		v000b = voxels[y0, x0, z0, 2]
		v010r = voxels[y0, x1, z0, 0]
		v010g = voxels[y0, x1, z0, 1]
		v010b = voxels[y0, x1, z0, 2]
		v100r = voxels[y1, x0, z0, 0]
		v100g = voxels[y1, x0, z0, 1]
		v100b = voxels[y1, x0, z0, 2]
		v110r = voxels[y1, x1, z0, 0]
		v110g = voxels[y1, x1, z0, 1]
		v110b = voxels[y1, x1, z0, 2]

		v001r = voxels[y0, x0, z1, 0]
		v001g = voxels[y0, x0, z1, 1]
		v001b = voxels[y0, x0, z1, 2]
		v011r = voxels[y0, x1, z1, 0]
		v011g = voxels[y0, x1, z1, 1]
		v011b = voxels[y0, x1, z1, 2]
		v101r = voxels[y1, x0, z1, 0]
		v101g = voxels[y1, x0, z1, 1]
		v101b = voxels[y1, x0, z1, 2]
		v111r = voxels[y1, x1, z1, 0]
		v111g = voxels[y1, x1, z1, 1]
		v111b = voxels[y1, x1, z1, 2]

		# inlining interpolation
		revxr = 1.0 - xr
		revyr = 1.0 - yr
		revzr = 1.0 - zr
		color_a0r = v000r * revxr + v010r * xr
		color_a0g = v000g * revxr + v010g * xr
		color_a0b = v000b * revxr + v010b * xr
		color_a1r = v100r * revxr + v110r * xr
		color_a1g = v100g * revxr + v110g * xr
		color_a1b = v100b * revxr + v110b * xr
		color_z0r = color_a0r * revyr + color_a1r * yr
		color_z0g = color_a0g * revyr + color_a1g * yr
		color_z0b = color_a0b * revyr + color_a1b * yr
		color_a0r = v001r * revxr + v011r * xr
		color_a0g = v001g * revxr + v011g * xr
		color_a0b = v001b * revxr + v011b * xr
		color_a1r = v101r * revxr + v111r * xr
		color_a1g = v101g * revxr + v111g * xr
		color_a1b = v101b * revxr + v111b * xr
		color_z1r = color_a0r * revyr + color_a1r * yr
		color_z1g = color_a0g * revyr + color_a1g * yr
		color_z1b = color_a0b * revyr + color_a1b * yr
		ret.append([
			color_z0r * revzr + color_z1r * zr,
			color_z0g * revzr + color_z1g * zr,
			color_z0b * revzr + color_z1b * zr,
		])

	return np.array(ret, dtype=DTYPE)

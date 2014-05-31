def interpolate(a, b, s):
	return a * (1-s) + b * s

def lookup(v, max):
	v %= max
	v0 = int(v)
	v1 = (v0 + 1) % max
	vr = v - v0
	return v0, v1, vr

def getpixel(voxels, x, y, z):

	height, width, depth, color_depth = voxels.shape

	x0, x1, xr = lookup(x, width)
	y0, y1, yr = lookup(y, height)
	z0, z1, zr = lookup(z, depth)

	v000 = voxels[y0, x0, z0]
	v010 = voxels[y0, x1, z0]
	v100 = voxels[y1, x0, z0]
	v110 = voxels[y1, x1, z0]

	v001 = voxels[y0, x0, z1]
	v011 = voxels[y0, x1, z1]
	v101 = voxels[y1, x0, z1]
	v111 = voxels[y1, x1, z1]

	color_z0 = interpolate(
		interpolate(v000, v010, xr),
		interpolate(v100, v110, xr),
		yr
	)

	color_z1 = interpolate(
		interpolate(v001, v011, xr),
		interpolate(v101, v111, xr),
		yr
	)

	return interpolate(
		color_z0,
		color_z1,
		zr
	)

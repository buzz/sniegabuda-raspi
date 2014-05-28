from numpy import array
import Image


from model import middle_sorted as leds
from voxelspace import VoxelSpace

# leds = leds[20:40]

voxels = VoxelSpace()
voxels.load('data/pixelspaces/basic')
voxels.setbounds((-30, -30, 0), (30, 30, 30))

bytes = [voxels.getpixel((x, y, 0)) for x, y, z in leds]
bytes = [list(rgb) for rgb in bytes]
print bytes
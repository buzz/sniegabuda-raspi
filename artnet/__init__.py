from StupidArtnet import StupidArtnet


NUM_PIXELS = 105


class LEDStrip(object):
	def __init__(self, ip='2.0.0.3', universe=1, fps=30):
		self._packet_size = NUM_PIXELS * 3
		self._artnet = StupidArtnet(ip, universe, self._packet_size, fps)
		self._artnet.clear()
		self._artnet.start()

	def __del__(self):
		self._artnet.stop()

	def set(self, pixel, r, g, b):
		self._artnet.set_rgb(pixel + 1, int(r), int(g), int(b))

	def update(self):
		pass

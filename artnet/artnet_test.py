import time
from StupidArtnet import StupidArtnet

packet_size = 30

artnet = StupidArtnet('2.0.0.3', 1, packet_size)
packet = bytearray(packet_size)
artnet.set(packet)
# artnet.set_single_value(, value)

artnet.start()

col = 0
for x in range(100):
	for i in range(10):
		packet[i*3] = col
		packet[i*3+1] = 0
		packet[i*3+2] = 0
	artnet.set(packet)
	col += 3
	if col > 255:
		col = 0
	time.sleep(.2)

artnet.stop()

import sys
import os
from ledstrip import LEDStrip
from color import *

dev = '/dev/spidev0.0'

if not os.path.exists(dev):
    sys.stderr.write('Could not find SPI device %s\n' % dev)
    sys.exit(2)

try:
    open(dev)
except IOError as  e:
    if e.errno == 13:
        sys.stderr.write('SPI device has wrong permissions: %s\n' % dev)
        sys.exit(2)

# 210 LED, we control them pair-wise!
NUM_PIXELS = 210
        
strip = LEDStrip(210, True, dev=dev)
strip.all_off()

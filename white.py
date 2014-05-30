#!/usr/bin/python
from ledstrip import LEDStrip

strip = LEDStrip()

for i in xrange(105):
    strip.set(i, 255, 255, 255)
strip.update()

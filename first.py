#!/usr/bin/python
'''Test first led'''

from ledstrip import LEDStrip

strip = LEDStrip()

for i in xrange(105):
    strip.set(i, 0, 0, 0)

strip.set(0, 255, 255, 255)

strip.update()

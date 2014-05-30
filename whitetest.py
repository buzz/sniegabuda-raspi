#!/usr/bin/python
'''Test white color'''

from ledstrip import LEDStrip

strip = LEDStrip()

while True:
    for i in xrange(105):
        strip.set(i, 255, 255, 255)
        strip.update()

    strip.off()
    strip.update()

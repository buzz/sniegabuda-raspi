#!/usr/bin/python

from time import sleep
from led import strip, Color

strip.fillOff()

for i in xrange(210):
    strip.set(i, Color(127, 127, 127))
    strip.update()
    sleep(0.05)

sleep(10)

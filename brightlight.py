#!/usr/bin/python

from time import sleep
from led import strip, Color

for i in xrange(255):
    strip.fill(Color(i, i, i))
    strip.update()
    #sleep(0.01)

while True:
    sleep(10)

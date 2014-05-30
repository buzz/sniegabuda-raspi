#!/usr/bin/python

from time import sleep
from ledstrip import LEDStrip

strip = LEDStrip()

min = 36
max = 140
b = 40
speed = 1
dir = 1
while True:
    if   b <= min: dir =  1
    elif b >= max: dir = -1
    b += dir * speed

    if   b > 255: b = 255
    elif b < 0:   b = 0

    for i in xrange(105):
        strip.set(i, b, 0, 0)
    strip.update()
    sleep(0.08)

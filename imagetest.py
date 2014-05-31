#!/usr/bin/python
from ledstrip import BaseEngine
from bytes import bytes


class ImageTest(BaseEngine):
    def __init__(self):
        super(ImageTest, self).__init__()
        self.b = 0.0
        self.i = 0

    def step(self):
	for i, (r, g, b) in enumerate(bytes[:105]):
	    self.strip.set(i, r, g, b)

t = ImageTest()
t.run()

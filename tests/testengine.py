#!/usr/bin/python
from ledstrip import BaseEngine


class TestEngine(BaseEngine):
    def __init__(self):
        super(TestEngine, self).__init__()
        self.b = 0

    def step(self):
        self.b += 10
        if self.b > 255:
            self.b = 0
        for i in xrange(105):
            self.strip.set(i, self.b, self.b, self.b)

t = TestEngine()
t.run()

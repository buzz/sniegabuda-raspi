#!/usr/bin/python

from time import time, sleep
from threading import Thread, Event
import spidev


NUM_PIXELS = 105
current_ms = lambda: int(round(time() * 1000))

class LEDStrip(object):
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        # 8000000 -> 8MHz
        self.spi.max_speed_hz = 8000000

        # init pixel buffer
        self.buffer = [bytearray(3) for x in range(NUM_PIXELS)]

        # gamma correction from
        # http://learn.adafruit.com/light-painting-with-raspberry-pi
        self.gamma = bytearray(256)
        for i in range(256):
            self.gamma[i] = 0x80 | int(
                pow(float(i) / 255.0, 2.5) * 127.0 + 0.5
            )

    def set(self, pixel, r, g, b):
        self.buffer[pixel][0] = self.gamma[int(r)]
        self.buffer[pixel][1] = self.gamma[int(g)]
        self.buffer[pixel][2] = self.gamma[int(b)]

    def off(self):
        for i in xrange(len(self.buffer)):
            self.set(i, 0, 0, 0)

    def update(self):
        out = []
        for pixel in self.buffer:
            # two LED for one pixel!
            out.append(pixel[0])
            out.append(pixel[1])
            out.append(pixel[2])
            out.append(pixel[0])
            out.append(pixel[1])
            out.append(pixel[2])
        for i in xrange(7):
            # 7 0-bytes (one per 32 LED) to clear
            out.append(0)
        # we call xfer2 only once (faster)
        self.spi.xfer2(out)


# StoppableThread is from user Dolphin, from http://stackoverflow.com/questions/5849484/how-to-exit-a-multithreaded-program
class StoppableThread(Thread):  
    def __init__(self):
        Thread.__init__(self)
        self.stop_event = Event()

    def stop(self):
        if self.isAlive() == True:
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class IntervalTimer(StoppableThread):
    def __init__(self, interval, worker_func):
        super(IntervalTimer, self).__init__()
        self._interval = interval
        self._worker_func = worker_func

    def run(self):
        while not self.stop_event.is_set():
            self._worker_func()
            sleep(self._interval)


class BaseEngine(object):
    def __init__(self, fps=20):
        self.strip = LEDStrip()
        self.strip.off()
        self._interval = 1. / fps
        self.timer = IntervalTimer(self._interval, self.__update)

    def run(self):
        self._start_ms = current_ms()
        self.timer.start()
        try:
            while True:
                sleep(0.5)
        except KeyboardInterrupt:
            self.halt()

    def halt(self):
        self.timer.stop()
        self.strip.off()
        self.strip.update()

    def step(self):
        raise NotImplementedError()

    def current_ms(self):
        return current_ms() - self._start_ms

    def current_s(self):
        return (current_ms() - self._start_ms) / 1000

    def __update(self):
        self.strip.update()
        self.step()

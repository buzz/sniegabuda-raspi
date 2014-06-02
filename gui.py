# -*- coding: utf-8 -*-

import sys
import time
import curses
import numpy as np


from model import middle_sorted as leds
# leds = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
# leds = leds[:31]

try:
	from voxelspace_cython import VoxelSpace
except ImportError:
	from voxelspace import VoxelSpace


from transformations import euler_matrix
from math import radians as rad

try:
	from ledstrip import LEDStrip
	strip = LEDStrip()
except ImportError:
	strip = None

def debug(*args):
	for a in args:
		sys.stderr.write(str(a) + ' ')
	sys.stderr.write('\n\r')

template_infopad = '''
                   	a          w          c
translate - X:%(tx)6.2f, Y:%(ty)6.2f, Z:%(tz)6.2f
                    d          x          e

                   r          f          v
rotation  - X:  10.0°, Y:   0.0°, Z:   0.0°
                   t          g          b
'''


class TitlePad(object):
	def __init__(self):
		w = 80
		h = 5

		stars = '*'*w
		title = 'Domulatrix-2000 v0.07a'

		def line(s):
			return '*%s*' % (s.center(w-2))

		self.pad = pad = curses.newpad(h+1, w)
		pad.addstr(0, 0, stars)
		pad.addstr(1, 0, line(''))
		pad.addstr(2, 0, line(title))
		pad.addstr(3, 0, line(''))
		pad.addstr(4, 0, stars)

	def refresh(self):
		self.pad.refresh(0,0,0,0,5,80)


class App(object):

	def setup(self):
		self.stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.stdscr.keypad(1)

	def exit(self):
		self.stdscr.keypad(0)
		curses.nocbreak()
		curses.echo()
		curses.endwin()

	def start(self):
		self.setup()
		try:
			self.run()
			self.exit()
		except:
			self.exit()
			raise

	def event_loop(self, funcs):
		try:
			while 1:
				c = self.stdscr.getch()
				info = str(c)
				# debug(c, chr(c), c in funcs)
				if c in funcs:
					funcs[c]()
		except KeyboardInterrupt:
			pass

class Domulatrix(App):

	def run(self):
		self.infopad = curses.newpad(20, 80)

		class Transform(object): pass

		t = self.transforms = Transform()
		t.tx = 0
		t.ty = 0
		t.tz = 0
		t.rx = 0
		t.ry = 0
		t.rz = 0

		self.update()

		step_translate = 1
		step_rotate    = 5

		def tx_dec(): t.tx -= step_translate
		def tx_inc(): t.tx += step_translate
		def ty_dec(): t.ty -= step_translate
		def ty_inc(): t.ty += step_translate
		def tz_dec(): t.tz -= step_translate
		def tz_inc(): t.tz += step_translate
		def rx_dec(): t.rx = (t.rx - step_rotate) % 360
		def rx_inc(): t.rx = (t.rx + step_rotate) % 360
		def ry_dec(): t.ry = (t.ry - step_rotate) % 360
		def ry_inc(): t.ry = (t.ry + step_rotate) % 360
		def rz_dec(): t.rz = (t.rz - step_rotate) % 360
		def rz_inc(): t.rz = (t.rz + step_rotate) % 360

		def update_after(func):
			def wrapped():
				func()
				self.update()
			return wrapped

		funcs = {
			# translation
			ord('a'): update_after(tx_dec),
			ord('d'): update_after(tx_inc),
			ord('w'): update_after(ty_dec),
			ord('x'): update_after(ty_inc),
			ord('c'): update_after(tz_dec),
			ord('e'): update_after(tz_inc),
			# rotation
			ord('r'): update_after(rx_dec),
			ord('t'): update_after(rx_inc),
			ord('f'): update_after(ry_dec),
			ord('g'): update_after(ry_inc),
			ord('v'): update_after(rz_dec),
			ord('b'): update_after(rz_inc),
		}

		self.event_loop(funcs)

	def update(self):
		self.update_gui()
		self.update_leds()

	def update_gui(self):
		t = self.transforms

		txt = ''
		txt =  'translate - X: %6.2f, Y: %6.2f, Z: %6.2f' % (t.tx, t.ty, t.tz)
		txt += '\n\r'
		txt += 'rotation  - X: %5.1f°, Y: %5.1f°, Z: %5.1f°' % (t.rx, t.ry, t.rz)

		pad = self.infopad

		pad.addstr(0, 0, '                + d +      + w +      + e +')
		pad.addstr(1, 0, 'translate - X: %6.2f, Y: %6.2f, Z: %6.2f' % (t.tx, t.ty, t.tz))
		pad.addstr(2, 0, '                - a -      - x -      - c -')

		pad.addstr(3, 0, '')

		pad.addstr(4, 0, '                + t +      + g +      + b +')
		pad.addstr(5, 0, 'rotation  - X: %5.1f°, Y: %5.1f°, Z: %5.1f°' % (t.rx, t.ry, t.rz))
		pad.addstr(6, 0, '                - r -      - f -      - v -')

		pad.refresh(0,0,0,0,6,80)

	def get_transformed_model(self):
		t = self.transforms

		translation_matrix = np.matrix([
			[1, 0, 0, t.tx],
			[0, 1, 0, t.ty],
			[0, 0, 1, t.tz],
			[0, 0, 0, 1   ]
		])

		rotation_matrix = np.matrix(euler_matrix(
			rad(t.rx),
			rad(t.ry),
			rad(t.rz)
		))

		matrix = translation_matrix * rotation_matrix

		leds_ = leds.copy()
		leds_ = np.pad(leds_, (0,1), 'constant', constant_values=1)[:-1]
		leds_ = np.rot90(leds_, 3)
		leds_ = np.dot(matrix, leds_)
		leds_ = np.rot90(leds_)
		leds_ = np.array(leds_)

		return leds_

	def update_leds(self):

		leds = self.get_transformed_model()
		colors = voxels.getpixels(leds)
		colors = [list(rgb) for rgb in colors]

		if strip is None: return

		for i, (red, green, blue) in enumerate(colors):
			strip.set(i, red, green, blue)

		strip.update()

try:
	folder = sys.argv[1]
except IndexError:
	print 'Argument missing.'
	sys.exit()

voxels = VoxelSpace()
voxels.load(folder)

app = Domulatrix()
app.start()


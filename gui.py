# -*- coding: utf-8 -*-

import sys
import time
import threading
import curses
import time
import math
import numpy as np

from model import middle_sorted as leds

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

class TransformsWindow(object):
	width = 80
	height = 20

	def __init__(self):
		begin_x = 0; begin_y = 0
		height = 11; width = 80
		self.win = curses.newwin(height, width, begin_y, begin_x)

	def update(self, transforms):
		t = transforms
		win = self.win

		win.erase()

		lines = [
			'                  + d +      + w +      + e +',
			'translation - X: %6.2f, Y: %6.2f, Z: %6.2f' % (t['tx'], t['ty'], t['tz']),
			'                  - a -      - x -      - c -',
			'',
			'                  + t +      + g +      + b +',
			'rotation    - X: %5.1f°, Y: %5.1f°, Z: %5.1f°' % (t['rx'], t['ry'], t['rz']),
			'                  - r -      - f -      - v -',
			'',
			'                  + z +      + h +      + n +      + l +',
			'scaling     - X: %5.1f%%, Y: %5.1f%%, Z: %5.1f%%,      XYZ' % (t['sx'], t['sy'], t['sz']),
			'                  - u -      - j -      - m -      - k -',
		]

		for y, line in enumerate(lines):
			win.addstr(y, 0, line)

		win.refresh()


class App(object):

	def start(self, *args, **kw):
		def run(curses_window):
			self.stdscr = curses_window
			self.run(*args, **kw)
		curses.wrapper(run)

	def event_loop(self, funcs):
		try:
			while not self._stop:
				c = self.stdscr.getch()
				if c in funcs: funcs[c]()
		except KeyboardInterrupt:
			pass

class Physics(threading.Thread):
	def __init__(self, transforms, motion, update):
		threading.Thread.__init__(self)
		self.frame = -1
		self.transforms = transforms
		self.motion = motion
		self.update = update
		lp = self.lfo_pos = {}
		lp['tx'] = lp['ty'] = lp['tz'] = 0
		lp['sx'] = lp['sy'] = lp['sz'] = 0
		lp['rx'] = lp['ry'] = lp['rz'] = 0

		self.lfos = {
			'rx': {'step': 0.01115, 'depth': 20},
			'ry': {'step': 0.011711, 'depth': 30},
			'rz': {'step': 0.012784, 'depth': 40},
			'tz': {'step': 0.00283, 'depth': 130},
			'sx': {'step': 0.00223, 'depth': 20},
			'sy': {'step': 0.00223, 'depth': 20},
			'sz': {'step': 0.00223, 'depth': 20},
		}

		self._stop = False

	def run(self):
		while not self._stop:
			time.sleep(0.02)
			self.step()

	def step(self):
		self.frame += 1
		t = self.transforms
		m = self.motion
		lp = self.lfo_pos

		for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
			t[attr] += m[attr]

		t = t.copy()
		for attr, values in self.lfos.items():
			step = values['step']
			depth = values['depth']
			lp[attr] += step 
			t[attr] += math.sin(lp[attr])*depth

		self.update(t)


class Domulatrix(App):

	def run(self, voxel_folder):
		# titlepad = TitlePad()
		# titlepad.refresh()

		self._stop = False

		self.voxels = VoxelSpace()
		self.voxels.load(folder)

		self.transforms_window = TransformsWindow()

		class Transform(object): pass

		t = self.transforms = {}
		t['tx'] = t['ty'] = t['tz'] = 0
		t['sx'] = t['sy'] = t['sz'] = 100
		t['rx'] = t['ry'] = t['rz'] = 0

		m = self.motion = {}
		m = self.motion = {
			'tx': 0.03452,
			'ty': 0.042525,
			'tz': 0.047234,
			'rx': 0,
			'ry': 0,
			'rz': 0,
		}

		self.update(t)

		shift_multiplier = 6.
		step_translate   = 1
		step_scale       = 1.02
		step_rotate      = 7.5

		xxx = t

		def sx_dec(m): xxx['sx'] /= step_scale ** m
		def sx_inc(m): xxx['sx'] *= step_scale ** m
		def sy_dec(m): xxx['sy'] /= step_scale ** m
		def sy_inc(m): xxx['sy'] *= step_scale ** m
		def sz_dec(m): xxx['sz'] /= step_scale ** m
		def sz_inc(m): xxx['sz'] *= step_scale ** m

		def rx_dec(m): xxx['rx'] = (xxx['rx'] - step_rotate * m) % 360
		def rx_inc(m): xxx['rx'] = (xxx['rx'] + step_rotate * m) % 360
		def ry_dec(m): xxx['ry'] = (xxx['ry'] - step_rotate * m) % 360
		def ry_inc(m): xxx['ry'] = (xxx['ry'] + step_rotate * m) % 360
		def rz_dec(m): xxx['rz'] = (xxx['rz'] - step_rotate * m) % 360
		def rz_inc(m): xxx['rz'] = (xxx['rz'] + step_rotate * m) % 360

		def event_wrapper(func, multiplier):
			def wrapped():
				func(multiplier)
				self.update(self.transforms)
			return wrapped

		def scale_dec(m):
			xxx['sx'] /= step_scale ** m
			xxx['sy'] /= step_scale ** m
			xxx['sz'] /= step_scale ** m

		def scale_inc(m):
			xxx['sx'] *= step_scale ** m
			xxx['sy'] *= step_scale ** m
			xxx['sz'] *= step_scale ** m

		def foo(*args):
			self.physics._stop = True
			self._stop = True

		events = {

			# translation
			'a': {'attr': 'tx', 'func': lambda v,s,m: v-s*m, 'step': step_translate },
			'd': {'attr': 'tx', 'func': lambda v,s,m: v+s*m, 'step': step_translate },
			'w': {'attr': 'ty', 'func': lambda v,s,m: v-s*m, 'step': step_translate },
			'x': {'attr': 'ty', 'func': lambda v,s,m: v+s*m, 'step': step_translate },
			'c': {'attr': 'tz', 'func': lambda v,s,m: v-s*m, 'step': step_translate },
			'e': {'attr': 'tz', 'func': lambda v,s,m: v+s*m, 'step': step_translate },

			# scale
			'z': sx_dec,
			'u': sx_inc,
			'h': sy_dec,
			'j': sy_inc,
			'n': sz_dec,
			'm': sz_inc,
			'k': scale_dec,
			'l': scale_inc,

			# rotation
			'r': rx_dec,
			't': rx_inc,
			'f': ry_dec,
			'g': ry_inc,
			'v': rz_dec,
			'b': rz_inc,			# translation
			'a': {'attr': 'tx', 'func': lambda v,s,m: v-s*m, 'step': step_translate },
			'd': {'attr': 'tx', 'func': lambda v,s,m: v+s*m, 'step': step_translate },
			'w': {'attr': 'ty', 'func': lambda v,s,m: v-s*m, 'step': step_translate },
			'x': {'attr': 'ty', 'func': lambda v,s,m: v+s*m, 'step': step_translate },
			'c': {'attr': 'tz', 'func': lambda v,s,m: v-s*m, 'step': step_translate },
			'e': {'attr': 'tz', 'func': lambda v,s,m: v+s*m, 'step': step_translate },

			# special
			'p': foo,
		}

		def create_hander(opts):
			def handler(mul):
				attr, func, step = opts['attr'], opts['func'], opts['step']
				v = t[attr]
				t[attr] = func(v, step, mul)

			return handler


		for char, opts in events.items():
			if callable(opts): handler = opts
			else:              handler = create_hander(opts)

			events[ord(char)]         = event_wrapper(handler, 1.)
			events[ord(char.upper())] = event_wrapper(handler, shift_multiplier)
			del events[char]

		self.physics = Physics(t, m, self.update)
		self.physics.start()
		self.event_loop(events)


	def update(self, transforms):
		self.transforms_window.update(transforms)
		self.update_leds(transforms)

	def get_transformed_model(self, transforms):
		t = transforms

		scaling_matrix = np.matrix([
			[t['sx']/100, 0, 0, 1],
			[0, t['sy']/100, 0, 1],
			[0, 0, t['sz']/100, 1],
			[0, 0, 0, 1]
		])

		translation_matrix = np.matrix([
			[1, 0, 0, t['tx']],
			[0, 1, 0, t['ty']],
			[0, 0, 1, t['tz']],
			[0, 0, 0, 1   ]
		])

		rotation_matrix = np.matrix(euler_matrix(
			rad(t['rx']),
			rad(t['ry']),
			rad(t['rz'])
		))

		matrix = scaling_matrix * translation_matrix * rotation_matrix

		leds_ = leds.copy()
		leds_ = np.pad(leds_, (0,1), 'constant', constant_values=1)[:-1]
		leds_ = np.rot90(leds_, 3)
		leds_ = np.dot(matrix, leds_)
		leds_ = np.rot90(leds_)
		leds_ = np.array(leds_)

		return leds_

	def update_leds(self, transforms):

		leds = self.get_transformed_model(transforms)
		colors = self.voxels.getpixels(leds)

		if strip is None: return

		for i, (red, green, blue) in enumerate(colors):
			strip.set(i, red, green, blue)

		strip.update()

try:
	folder = sys.argv[1]
except IndexError:
	print 'Argument missing.'
	sys.exit()

app = Domulatrix()
app.start(voxel_folder=folder)

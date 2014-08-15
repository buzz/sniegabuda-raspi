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

DISPLAY_PRESSED_KEY = True
MODULATE = True

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
		height = 20; width = 80
		self.win = curses.newwin(height, width, begin_y, begin_x)

	def update(self, transforms):
		t = transforms
		win = self.win

		win.erase()

		lines = """
			=============================================
			            |    X       Y       Z
			=============================================
			            |
			            |  A / D   X / W   C / E
			translation | %6.2f  %6.2f  %6.2f
			            |
			---------------------------------------------
			            |
			            |  R / T   F / G   V / B
			rotation    |  %5.1f° %5.1f° %5.1f°
			            |
			---------------------------------------------
			            |
			            |  Z / U   H / J   N / M   K / L
			scaling     | %5.1f%%  %5.1f%%  %5.1f%%
			            |
			============|================================
			            |    X       Y       Z
			=============================================
		"""

		lines = lines % (
			t['tx'], t['ty'], t['tz'],
			t['rx'], t['ry'], t['rz'],
			t['sx'], t['sy'], t['sz']
		)

		lines = lines.replace('\t','').replace('\r','').split('\n')[1:-1]

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
				if DISPLAY_PRESSED_KEY: debug('\n\nkey pressed: %s   '%c)
				if c in funcs: funcs[c]()
		except KeyboardInterrupt:
			pass

def oscillator(speed, depth):
	def f(frame):
		return math.sin(frame*speed)*depth
	return f

def linear_motion(speed, wrap=None, minimum=float('-inf'), maximum=float('inf')):
	def f(frame):
		v = frame*speed
		if wrap is not None: v %= wrap
		v = min(maximum, v)
		v = max(minimum, v)
		return v
	return f

modulator_functions = {
	'oscillator': oscillator,
	'linear_motion': linear_motion
}

class Modulators(threading.Thread):

	framerate = 60

	def __init__(self, transforms, voxelspace, update):
		threading.Thread.__init__(self)
		self.frame = -1
		self.transforms = transforms
		self.update = update
		self._stop = False
		self.init_modulators(voxelspace)

	def init_modulators(self, voxelspace):
		self.modulators = {}

		if not 'modulation' in voxelspace.settings:
			return

		for attr, mods in voxelspace.settings['modulation'].items():
			for mod in mods:
				func = modulator_functions[mod['type']](**mod['options'])
				self.modulators.setdefault(attr, []).append(func)

	def run(self):
		while not self._stop:
			self.step()
			time.sleep(1./self.framerate)

	def reset(self):
		self.frame = -1

	def step(self):
		self.frame += 1

		transforms = self.transforms.copy()

		for attr, funcs in self.modulators.items():
			if callable(funcs):
				funcs = (funcs,)
			for func in funcs:
				transforms[attr] += func(self.frame)

		if MODULATE:
			self.update(transforms)
		else:
			self.update(self.transforms)


class Domulatrix(App):

	def run(self, voxel_folder):
		# titlepad = TitlePad()
		# titlepad.refresh()
		self.init_transforms()
		self.load_voxelspace(voxel_folder)
		self.init_gui()

	def init_transforms(self):
		t = self.initial_transforms = {}
		t['tx'] = t['ty'] = t['tz'] = 0
		t['sx'] = t['sy'] = t['sz'] = 100
		t['rx'] = t['ry'] = t['rz'] = 0
		t = self.transforms = self.initial_transforms.copy()

	def init_gui(self):
		self._stop = False

		self.transforms_window = TransformsWindow()

		t = self.transforms

		shift_multiplier = 6.
		step_translate   = 1
		step_scale       = 1.02
		step_rotate      = 7.5

		def scale_dec(multiplier):
			t['sx'] /= step_scale ** multiplier
			t['sy'] /= step_scale ** multiplier
			t['sz'] /= step_scale ** multiplier

		def scale_inc(multiplier):
			t['sx'] *= step_scale ** multiplier
			t['sy'] *= step_scale ** multiplier
			t['sz'] *= step_scale ** multiplier

		def reset(*args):
			self.transforms.update(self.initial_transforms)
			self.modulators.reset()

		def prev_voxelspace(*args):
			self.load_voxelspace('data/voxelspaces/check-1-0')

		def next_voxelspace(*args):
			self.load_voxelspace('data/voxelspaces/basic-10x10x10')

		def stop(*args):
			self.modulators._stop = True
			self._stop = True

		events = {

			# reset
			19: reset, # ctrl-s

			# translation
			'a': {'attr': 'tx', 'func': lambda val, mul: val-(step_translate*mul) },
			'd': {'attr': 'tx', 'func': lambda val, mul: val+(step_translate*mul) },
			'x': {'attr': 'ty', 'func': lambda val, mul: val-(step_translate*mul) },
			'w': {'attr': 'ty', 'func': lambda val, mul: val+(step_translate*mul) },
			'c': {'attr': 'tz', 'func': lambda val, mul: val-(step_translate*mul) },
			'e': {'attr': 'tz', 'func': lambda val, mul: val+(step_translate*mul) },

			# scale
			'z': {'attr': 'sx', 'func': lambda val, mul: val/(step_scale**mul) },
			'u': {'attr': 'sx', 'func': lambda val, mul: val*(step_scale**mul) },
			'h': {'attr': 'sy', 'func': lambda val, mul: val/(step_scale**mul) },
			'j': {'attr': 'sy', 'func': lambda val, mul: val*(step_scale**mul) },
			'n': {'attr': 'sz', 'func': lambda val, mul: val/(step_scale**mul) },
			'm': {'attr': 'sz', 'func': lambda val, mul: val*(step_scale**mul) },
			'k': scale_dec,
			'l': scale_inc,

			# rotation
			'r': {'attr': 'rx', 'func': lambda val, mul: (val-step_rotate*mul)%360 },
			't': {'attr': 'rx', 'func': lambda val, mul: (val+step_rotate*mul)%360 },
			'f': {'attr': 'ry', 'func': lambda val, mul: (val-step_rotate*mul)%360 },
			'g': {'attr': 'ry', 'func': lambda val, mul: (val+step_rotate*mul)%360 },
			'v': {'attr': 'rz', 'func': lambda val, mul: (val-step_rotate*mul)%360 },
			'b': {'attr': 'rz', 'func': lambda val, mul: (val+step_rotate*mul)%360 },

			# voxelspaces
			260: prev_voxelspace, # arrow-left
			261: next_voxelspace, # arrow-right

			# special
			17: stop, # ctrl-q
		}

		def event_wrapper(func, multiplier):
			def wrapped():
				func(multiplier)
				self.update(self.transforms)
			return wrapped

		def create_hander(opts):
			def handler(mul):
				attr, func = opts['attr'], opts['func']
				t[attr] = func(t[attr], mul)

			return handler

		for char, opts in events.items():
			if callable(opts): handler = opts
			else:              handler = create_hander(opts)

			if type(char) is not int:
				events[ord(char)]         = event_wrapper(handler, 1.)
				events[ord(char.upper())] = event_wrapper(handler, shift_multiplier)
				del events[char]

		self.update(t)
		self.event_loop(events)

	def load_voxelspace(self, voxel_folder):
		self.voxels = VoxelSpace()
		self.voxels.load(voxel_folder)

		if hasattr(self, 'modulators'):
			self.modelators.stop()

		self.modulators = Modulators(
			self.transforms,
			self.voxels,
			self.update
		)

		self.modulators.start()

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

	def update(self, transforms):
		self.transforms_window.update(transforms)
		self.update_leds(transforms)

	def update_leds(self, transforms):

		leds = self.get_transformed_model(transforms)
		colors = self.voxels.getpixels(leds)

		if strip is None: return

		for i, (red, green, blue) in enumerate(colors):
			strip.set(i, red, green, blue)

		strip.update()

	def flash_leds(self):
		if strip is None: return

		for i in range(2):
			red = (i%2)*255

			for i in xrange(105):
				strip.set(i, red, 0, 0)

			strip.update()

			time.sleep(0.3)

try:
	folder = sys.argv[1]
except IndexError:
	print 'Argument missing.'
	sys.exit()

app = Domulatrix()
app.start(voxel_folder=folder)

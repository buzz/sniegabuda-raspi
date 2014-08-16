# -*- coding: utf-8 -*-

import sys
sys.stderr = open('debug.log', 'a')

import os
from os.path import exists, join, isdir
import re
import time
import threading
import curses
import time
import math

import numpy as np

from curses_pads import TransformsPad
from model import middle_sorted as leds
from logger import debug

from voxelspace.voxelspace import VoxelSpace, JsonError, fast as _voxelspace_is_fast
if _voxelspace_is_fast:
	print 'Using fast voxelspace!'
else:
	print 'Using slow voxelspace!'

time.sleep(1)

import watcher
from watcher import WatchDog

from transformations import euler_matrix
from math import radians as rad

try:
	from ledstrip import LEDStrip
	strip = LEDStrip()
except ImportError:
	strip = None

VOXELSPACES_ROOT_FOLDER = 'data/voxelspaces/'
DISPLAY_PRESSED_KEY = False
MODULATE = True

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
		self._stop = False

		self.frame = -1
		self.transforms = transforms
		self.update = update
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

	def stop(self):
		self._stop = True

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


class Domulatrix(object):

	def start(self, *args, **kw):
		def run(curses_window):
			self.stdscr = curses_window
			self.run(*args, **kw)
		curses.wrapper(run)

	def poll_keyboard(self, funcs):
		try:
			while not self._stop:
				c = self.stdscr.getch()
				if DISPLAY_PRESSED_KEY: debug('\n\nkey pressed: %s   '%c)
				if c in funcs: funcs[c]()
		except KeyboardInterrupt:
			pass

	def run(self, voxel_folder, settings_file):

		self.voxels = None
		self.modulators = None

		self.transforms_pad = TransformsPad()

		self.init_transforms()

		self.find_available_voxelspaces()
		if (voxel_folder, settings_file) in self.available_voxelspaces:
			self.current_voxelspace_idx = self.available_voxelspaces.index((voxel_folder, settings_file))
		else:
			self.current_voxelspace_idx = 0
		self.load_voxelspace(*self.available_voxelspaces[self.current_voxelspace_idx])

		self.init_watchdog()
		self.init_gui()

	def find_available_voxelspaces(self):
		self.available_voxelspaces = []

		for folder_name in os.listdir(VOXELSPACES_ROOT_FOLDER):
			folder_path = join(VOXELSPACES_ROOT_FOLDER, folder_name)
			if not isdir(folder_path): continue
			settings_files = [name for name in os.listdir(folder_path) if name.startswith('settings') and name.endswith('.json')]
			if not settings_files: continue
			layers_folder = join(folder_path, 'layers')
			layers_exist = exists(layers_folder) and bool(os.listdir(layers_folder))
			if not layers_exist: continue

			for settings_file in settings_files:
				self.available_voxelspaces.append((folder_name, settings_file))

	def init_watchdog(self):

		def reload_settings(voxelspace_folder, settings_file):
			current_voxelspace_folder, current_settings_file = self.available_voxelspaces[self.current_voxelspace_idx]
			if (voxelspace_folder == current_voxelspace_folder and settings_file == current_settings_file):
				debug('reloading current voxelspace settings.')
				self.load_voxelspace(current_voxelspace_folder, current_settings_file)

		def reload_voxelspace(voxelspace_folder, image_file):
			current_voxelspace_folder, current_settings_file = self.available_voxelspaces[self.current_voxelspace_idx]
			if (voxelspace_folder == current_voxelspace_folder):
				debug('reload current voxelspace layers.')
				self.load_voxelspace(current_voxelspace_folder, current_settings_file)

		self.watchdog = WatchDog(VOXELSPACES_ROOT_FOLDER, reload_settings, reload_voxelspace)
		self.watchdog.start()

	def init_transforms(self):
		t = self.initial_transforms = {}
		t['tx'] = t['ty'] = t['tz'] = 0
		t['sx'] = t['sy'] = t['sz'] = 100
		t['rx'] = t['ry'] = t['rz'] = 0
		t = self.transforms = self.initial_transforms.copy()

	def init_gui(self):
		self._stop = False

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
			self.current_voxelspace_idx -= 1
			self.current_voxelspace_idx %= len(self.available_voxelspaces)
			self.load_voxelspace(*self.available_voxelspaces[self.current_voxelspace_idx])

		def next_voxelspace(*args):
			self.current_voxelspace_idx += 1
			self.current_voxelspace_idx %= len(self.available_voxelspaces)
			self.load_voxelspace(*self.available_voxelspaces[self.current_voxelspace_idx])

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
			27: self.stop, # escape
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
		self.poll_keyboard(events)

	def stop(self, *args):
		self.watchdog.stop()
		self.modulators.stop()
		self._stop = True

	def load_voxelspace(self, voxel_folder, settings_file):

		settings_file = '%s/%s' % (voxel_folder, settings_file)

		# debug('XXXXXX', settings_file)
		# time.sleep(3)
		# sys.exit()

		error = None

		try:
			voxels = VoxelSpace()
			voxels.load(join(VOXELSPACES_ROOT_FOLDER, settings_file))
			modulators = Modulators(
				self.transforms,
				voxels,
				self.update
			)
		except JsonError:
			error = ('Error loading settings.py', (255, 255, 0))

		if error:
			self.flash_leds()
			debug('*** ERROR ***\n%s' % error[0])
			if not self.voxels:
				time.sleep(2)
				sys.exit()
		else:
			self.voxels = voxels
			if self.modulators: self.modulators.stop()
			self.modulators = modulators
			self.modulators.start()
			self.transforms_pad.update_voxelspace_folder(settings_file)

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
		self.transforms_pad.update_transforms(transforms)
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
	settings_path = sys.argv[1]
	voxel_folder, settings_file = re.compile('data/voxelspaces/(.*)/(settings.*\.json)').match(settings_path).groups()
except IndexError:
	print 'Argument missing.'
	sys.exit()
except AttributeError:
	print 'Path doesn\'t look right.'
	sys.exit()

domulatrix = Domulatrix()
domulatrix.start(voxel_folder, settings_file)

# -*- coding: utf-8 -*-

import curses

template_transforms = """
=============================================
voxelspace: "%s"
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

def process_template(template):
	return '\n'.join(template.replace('\t','').replace('\r','').split('\n')[1:-1])

template_transforms = process_template(template_transforms)

class TransformsPad(object):

	width = 80
	height = 20

	def __init__(self):

		self.pad = curses.newpad(100, 100)
		t = self.transforms = {}
		t['tx'] = t['ty'] = t['tz'] = -1
		t['rx'] = t['ry'] = t['rz'] = -1
		t['sx'] = t['sy'] = t['sz'] = -1
		self.voxelspace_folder = 'n/a'

	def update_transforms(self, transforms):
		self.transforms = transforms
		self.update()

	def update_voxelspace_folder(self, voxelspace_folder):
		self.voxelspace_folder = voxelspace_folder
		self.update()

	def update(self):
		t = self.transforms
		pad = self.pad

		rendered = template_transforms % (
			self.voxelspace_folder,
			t['tx'], t['ty'], t['tz'],
			t['rx'], t['ry'], t['rz'],
			t['sx'], t['sy'], t['sz']
		)

		lines = rendered.split('\n')
		width = 0
		for y, line in enumerate(lines):
			pad.addstr(y, 0, line)

		width = max(len(line) for line in lines)
		height = len(lines)
		pad.refresh(0,0, 0,0, height,width)
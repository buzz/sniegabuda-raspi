import sys
import os
import re
import time

import threading
from watchdog.observers import Observer
from watchdog.events import FileCreatedEvent, FileDeletedEvent, FileModifiedEvent

def normpath(path):
	return os.path.normpath(path).replace('\\', '/')

re_settings = re.compile('^data/voxelspaces/(.*)/(settings(.*)\.json)$')
re_layer    = re.compile('^data/voxelspaces/(.*)/layers/((.*)\.(png|jpg))$')

class WatchHandler(object):
	def __init__(self, change_settings_handler, change_layers_handler):
		self.change_settings_handler = change_settings_handler
		self.change_layers_handler = change_layers_handler

	def dispatch(self, event):

		# print '--->', type(event), normpath(event.src_path)

		if type(event) not in (FileCreatedEvent, FileDeletedEvent, FileModifiedEvent):
			return

		path = normpath(event.src_path)

		match_settings = re_settings.match(path)
		if type(event) is FileModifiedEvent and match_settings:
			voxelspace_folder, settings_file, _ = match_settings.groups()
			self.change_settings_handler(voxelspace_folder, settings_file)
			return

		match_layer = re_layer.match(path)
		if type(event) in (FileCreatedEvent, FileDeletedEvent, FileModifiedEvent) and match_layer:
			voxelspace_folder, image_file, _, _ = match_layer.groups()
			self.change_layers_handler(voxelspace_folder, image_file)

class WatchDog(threading.Thread):
	def __init__(self, path, change_settings_handler, change_layers_handler):
		threading.Thread.__init__(self)
		self._stop = False

		self.path = path
		self.change_settings_handler = change_settings_handler
		self.change_layers_handler   = change_layers_handler

	def run(self):

		event_handler = WatchHandler(self.change_settings_handler, self.change_layers_handler)
		observer = Observer()
		observer.schedule(event_handler, self.path, recursive=True)
		observer.start()

		try:
			while not self._stop:
				time.sleep(0.1)
		except KeyboardInterrupt:
			pass

		observer.stop()
		observer.join()

	def stop(self):
		self._stop = True

if __name__ == "__main__":
	path = 'data/voxelspaces'

	def reload_settings(voxelspace_folder, settings_file):
		print '*** reload_settings:', voxelspace_folder, settings_file

	def reload_voxelspace(voxelspace_folder, image_file):
		print '*** reload_voxelspace:', voxelspace_folder, image_file

	dog = WatchDog(path, reload_settings, reload_voxelspace)
	dog.start()

	try:
		while True:
			time.sleep(0.1)
	except KeyboardInterrupt:
		dog.stop()

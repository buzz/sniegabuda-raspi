import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileCreatedEvent, FileDeletedEvent, FileModifiedEvent

def normpath(path):
	return os.path.normpath(path).replace('\\', '/')

class WatchHandler(object):

	def dispatch(self, event):
		global e
		e = event

		path = normpath(event.src_path)
		print type(event), event

if __name__ == "__main__":
	path = 'data/voxelspaces'

	event_handler = WatchHandler()
	observer = Observer()
	observer.schedule(event_handler, path, recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(0.1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def debug(*args):
	args = args or ('',)
	logging.debug(' '.join(unicode(arg) for arg in args))

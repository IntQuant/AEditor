import pathlib
import threading
import sys
import locale

from kivy.logger import Logger

current = {}
load_thread = None


def init():
	lc = locale.getdefaultlocale()[0]
	available = get_lang_list()
	fitting = list(filter(lambda x:lc in x, available))

	if len(fitting) > 0:
		thread_load(fitting[0])
	else:
		thread_load()


def get_int(name, default=0):
	ret = get(name)
	if ret.isalnum():
		return int(ret)
	else:
		return default


def get(name):
	global current
	join()
	if name in current:
		return current[name]
	else:
		return name


def join():
	global load_thread
	if load_thread:
		load_thread.join()
		Logger.info("l18n: Joined loading thread")
	load_thread = None


def get_lang_list():
	return list(
	  map(lambda x:x.name, 
	  filter(lambda x:x.is_dir()==False, 
	  pathlib.Path("./lang").iterdir()
	  )))

	
def thread_load(lang="en_US"):
	#print("Starting loader thread")
	global load_thread
	load_thread = threading.Thread(target=load, kwargs={"lang":lang})
	load_thread.start()
	Logger.info("l18n: Started loader thread")


def load(lang="en_US"):
	global current
	
	if lang!="en_US":
		load()
	
	with open("./lang/"+lang, 'r') as f:
		for line in f:
			try:
				ind, val = line.split("=")
				current[ind] = val[:-1]
			except:
				Logger.warning("l18n: error while parsing '%s'" % line)
	Logger.info("l18n: Loaded %s" % lang)

	
if __name__ == "__main__":
	print(get_lang_list())
	thread_load()
	load_thread.join()
	print(current)

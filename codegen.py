from threading	import Thread

def generate(state):
	Thread(target = gen, args = (state)).start()

def gen(state):
	print(state)

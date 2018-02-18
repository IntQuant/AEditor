from threading			import Thread
from kivy.logger 		import Logger

import editor_visual

def generate(state):
	Thread(target = gen, args = [state]).start()

def gen(state):
	Logger.info("Staring code generation")
	Logger.info("Starting translation")
	code_pieces = []
	connections, snippets = map(list, state)
	for snp in snippets:
		if isinstance(snp, editor_visual.StartSnippet):
			snp.handle_codegen(connections, snippets)
	
	
	Logger.info("Ended translation")
	Logger.info("Ended code generation")
	

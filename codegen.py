from threading			import Thread
from kivy.logger 		import Logger

import editor_visual

def flatten(lst): #TODO: non-recursive
	for lst_item in lst:
		if isinstance(lst_item, list):
			yield from flatten(lst_item)
		else:
			yield lst_item

def generate(state):
	Thread(target = gen, args = [state]).start()

def gen(state):
	Logger.info("Staring code generation")
	Logger.info("Starting translation")
	code_pieces = []
	#code_pieces.append("""#include <avr/io.h>""")
	with open("headers.C", 'r') as f:
		code_pieces.append(f.readlines())
	code_pieces.append("""int main(void) { """)
	connections, snippets = map(list, state)
	for snp in snippets:
		if isinstance(snp, editor_visual.StartSnippet):
			code_pieces.append(snp.handle_codegen(connections, snippets))
	#print(code_pieces)
	code_pieces.append("}")
	
	code = "\n".join(flatten(code_pieces))
	print(code)
	
	Logger.info("Ended translation")
	Logger.info("Ended code generation")
	

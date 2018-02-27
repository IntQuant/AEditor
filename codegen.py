from threading			import Thread
import pathlib
import subprocess
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
		code_pieces.append(f.read())
	code_pieces.append("""int main(void) { """)
	connections, snippets = map(list, state)
	for snp in snippets:
		if isinstance(snp, editor_visual.StartSnippet):
			code_pieces.append(snp.handle_codegen(connections, snippets))
	#print(code_pieces)
	code_pieces.append("for (;;) {}")
	code_pieces.append("}")
	
	code = "\n".join(flatten(code_pieces))
	#print(code)
	
	Logger.info("Ended translation")
	
	base_path = pathlib.Path("./tmp/codegen/")
	base_path.mkdir(exist_ok=True, parents=True)
	
	for path in base_path.glob("**/*"):
		if path.is_dir:
			#path.rmdir()
			pass
		else:	
			path.unlink()
	
	code_file_name = "code"
	code_file_path = (base_path / ("%s.C" % code_file_name))
	#with code_file_path.open("w") as f:
	#	f.write(code)
	with open("code.C", "w") as f:
		f.write(code)
	
	subprocess.run("./compile_and_upload.sh", shell=True)
	"""
	avrgcc = subprocess.run(["avr-gcc", "-mmcu=atmega328p", "{0}.C".format(base_path / code_file_name), "-o", "{0}.elf".format(base_path / code_file_name)], stdout=subprocess.PIPE) 
	print(avrgcc)
	avrobj = subprocess.run(["avr-objcopy", "-j .text -O ihex", "{0}.elf".format(base_path / code_file_name), "{0}.hex".format(base_path / code_file_name)])
	print(avrobj)
	#avrdude = subprocess.run(["avrdude", "-v -patmega328p -carduino -P/dev/ttyUSB0 -b115200 -D", "-Uflash:r:%s.hex:i" % (base_path / code_file_name)])
	avrdude = subprocess.run("avrdude -v -patmega328p -carduino -P/dev/ttyUSB0 -b115200 -D -Uflash:w:tmp/codegen/code.hex:i", shell=True)
	print(avrdude)
	"""
	Logger.info("Ended code generation")
	

from enum import Enum



class ConnectionInfo():
	def __init__(self, color):
		assert len(color) in [3, 4]
		
		if len(color) == 3:
			color = [color[0], color[1], color[2], 1]
		
		self.color = color
	
	
	def unpack(self):
		return (self.color, )



class ConnectionType(Enum):
	PROPAGATE 	= ConnectionInfo((1, 1, 1, 1))
	INT 		= ConnectionInfo((0.1, 0.5, 1, 1))
	BOOL 		= ConnectionInfo((0.5, 0.7, 0.5, 1))



class Connection():
	def __init__(self, inp, out, conn_type):
		self.input = inp
		self.output =out
		self.conn_type = self.input.conn_type
		self.valid = True
	
	
	def get_color(self):
		return self.conn_type.value.color



class Connector():
	def __init__(self, conn_type, parent, is_inp, name=""):
		#print("Created connector", self, "with", conn_type, parent, is_inp, name)
		self.conn_type = conn_type
		self.parent = parent
		self.is_inp = is_inp
		self.name = name
		self.button = None
	
	
	def get_pos(self):
		if self.button:
			return self.button.center # TODO
		else:
			return (0, 0)


if __name__ == "__main__":
	for conn in ConnectionType:
		val = ("%s %s" % (conn.name, str(conn.value.unpack()).rjust(50-len(conn.name), ' '))).expandtabs()
		print(val)

from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.uix.widget 			import Widget
from kivy.app 					import App
from kivy.uix.floatlayout		import FloatLayout
from kivy.uix.boxlayout			import BoxLayout
from kivy.uix.button			import Button
from kivy.properties			import ObjectProperty, ListProperty, \
									   BooleanProperty, StringProperty, \
									   NumericProperty
from kivy.clock 				import Clock
from kivy.core.window 			import Window
from kivy.graphics 				import Color, Line, InstructionGroup
from kivy.logger 				import Logger
from kivy.uix.textinput 		import TextInput

from QLibs 						import qvec

from connections 				import Connection, ConnectionType, Connector
from codegen 					import generate

MOVE_BUTTON = "right"

snippets = []

app = None
next_uuid = -1

def get_next_uuid():
	global next_uuid
	next_uuid += 1
	return (hex(next_uuid-1)[2:]).rjust(16, '0')


def set_app(p_app):
	global app
	app = p_app


def get_var_name_by_connector(connector):
	return "dev_" + connector.parent.uuid + "_" + connector.name

def get_var_name(uuid, name):
	return "dev_" + uuid + "_" + name

class VisualSnippet(BoxLayout):
	
	conn_area 	= ObjectProperty(None)
	editor 		= ObjectProperty(None)
	valid 		= BooleanProperty(True)
	
	def invalidate(self):
		self.valid = False
	
	def handle_codegen(self, connections, snippets):
		return """/*NO GENERATED CODE FROM %s*/\n""" % self.get_snippet_name()
	
	def connector_factory(self, connector):
		bt = Button(text=connector.name)
		def disp(*args):
			if connector.is_inp:
				self.editor.connection_starter 	= connector
			else:
				self.editor.connection_ender 	= connector
			self.editor.try_to_make_connection()
			
		connector.button = bt
		bt.bind(on_press=disp)
		return bt
	
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.on_next_sched)
		self.uuid = get_next_uuid()
	
		
	def get_state(self):
		return {}
	
	
	def on_next_sched(self, dt):
		if self.conn_area:
			for connector in self.get_connectors():
				self.conn_area.add_widget(self.connector_factory(connector))
		else:
			Clock.schedule_once(self.on_next_sched, 1)
	
	@staticmethod
	def get_snippet_name():
		return "None"
	
	
	def get_connectors(self):
		return (
			Connector(ConnectionType.PROPAGATE, self, True, name='input'),
			Connector(ConnectionType.PROPAGATE, self, False, name='output')
			)
	
	
	def on_touch_down(self, touch):
		if touch.button == MOVE_BUTTON and self.collide_point(touch.x, touch.y):
			touch.grab(self)
			return True
		
		return super().on_touch_down(touch)
	
	
	def on_touch_move(self, touch):
		if touch.button == MOVE_BUTTON:
			if touch.grab_current is self:
				self.pos = self.pos[0] + touch.dx, self.pos[1] + touch.dy
				return True
		
		return super().on_touch_move(touch)
	
	
	def on_touch_up(self, touch):		
		if touch.button == MOVE_BUTTON and self.collide_point(touch.x, touch.y):
			if touch.grab_current is self:
				touch.ungrab(self)
				return True
		
		return super().on_touch_up(touch)



class StartSnippet(VisualSnippet):
	@staticmethod
	def get_snippet_name():
		return "On Init"
	
	def get_connectors(self):
		return (
		  Connector(ConnectionType.PROPAGATE, self, False, name='output'),
		  )
	
	def handle_codegen(self, connections, snippets):
		code_pieces = []
		stack = []
		prv = None
		csnp = self
		for conn in connections:
			print(conn.input.name, conn.input.is_inp, conn.output.name, conn.output.is_inp)
		
		while prv!=csnp:
			csnp_all = []
			for conn in connections:
				if conn.output.parent is csnp and conn.conn_type == ConnectionType.PROPAGATE:
					csnp_all.append(conn.input.parent)
			stack += csnp_all
			
			prv = csnp
			if len(stack)>0:
				csnp = stack.pop()
				code_pieces.append(csnp.handle_codegen(connections, snippets))
		
		return code_pieces	
			
			

class SimpleSnippetGen():
	@staticmethod
	def make(name, cd, codegen):
		class SimpleSnippet(VisualSnippet):
			def __init__(self, **kwargs):
				super().__init__(**kwargs)
				self.connector_data = cd
				self.connectors = None
			
			@staticmethod
			def get_snippet_name():
				return name
			
			def get_connectors(self):
				if self.connectors:
					return self.connectors
				else:
					self.connectors = [Connector(ConnectionType[conn_spec["type"]], self, is_inp=conn_spec['input']=="true", name=conn_spec["name"]) for conn_spec in self.connector_data]
					return self.connectors
			
			def handle_codegen(self, connections, snippets):
				try:
					if codegen:
						connectors = self.get_connectors()
						frm = {}
						print(len(connectors))
						for conn in connectors:
							#print(conn.name, conn.is_inp)
							if conn.is_inp:
								for connection in connections:
									if connection.input is conn:
										frm[conn.name] = (get_var_name_by_connector(connection.output))
										break
							else:
								frm[conn.name]	= get_var_name_by_connector(conn)
						return codegen.format(**frm)
					else:
						return super().handle_codegen(connections, snippets)
				except Exception as e:
					print("Exception encoutered while handling codegen of %s" % name)
					raise e
		return SimpleSnippet
	@staticmethod
	def init():
		from json import load
		with open("snippets.json", "r") as f:
			for snp in load(f):
				if "name" in snp and "connections" in snp:
					snippet = SimpleSnippetGen.make(snp["name"], snp["connections"], snp["codegen"] if "codegen" in snp else None)
					Logger.info("visual: registered snippet '%s'" % snp["name"])
					snippets.append(snippet)

class SetVariable(VisualSnippet):
	@staticmethod
	def get_snippet_name():
		return "SetVariable"

	def text_input_factory(self):
		def cb(text):
			self.var_name = "usr_" + text.text
		
		ti = TextInput(multiline=False, size_hint_y=None, height=30, on_text_validate=cb)
		return ti

	def on_next_sched(self, dt):
		if self.conn_area:
			self.conn_area.add_widget(self.text_input_factory())
		super().on_next_sched(dt)

	def get_state(self):
		return {"var_name":self.var_name}
	
	def get_connectors(self):
		return (
			Connector(ConnectionType.INT, self, True, name="value"),
		) + super().get_connectors()
		
		

class GetVariable(VisualSnippet):
	var_name = StringProperty()
	@staticmethod
	def get_snippet_name():
		return "GetVariable"
	
	def get_state(self):
		return {"var_name":self.var_name}
	
	def get_connectors(self):
		return (
			Connector(ConnectionType.INT, self, False, name="value"),
		) + super().get_connectors()
	
	def text_input_factory(self):
		def cb(text):
			self.var_name = "usr_" + text.text
		
		ti = TextInput(multiline=False, size_hint_y=None, height=30, on_text_validate=cb)
		return ti
		
	
	def on_next_sched(self, dt):
		if self.conn_area:
			self.conn_area.add_widget(self.text_input_factory())
		super().on_next_sched(dt)



class IntInput(TextInput):
	def insert_text(self, pat, from_undo=False):
		s = "".join([ch for ch in pat if ch.isalnum() if int(ch) in range(10)])
		return super(IntInput, self).insert_text(s, from_undo=from_undo)
	def on_enter(self):
		self.text = str(int(self.text))



class IntValue(VisualSnippet):
	value = NumericProperty(0)
	@staticmethod
	def get_snippet_name():
		return "ValueInt"
	
	def get_connectors(self):
		return (
			Connector(ConnectionType.INT, self, False, name="value"),
		) + super().get_connectors()
	
	def handle_codegen(self, connections, snippets):
		return "int %s = %s;" % (get_var_name(self.uuid, "value"), self.value)
	
	def text_input_factory(self):
		def cb(text):
			self.value = int(text.text)
		
		ti = IntInput(multiline=False, size_hint_y=None, height=30, on_text_validate=cb, text="0")
		return ti
		
	
	def on_next_sched(self, dt):
		if self.conn_area:
			self.conn_area.add_widget(self.text_input_factory())
		super().on_next_sched(dt)


snippets.append(StartSnippet)
snippets.append(SetVariable)
snippets.append(GetVariable)
snippets.append(IntValue)

class VisualEditor(FloatLayout):
	grid_lay			= ObjectProperty(None)
	snippet_area		= ObjectProperty(None)
	connections 		= ListProperty([])

	
	def __init__(self, **kwargs):
		global app
		
		Clock.schedule_once(self.init_grid_lay, 1)
		Clock.schedule_interval(self.update, 1/20)
		super(VisualEditor, self).__init__(**kwargs)
		Window.bind(on_motion=self.on_motion)
		
		self.connection_starter	= None
		self.connection_ender	= None
		
		app.editor = self
		
		self.line_group = InstructionGroup()
		self.canvas.add(self.line_group)
	
	def get_state(self):
		return (self.connections, self.snippet_area.children)
	
	def update(self, dt):
		if len(self.connections)>0:
			self.line_group.clear()
			for conn in self.connections:
				self.line_group.add(Color(*conn.get_color()))           #TODO
				self.line_group.add(Line(points=(conn.input.get_pos()+conn.output.get_pos()), width=1))
		else:
			self.line_group.clear()
					
			
	def try_to_make_connection(self):
		if self.connection_starter and self.connection_ender and \
		self.connection_starter.conn_type == self.connection_ender.conn_type and \
		self.connection_starter.parent is not self.connection_ender.parent:
			
			for conn in self.connections:
				if conn.input == self.connection_starter and conn.output == self.connection_ender:
					break
			else:
				self.connections.append(Connection(self.connection_starter, self.connection_ender, self.connection_ender.conn_type))
			
			self.connection_starter = None
			self.connection_ender = None
		
			
	def on_motion(self, etype, stm ,touch):
		mult = 0
		
		if touch.is_mouse_scrolling:
			if touch.button == 'scrolldown':
				mult = 0.1
			if touch.button == 'scrollup':
				mult = -0.1
		else:
			return
		
		if self.collide_point(touch.x, touch.y):
			for child in self.snippet_area.children:
				if child.collide_point(touch.x, touch.y):
					break
			else:
				if touch.is_mouse_scrolling:
					for child in self.snippet_area.children:
						tv = qvec.VecNd(tuple(child.pos)) - qvec.VecNd(tuple(touch.pos))
						tv *= mult
						child.pos = (qvec.VecNd(child.pos) + tv).to_tuple()
	
	
	def on_touch_down(self, touch):
		if super().on_touch_down(touch):
			return True
		
		if touch.button == MOVE_BUTTON and self.collide_point(touch.x, touch.y):
			for child in self.snippet_area.children:
				if child.collide_point(touch.x, touch.y):
					break
			else:
				touch.grab(self)
				return True
		
		return super().on_touch_down(touch)
	
	
	def on_touch_move(self, touch):
		if super().on_touch_move(touch):
			return True
		
		if touch.button == MOVE_BUTTON:
			if touch.grab_current is self:
				for child in self.snippet_area.children:
					child.pos[0] += touch.dx
					child.pos[1] += touch.dy
				return True
	
		
	def on_touch_up(self, touch):
		if super().on_touch_up(touch):
			return True
		
		if touch.button == MOVE_BUTTON and self.collide_point(touch.x, touch.y):
			if touch.grab_current is self:
				touch.ungrab(self)
				return True
	
	
	def button_factory(self, snippet):
		def f(*args):
			snp = snippet()
			snp.editor = self
			self.snippet_area.add_widget(snp)
			snp.pos=(self.snippet_area.height / 2, self.snippet_area.width / 2)
		b = Button(size_hint_y=None, height=40, text=snippet.get_snippet_name())
		b.bind(on_press=f)
		return b
	
	
	def init_grid_lay(self, *args):
		global snippets
		for snippet in snippets:
			self.add_child_to_grid_lay(self.button_factory(snippet))	
	
	
	def add_child_to_grid_lay(self, child):
		if self.grid_lay:
			self.grid_lay.add_widget(child)
			
			target_height = 0
			
			for child in self.grid_lay.children:
				target_height += child.height
			
			self.grid_lay.height = target_height

	
	def update_connections(self):
		for conn in self.connections[:]:
			if not (conn.input.parent.valid and conn.output.parent.valid):
				self.connections.remove(conn)

	
	def remove_snippet(self, snippet):
		snippet.invalidate()
		self.snippet_area.remove_widget(snippet)
		self.update_connections()

	def generate(self):
		generate(self.get_state())

SimpleSnippetGen.init()


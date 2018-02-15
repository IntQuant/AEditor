from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.uix.widget 			import Widget
from kivy.app 					import App
from kivy.uix.floatlayout		import FloatLayout
from kivy.uix.boxlayout			import BoxLayout
from kivy.uix.button			import Button
from kivy.properties			import ObjectProperty, ListProperty, BooleanProperty
from kivy.clock 				import Clock
from kivy.core.window 			import Window

from QLibs 						import qvec

from connections import Connection, ConnectionType, Connector

MOVE_BUTTON = "right"

snippets = []



class VisualSnippet(BoxLayout):
	
	conn_area 	= ObjectProperty(None)
	editor 		= ObjectProperty(None)
	valid 		= BooleanProperty(True)
	
	def invalidate(self):
		self.valid = False
	
	def connector_factory(self, connector):
		bt = Button(text=connector.name)
		def disp(*args):
			if connector.is_inp:
				self.editor.connection_starter 	= connector
			else:
				self.editor.connection_ender 	= connector
			self.editor.try_to_make_connection()
			
		bt.bind(on_press=disp)
		return bt
	
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.on_next_sched)
	
		
	def get_state(self):
		return ()
	
	
	def on_next_sched(self, dt):
		if self.editor:
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
				#print(touch.dx, touch.dy)
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



class GetInputSnippet(VisualSnippet):
	@staticmethod
	def get_snippet_name():
		return "Get Input"
	
	
	def get_connectors(self):
		return (
		  Connector(ConnectionType.PROPAGATE, self, True, name='input'),
		  Connector(ConnectionType.PROPAGATE, self, False, name='output'),
		  Connector(ConnectionType.BOOL, self, False, name="value"),
		  )



class SetOutputSnippet(VisualSnippet):
	@staticmethod
	def get_snippet_name():
		return "Set Output"
	
	
	def get_connectors(self):
		return (
		  Connector(ConnectionType.PROPAGATE, self, True, name='input'),
		  Connector(ConnectionType.BOOL, self, True, name="value"),
		  Connector(ConnectionType.PROPAGATE, self, False, name='output'),
		  )



#snippets.append(VisualSnippet)
snippets.append(StartSnippet)
snippets.append(GetInputSnippet)
snippets.append(SetOutputSnippet)



class VisualEditor(FloatLayout):
	grid_lay			= ObjectProperty(None)
	snippet_area		= ObjectProperty(None)
	connections 		= ListProperty([])

	
	def __init__(self, **kwargs):
		Clock.schedule_once(self.init_grid_lay, 1)
		super(VisualEditor, self).__init__(**kwargs)
		Window.bind(on_motion=self.on_motion)
		
		self.connection_starter	= None
		self.connection_ender	= None
	
	
	def try_to_make_connection(self):
		if self.connection_starter and self.connection_ender and \
		self.connection_starter.conn_type == self.connection_ender.conn_type and \
		self.connection_starter.parent is not self.connection_ender.parent:
			
			for conn in self.connections:
				if conn.input == self.connection_starter and conn.output == self.connection_ender:
					break
			else:
				print("Can make connection!")
				self.connections.append(Connection(self.connection_starter, self.connection_ender, self.connection_ender.conn_type))
			
			self.connection_starter = None
			self.connection_ender = None
		print(self.connections)
		
			
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
					#print("Scrolling")
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
				#print(touch.dx, touch.dy)
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
		b = Button(size_hint_y=None, height=100, text=snippet.get_snippet_name())
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
			print(conn.input.parent, conn.output.parent)
			if not (conn.input.parent.valid and conn.output.parent.valid):
				self.connections.remove(conn)
	
	def remove_snippet(self, snippet):
		try: #TODO: remove connections on widget removing
			child = snippet
			print(child)
			print(snippet)
			snippet.invalidate()
			self.snippet_area.remove_widget(snippet)
			self.update_connections()
			print("Success!")
		except Exception as e:
			print(e)

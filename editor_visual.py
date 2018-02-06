from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.uix.widget 			import Widget
from kivy.app 					import App
from kivy.uix.floatlayout		import FloatLayout
from kivy.uix.boxlayout			import BoxLayout
from kivy.uix.button			import Button
from kivy.properties			import ObjectProperty
from kivy.clock 				import Clock

MOVE_BUTTON = "right"

snippets = []

class VisualSnippet(BoxLayout):
	@staticmethod
	def get_snippet_name():
		return "BASIC"
	
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

snippets.append(VisualSnippet)

class VisualEditor(FloatLayout):
	grid_lay = ObjectProperty(None)
	snippet_area = ObjectProperty(None)
	
	def __init__(self, **kwargs):
		Clock.schedule_once(self.init_grid_lay, 1)
		super(VisualEditor, self).__init__(**kwargs)
	
	def button_factory(self, snippet):
		def f(*args):
			snp = snippet()
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



class EditorVisualApp(App):
		def build(self):
			return VisualEditor()

if __name__ == "__main__":
	EditorVisualApp().run()

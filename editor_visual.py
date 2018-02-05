from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.uix.widget 			import Widget
from kivy.app 					import App
from kivy.uix.floatlayout		import FloatLayout
from kivy.uix.boxlayout			import BoxLayout

MOVE_BUTTON = "right"

class VisualSnippet(BoxLayout):
	def on_touch_down(self, touch):
		if touch.button == MOVE_BUTTON and self.collide_point(touch.x, touch.y):
			touch.grab(self)
			return True
		
		super().on_touch_down(touch)
	
	def on_touch_move(self, touch):
		if touch.button == MOVE_BUTTON:
			if touch.grab_current is self:
				self.pos = self.pos[0] + touch.dx, self.pos[1] + touch.dy
				return True
		
		super().on_touch_move(touch)
		
	def on_touch_up(self, touch):		
		if touch.button == MOVE_BUTTON and self.collide_point(touch.x, touch.y):
			if touch.grab_current is self:
				touch.ungrab(self)
				return True
		
		super().on_touch_up(touch)

class VisualEditor(FloatLayout):
	pass


class EditorVisualApp(App):
		def build(self):
			return VisualEditor()

if __name__ == "__main__":
	EditorVisualApp().run()

from kivy.app import App
from kivy.uix.widget import Widget

class MainWidget(Widget):
	pass


class AEditorApp(App):
	def build(self):
		return MainWidget()


AEditorApp().run()

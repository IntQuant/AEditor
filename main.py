import l18n

l18n.init()

from kivy.app		 	import App
from kivy.uix.widget 	import Widget
from kivy.clock 		import Clock
from kivy.logger 		import Logger
from kivy.properties	import ObjectProperty

from editor_visual 		import VisualEditor, set_app

class MainWidget(Widget):
	def init_all(self):
		Clock.schedule_once(self.init, 5)
	def init(self, dt):
		for child in self.walk():
			#print(child)
			if hasattr(child, "ae_init"):
				child.ae_init()
				Logger.info("Initialized %s" % child)



class AEditorApp(App):
	editor = ObjectProperty(None)
	
	def build(self):
		MW = MainWidget()
		MW.init_all()
		return MW
	def generate(self):
		if self.editor:
			self.editor.generate()

if __name__ == "__main__":
	app = AEditorApp()
	set_app(app)
	app.run()

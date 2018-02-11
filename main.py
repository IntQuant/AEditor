import l18n

l18n.init()

from kivy.app		 	import App
from kivy.uix.widget 	import Widget
from kivy.clock 		import Clock
from kivy.logger 		import Logger

from editor_visual 		import VisualEditor

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
	def build(self):
		MW = MainWidget()
		MW.init_all()
		return MW

AEditorApp().run()

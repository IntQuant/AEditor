import l18n
import locale

lc = locale.getdefaultlocale()[0]
available = l18n.get_lang_list()
fitting = list(filter(lambda x:lc in x, available))
if len(fitting) > 0:
	l18n.thread_load(fitting[0])
else:
	l18n.thread_load()

from kivy.app import App
from kivy.uix.widget import Widget
import kivy.resources

#kivy.resources.resource_add_path('C:\Windows\Fonts')

from editor_visual import VisualEditor

class MainWidget(Widget):
	pass


class AEditorApp(App):
	def build(self):
		return MainWidget()

l18n.join()
print(l18n.current)
AEditorApp().run()

import kivy
kivy.require('2.1.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class Staff(Widget):
    pass

class TickLineMetronomeApp(App):
    def build(self):
        return Staff()
		
if __name__ == '__main__':
    TickLineMetronomeApp().run()

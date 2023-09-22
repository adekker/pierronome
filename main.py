import kivy
kivy.require('2.1.1')

from kivy.app import App
from kivy.uix.label import Label

class Pierronome(App):

	def build(self):
		return Label(text='Hello world')
		
if __name__ == '__main__':
	Pierronome().run()
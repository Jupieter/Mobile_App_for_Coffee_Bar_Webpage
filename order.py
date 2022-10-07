from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox

Builder.load_file('kv/order.kv')

class CoffeOrder(MDGridLayout):
	print('CoffeOrder 0')
	
	def __init__(self, **kwargs):
		super(CoffeOrder, self).__init__(**kwargs)

	def oreder_press_dose(self, act_choice, dose_grid):
		'''One Choice button selection function'''
		print('One Choice button selection function')
		for dose_but in self.ids[dose_grid].children:
			print(dose_but)
			print(dose_but.text, dose_but.text_color)
			dose_but.selected = False
			dose_but.text_color=[0, 0, 0, 0.3]
			dose_but.md_bg_color = [0.5, 0.5, 0.5, 1]
			act_choice.text_color=(1, 1, 1, 1)
			act_choice.md_bg_color=(0, 0.5, 0, 1)
			print(act_choice.value)

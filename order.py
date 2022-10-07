from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from login import LogInCard

Builder.load_file('kv/order.kv')

class CoffeOrder(MDGridLayout):
	print('CoffeOrder 0')
	
	def __init__(self, **kwargs):
		super(CoffeOrder, self).__init__(**kwargs)
		self.app = MDApp.get_running_app()

	def oreder_press_dose(self, act_choice, dose_grid):
		'''One Choice button selection function'''
		for dose_but in self.ids[dose_grid].children:
			# print(dose_but)
			# print(dose_but.text, dose_but.text_color)
			dose_but.selected = False
			dose_but.text_color=[0, 0, 0, 0.3]
			dose_but.md_bg_color = [0.5, 0.5, 0.5, 1]
			act_choice.text_color=(1, 1, 1, 1)
			act_choice.md_bg_color=(0, 0.5, 0, 1)
		print('One Choice button selection function', act_choice.value)
		self.ids[dose_grid].value = act_choice.value

	def btn_text_reset(self, dose_grid):
		print("RESET", self.ids)
		# self.app = MDApp.get_running_app()
#
		self.ids[dose_grid].value = 0
		for dose_but in self.ids[dose_grid].children:
			print(dose_but.text, dose_but.text_color)
			dose_but.text_color=[1, 1, 1, 0.6]
			dose_but.md_bg_color = self.app.theme_cls.primary_color
		# self.button_able(dose_grid)
	
	def button_able(self, dose_grid, *args):
		'''buttun disabled if not authenticated 
			disabled TimePicker if Date not selected
			disabled SAVE button if all option isn't selected.
		'''
		log_card = LogInCard()
		active_token, token_auth = log_card.load_token()
		# active_user, act_pkey, act_staff = log_card.read_user()
		scr2 = MDApp.get_running_app().scr_2_mess_lbl
		print(scr2, active_token)
		if active_token == 'Empty':
			able = True
			scr2.text = "Isn't valid login with staff status"
		else:
			able = False
			scr2.text = "Set the parameters:"
		print('able',able)
		for button1 in self.ids[dose_grid].children:
			button1.disabled = able
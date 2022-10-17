from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from login import LogInCard
from coffe_make import CoffeWare
import requests
import json

Builder.load_file('kv/order.kv')

class CoffeOrder(MDGridLayout):
	print('CoffeOrder 0')
	ordered = [[],[],[],[]]
	ware_step_lst = [0,0,0,0]
	
	def __init__(self, **kwargs):
		super(CoffeOrder, self).__init__(**kwargs)
		self.app = MDApp.get_running_app()
		# Clock.schedule_once(self.load_data_ware, 0)
	
	def ware_ordr_btn(self, btn_id, *args):
		''' carussel button => selected coffee raw material'''
		# print("self.ordered", self.ordered)
		w_order = self.ordered[btn_id]
		if w_order != []:
			btn_text = "order_btn_" + str(btn_id)
			lbl_text = "order_end_label_A_" + str(btn_id)
			grd_text = "dose_grid_" + str(btn_id)
			tuple_len = len(w_order)
			# print("Have Ware: ", btn_text, "len: ", w_order)
			self.ware_step_lst[btn_id] += 1
			if self.ware_step_lst[btn_id] > tuple_len:
				self.ware_step_lst[btn_id] = 1
			w_step = self.ware_step_lst[btn_id]-1
			ware = json.loads(w_order[w_step])
			w_id = ware['w_id']
			w_name = ware['w_name']   # .replace('Coffee','')
			w_name.replace(',','')
			w_dose = ware['w_dose']
			print("w_step", w_step, w_id, w_name, w_dose)
			texte = str(w_id) + " " + w_name + "\n  " + str(w_dose) +" dose"
			print(texte, btn_text)
			self.ids[btn_text].text = texte
			self.ids[btn_text].md_bg_color=(0, 0.5, 0, 1)
			self.ids[btn_text].value = w_id
			# SAVE Card text: 
			dose = self.ids[grd_text].value 
			self.ids[lbl_text].text = texte
			self.button_able(btn_id, w_id)
			# Clock.schedule_once(self.button_able, 0)
		else:
			self.ids.order_label_0.text = "Something went wrong. No ware data"
	
	def load_data_ware(self, *args):
		print('coffe order data')
		cw = CoffeWare()
		log_card = LogInCard()
		active_token, hd_token= log_card.load_token()
		if active_token == 'Empty':
			print('token print active_token: ',active_token)
		try:
			wares = requests.get('http://127.0.0.1:8000/c_app/order_tastes/').json()
			print("-----------------wares----------------------")
			for i in range(4):
				self.ordered[i] = wares[i]	
			print('store ware: ', self.ordered)	
			# return self.ordered
		except:
			# self.ids.order_label_0.text = "New coffee brewing time saved."
			print("-----------------problem----------------------")
			print("Problem with internet conection")


	def oreder_press_dose(self, act_choice, btn_id):
		'''One Choice button selection function'''
		dose_grid = "dose_grid_" + str(btn_id)
		print(dose_grid)
		lbl_text = "order_end_label_B_" + str(btn_id)
		print(lbl_text)
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
		self.ids[lbl_text].text = str(act_choice.value) + "  ordered dose"
		# lbl_text = act_choice.value + " dose"

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
	
	def button_able(self, btn_id, w_id, *args):
		'''buttun disabled if not authenticated 
			disabled TimePicker if Date not selected
			disabled SAVE button if all option isn't selected.
		'''
		print("btn_id, w_id", btn_id, w_id)
		log_card = LogInCard()
		active_token, token_auth = log_card.load_token()
		# active_user, act_pkey, act_staff = log_card.read_user()
		scr2 = MDApp.get_running_app().scr_2_mess_lbl
		dose_grid = "dose_grid_" + str(btn_id)
		print(scr2, active_token)
		if active_token == 'Empty' and w_id == 0:
			able = True
			# scr2.text = "Isn't valid login with staff status"
		else:
			able = False
			# scr2.text = "Set the parameters:"
		print('able',able)
		print('able 2 :', self.ids[dose_grid].children)
		for button1 in self.ids[dose_grid].children:
			button1.disabled = able
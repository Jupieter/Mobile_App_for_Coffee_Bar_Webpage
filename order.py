from re import S
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatButton
from login import LogInCard
from decimal import Decimal
from time import sleep
import requests
import json

Builder.load_file('kv/order.kv')

class OrderMDFillRoundFlatButton(MDFillRoundFlatButton):
	print('DoseButton 0')


	def __init__(self, **kwargs):
		super(OrderMDFillRoundFlatButton, self).__init__(**kwargs)
		self.text_color=(1, 1, 1, 0.3)
	
	def on_disabled(self, instance, value):
		pass
		# print("OrderMDFillRoundFlatButton:   ", self)


class CoffeOrder(MDGridLayout):
	
	def __init__(self, **kwargs):
		super(CoffeOrder, self).__init__(**kwargs)
		self.ordered = [[],[],[],[]]
		self.ware_step_lst = [0,0,0,0]
		self.app = MDApp.get_running_app()
		self.scr2 = self.app.root.ids.scr2_message_lbl
		self.log_card = LogInCard()
		self.active_token = self.log_card.load_token()
		# print(self.scr2)
		self.mess_text1 = "O R D E R"
		Clock.schedule_once(self.load_data_ware, 0)
		# Clock.schedule_once(self.ware_btn_able, 0)
		# Clock.schedule_once(self.fresh_ord_mess, 0)
	
	def ware_ordr_btn(self, btn_id, *args):
		''' carussel button => selected coffee raw material'''
		# print("self.ordered", self.ordered)
		w_order = self.ordered[btn_id]
		print("w_order:        ", w_order)
		self.active_token = self.log_card.load_token()
		if self.active_token == "Empty":
			self.mess_text1 = "Isn't valid login"
			print(self.mess_text1 , "Empty")
		elif w_order != [] and self.active_token != "Empty":
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
			w_dose = Decimal(ware['w_dose'])
			print("w_step", w_step, w_id, w_name,'w_dose', w_dose, type(w_dose))
			texte = str(w_id) + " " + w_name + "\n  " + str(w_dose) +" dose"
			print(texte, btn_text)
			self.ids[btn_text].text = texte
			self.ids[btn_text].text_color=(1, 1, 1, 1)
			self.ids[btn_text].value = w_id
			self.dose_button_able(btn_id, w_id, w_dose)
			self.save_btn_able()
			self.ids[btn_text].md_bg_color=(0, 0.5, 0, 1)
			self.ids[lbl_text].text = texte

			print("self.ids[dose_grid].value:  ", self.ids[grd_text].value)
			self.mess_text1  = texte
		else:
			self.mess_text1  = "Something went wrong. No ware data"	
		self.fresh_ord_mess()
		# Clock.schedule_once(self.fresh_ord_mess, 0)

	def ware_btn_able(self, *args):
		'''buttun disabled if not authenticated '''
		if self.active_token == "Empty" or self.ids["order_btn_0"].value == 0:
			able1 = True
		else:
			able1 = False
		print('able1: ', able1)

		for i in range(1,4,1):
			btn_id = "order_btn_" + str(i)
			print('able1 next: ', able1)
			self.ids[btn_id].disabled = able1
		self.fresh_ord_mess()

	def save_btn_able(self, *args):
		'''buttun disabled if not choice all  '''
		if (self.ids["order_btn_0"].text ==  "Choice Coffee" or
			self.ids["order_btn_1"].text ==  "Choice Sugar" or 
			self.ids["order_btn_2"].text ==  "Choice Milk" or
			self.ids["order_btn_3"].text ==  "Choice Flavour"):
			self.ids["order_save_btn"].disabled = True
		else:
			self.ids["order_save_btn"].disabled =  False
			self.mess_text2 = "You can save your order"
			self.fresh_ord_mess()
		# Clock.schedule_once(self.fresh_ord_mess, 0)

	def oreder_press_dose(self, act_choice, btn_id):
		'''One Choice button selection function'''
		dose_grid = "dose_grid_" + str(btn_id)
		self.ids[dose_grid].value = 0
		print(dose_grid)
		for dose_but in self.ids[dose_grid].children:
			# dose_but.selected = True
			dose_but.text_color=[0, 0, 0, 0.3]
			dose_but.md_bg_color = [0.4, 0.4, 0.4, 1]
			print(dose_but.text, dose_but.text_color, "bg: ", dose_but.md_bg_color)
		act_choice.md_bg_color=(0, 0.5, 0, 1)
		act_choice.text_color=(1, 1, 1, 1)
		self.ids[dose_grid].value = act_choice.value
		if btn_id == "0" and self.ids["dose_grid_0"].value != 0:
			self.ware_btn_able()
			# Clock.schedule_once(self.ware_btn_able, 0)

		lbl_text = "order_end_label_B_" + str(btn_id)
		self.ids[lbl_text].text = str(act_choice.value) + "  ordered dose"
		print("self.ids[dose_grid].value:  ", self.ids[dose_grid].value)

		order_label = "order_label_" + str(btn_id)
		self.mess_text1  = self.ids[order_label].text + " : " + str(act_choice.value) + " dose"
		self.fresh_ord_mess()
		# Clock.schedule_once(self.fresh_ord_mess, 0)

		
	
	def dose_button_able(self, btn_id, w_id, w_dose, *args):
		'''buttun disabled if not authenticated 
			disabled SAVE button if all option isn't selected.
		'''
		print("btn_id, w_id", btn_id, w_id)
		dose_grid = "dose_grid_" + str(btn_id)
		print("dose:          ", w_dose)
		if w_dose == 0:
			able2 = True
		else:
			able2 = False
		print('able2: ',able2)
		for button1 in self.ids[dose_grid].children:
			if button1.value > w_dose:
				button1.disabled = True
			else: 
				button1.disabled = able2
			# button1.selected = False
	
	def btn_text_reset(self, dose_grid):
		print("RESET", self.ids)
		# self.app = MDApp.get_running_app()
#
		self.ids[dose_grid].value = 0
		for dose_but in self.ids[dose_grid].children:
			print(dose_but.text, dose_but.text_color)
			dose_but.text_color=[1, 1, 1, 0.6]
			dose_but.md_bg_color = self.app.theme_cls.primary_color


	def go_home(self, *args):
		sm = self.app.root.ids.nav_bottom
		sm.switch_tab('screen 1')

	def load_data_ware(self, *args):
		print('coffe order data')
		try:
			wares = requests.get('http://coffeeanteportas.herokuapp.com/c_app/order_tastes/').json()
			# wares = requests.get('http://127.0.0.1:8000/c_app/order_tastes/').json()
			print("-----------------wares----------------------")
			for i in range(4):
				self.ordered[i] = wares[i]	
			print('store ware: ', self.ordered)	
			self.mess_text1 = "Order a Coffee with tastes"
			# return self.ordered
		except:
			# self.ids.order_label_0.text = "New coffee brewing time saved."
			print("-----------------problem----------------------")
			print("Problem with internet conection")
			self.mess_text1  = "Something went wrong. No ware data"	
		self.fresh_ord_mess()


	def order_save(self, *args):
		log_card = LogInCard()
		active_user, act_pkey, act_staff = log_card.read_user()
		sends = {
			"coffee_selected": self.ids.order_btn_0.value,
			"coffee_dose": self.ids.dose_grid_0.value,
			"sugar_choice": self.ids.order_btn_1.value if self.ids.order_btn_1.value != 0 else None,
			"sugar_dose": self.ids.dose_grid_1.value,
			"milk_choice": self.ids.order_btn_2.valueif if self.ids.order_btn_2.value != 0 else None,
			"milk_dose": self.ids.dose_grid_2.value,
			"flavour_choice": self.ids.order_btn_3.value if self.ids.order_btn_3.value != 0 else None,
			"flavour_dose": self.ids.dose_grid_3.value,
			"coffe_user": act_pkey
		}
		print("sends:     -----------------------------------------------------")
		print(sends)
		try:
			# log_card = LogInCard()
			# active_token = log_card.load_token()
			token_str = 'Token ' + self.active_token
			hd_token = {'Authorization':token_str}
			if self.active_token != "Empty":
				print('LOG ware_save Token', self.active_token)
				# requests.post('http://127.0.0.1:8000/c_app/order_save/', headers=hd_token, data=sends)
				# requests.post('https://coffeeanteportas.herokuapp.com/c_app/order_save/', headers=hd_token, data=sends)
				self.ids["order_save_btn"].md_bg_color=(0, 0.5, 0, 1)
				self.mess_text2 = "New coffee order saved."
				Clock.schedule_once(self.fresh_ord_mess, 0)
				print(self.mess_text2)
				# self.button_able()
				# self.btn_text_reset()
				# sleep(1)
				Clock.schedule_once(self.go_home, 3)
				# self.go_home()
		except:
			self.mess_text2 = "It seems, there is no internet"
			self.fresh_ord_mess()
			
	
	def fresh_ord_mess(self, *args, **kwargs):
		self.scr2.text = self.mess_text1
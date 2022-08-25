from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager
from datetime import time, datetime, timedelta
import requests
import time
import sqlite3, random, json
from login import LogInCard

Builder.load_file('kv/coffee_make.kv')

class DoseButton(MDFillRoundFlatButton):
	print('DoseButton 0')
	# font_size = 25
	selected = BooleanProperty()

	def __init__(self, **kwargs):
		super(DoseButton, self).__init__(**kwargs)
		self.selected = False
		self.text_color=(1, 1, 1, 0.6)
		sm = ScreenManager
		self.sm = sm
		

class CoffeWare(MDCard): # the.boss@staff.com    Enter1
	print('CoffeWare 0')
	

	def __init__(self, **kwargs):
		super(CoffeWare, self).__init__(**kwargs)
		# self.add_dose_button()
		# self.load_data()
		self.stor = None
		self.ware_step = 0
		self.dt_obj = None
		Clock.schedule_once(self.load_data, 0)
		# Clock.schedule_interval(self.load_data_clk, 5)
		# self.r_fresh()
		self.message = ""
		Clock.schedule_once(self.button_able, 0)
		# Clock.schedule_interval(self.button_able, 3)
		# Clock.schedule_once(self.r_fresh, 0)
		# Clock.schedule_interval(self.r_fresh, 5) 

	def d_on_save(self, instance, value, date_range):
# 		print('d_on_save:',instance, value, date_range)
		self.ids.date_btn.text = str(value)
		self.ids.date_btn.md_bg_color=(0, 0.5, 0, 1)
		Clock.schedule_once(self.button_able, 0)

	def show_date_picker(self):
		act_t = datetime.now()
		end_t = act_t + timedelta(days = 5)
		act_date = str(act_t)[0:10].replace("-", ":")
		end_date =  str(end_t)[0:10].replace("-", ":")
		print('act_t', act_date, end_date)
		min_date = datetime.strptime(act_date, '%Y:%m:%d').date()
		max_date = datetime.strptime(end_date, '%Y:%m:%d').date()
		print(min_date, max_date)
		date_dialog = MDDatePicker(
			min_date=min_date,
			max_date=max_date,
    		)
		date_dialog.bind(on_save=self.d_on_save)
		date_dialog.open()

	def t_on_save(self, instance, value):
		print('Set Time: ', value)
		date = self.ids.date_btn.text
		print('Set Date: ', date)
		dt = str(date) + ' ' + str(value)
		self.dt_obj =datetime.fromisoformat(dt)
		act_t = datetime.now()
		print('act_t  /self.dt_obj: ', act_t, self.dt_obj)
		if self.dt_obj < act_t:
			self.dt_obj = act_t + timedelta(hours = 1)
			t_now = self.dt_obj.time()
		else:
			t_now = value
		print('t_now: ', t_now)
		self.ids.time_btn.text = str(t_now)[0:8]
		self.ids.time_btn.md_bg_color=(0, 0.5, 0, 1)
		Clock.schedule_once(self.button_able, 0)
		
	def show_time_picker(self):
		'''Open time picker dialog.'''	
		time_dialog = MDTimePicker()
		# current_time = now.strftime("%H:%M:%S").time()
		# print(now, '  :  ',current_time)
		# time_dialog.set_time = current_time
		# time_dialog._set_current_time
		time_dialog.bind(on_save=self.t_on_save)
		time_dialog.open()

	
	def load_data(self, *args):
		Clock.schedule_once(self.load_data_clk, 0)

	def load_data_clk(self, *args):
		print('coffe make data')
		log_card = LogInCard()
		active_token = log_card.load_token()
		token_str = 'Token ' + active_token
		hd_token = {'Authorization':token_str}
		if active_token == 'Empty':
			print('token print',self.ids.coffe_ware_label.parent)
		else:	
			print('Request')
			store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/act_ware/', headers=hd_token).json()
			print('store', store)			
			self.stor = self.ware_json(store)
			print(self.stor)
		return self.stor
	
	def ware_json(self, store_d):
		store = []
		for item in store_d:
			it = json.loads(item)
			# print('st', item)
			# print('it', it)
			store.append(it)
		return store
	
	def ware_button(self, *args):
		print("self.stor", self.stor)
		tuple_len = len(self.stor)
		self.ware_step += 1
		if self.ware_step > tuple_len:
			self.ware_step = 1
		id = self.stor[self.ware_step-1]['w_id']
		name = self.stor[self.ware_step-1]['w_name'].replace('Coffee','')
		name.replace(',','')
		dose = self.stor[self.ware_step-1]['w_dose']
		print('self.ware_step',self.ware_step, id, name, dose)
		texte = str(id) + " " + name + " left " + str(dose) +" dose"
		print(texte)
		self.ids.ware_btn.text = texte
		self.ids.ware_btn.md_bg_color=(0, 0.5, 0, 1)
		self.ids.ware_btn.value = id
		Clock.schedule_once(self.button_able, 0)

	def press_dose(self, act_choice):
		# prnt = self.ids.coffe_ware_label.parent
		# print('children1',prnt.ids.dose_grid.children)
		# print('children2',self.ids.dose_grid.children)
		for dose_but in self.ids.dose_grid.children:
			# print(dose_but)
			print(dose_but.text, dose_but.text_color)
			dose_but.selected = False
			dose_but.text_color=[0, 0, 0, 0.3]
			dose_but.md_bg_color = [0.5, 0.5, 0.5, 1]
			act_choice.text_color=(1, 1, 1, 1)
			act_choice.md_bg_color=(0, 0.5, 0, 1)
			print(act_choice.value)
		self.ids.dose_grid.value = act_choice.value
		Clock.schedule_once(self.button_able, 0)
	
	def button_able(self, *args):
		log_card = LogInCard()
		active_token = log_card.load_token()
		active_user, act_pkey, act_staff = log_card.read_user()

		print(active_token)
		if active_token == 'Empty'or act_staff == False:
			able = True
			self.ids.coffe_message_label.text = "Isn't valid login with staff status"
		else:
			able = False
			self.ids.coffe_message_label.text = "Set the parameters:"
		print('able',able)
		prnt = self.ids.coffe_ware_label.parent
		for button1 in self.ids.dose_grid.children:
			button1.disabled = able
		self.ids.ware_btn.disabled = able
		self.ids.date_btn.disabled = able
		if self.ids.date_btn.text == 'Coffee Date':
			self.ids.time_btn.disabled = True
		else:
			self.ids.time_btn.disabled = False
		# Check data to Save button enabled
		if (self.ids.ware_btn.value == 0 or
			self.ids.date_btn.text == 'Coffee Date' or
			self.ids.time_btn.text == 'Coffee Time' or
			self.ids.dose_grid.value == 0):
			self.ids.ware_save.disabled = True 
		else:
			self.ids.ware_save.disabled = False
		print('END able')
		
	def ware_save(self, *args):
		ware = self.ids.ware_btn.value
		dose = self.ids.dose_grid.value
		log_card = LogInCard()
		active_user, act_pkey, act_staff = log_card.read_user()
		if self.dt_obj:
			make_date = self.dt_obj.isoformat()
			print('SAVE', 'self.dt_obj',  make_date, type(make_date))
		sends = {
			"c_make_user": act_pkey,
			"c_make_date": make_date,
			"c_make_ware": ware,
			"c_make_dose": dose
		}
		print(sends)
		# requests.post('https://coffeeanteportas.herokuapp.com/c_app/coffe_make/', data=sends)
		self.ids.coffe_message_label.text = "New coffee brewing time saved."
		print('sleep              sleep')
		time.sleep(2)
	
	def btn_text_reset(self):
		self.ids.ware_btn.value = "Opened Coffee"
		self.ids.ware_btn.value = 0
		self.ids.date_btn.text = 'Coffee Date'
		self.ids.time_btn.text = 'Coffee Time'
		self.ids.dose_grid.value = 0
		self.press_dose(self, act_choice=None)
		self.button_able()
		
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.uix.button import MDFillRoundFlatButton
from datetime import datetime, timedelta
import requests
import json
from login import LogInCard




Builder.load_file('kv/coffee_make.kv')


class MyTimePicker(MDTimePicker):
	def __init__(self, **kwargs):
		super(MyTimePicker, self).__init__(**kwargs)
	
	def _set_am_pm(self, selected: str) -> None:
		"""Used by set_time() to manually set the mode to "am" or "pm"."""
		self.am_pm = selected
		self._am_pm_selector.mode = self.am_pm
		self._am_pm_selector.selected = self.am_pm
	
	def set_time(self, time_obj):
		"""
		Manually set time dialog with the specified time. 
		Overvrited version 12:00-12:59 != 'am'
		"""
		hour = time_obj.hour
		minute = time_obj.minute
		if hour > 12:
			mode = "pm"
			hour -= 12
		else:
			mode = "am"
		if hour > 11:  # Correction: am/pm fault between 12:00-12:59
			mode = "pm"
		hour = str(hour)
		minute = str(minute)
		print(hour, minute, mode)
		self._set_time_input(hour, minute)
		self._set_dial_time(hour, minute)
		self._set_am_pm(mode)

class DoseButton(MDFillRoundFlatButton):

	def __init__(self, **kwargs):
		super(DoseButton, self).__init__(**kwargs)
		self.text_color=(1, 1, 1, 0.3)
	
	def on_disabled(self, instance, value):
		pass
		

class CoffeWare(MDCard):

	def __init__(self, **kwargs):
		super(CoffeWare, self).__init__(**kwargs)
		self.stor = None
		self.ware_step = 0
		self.dt_obj = None
		self.app = MDApp.get_running_app()
		log_card = LogInCard()
		self.active_token = log_card.load_token()
		active_user, self.act_pkey, self.act_staff = log_card.read_user()
		Clock.schedule_once(self.load_data, 0)
		self.message = ""
		Clock.schedule_once(self.button_able, 0) 


	def d_on_save(self, instance, value, date_range):
		'''Date picker save function'''
		self.ids.date_btn.text = str(value)
		self.ids.date_btn.md_bg_color=(0, 0.5, 0, 1)
		Clock.schedule_once(self.button_able, 0)


	def show_date_picker(self):
		'''Open date picker dialog.'''
		act_t = datetime.now()
		end_t = act_t + timedelta(days = 5)
		act_date = str(act_t)[0:10].replace("-", ":")
		end_date =  str(end_t)[0:10].replace("-", ":")
		min_date = datetime.strptime(act_date, '%Y:%m:%d').date()
		max_date = datetime.strptime(end_date, '%Y:%m:%d').date()
		date_dialog = MDDatePicker(
			min_date=min_date,
			max_date=max_date,
    		)
		date_dialog.bind(on_save=self.d_on_save)
		date_dialog.open()


	def t_on_save(self, instance, value):
		'''Time picker save function'''
		date = self.ids.date_btn.text
		dt = str(date) + ' ' + str(value)
		self.dt_obj = datetime.fromisoformat(dt)
		act_t = datetime.now()
		if self.dt_obj < act_t:
			self.dt_obj = act_t + timedelta(hours = 1)
			t_now = self.dt_obj.time()
		else:
			t_now = value
		self.ids.time_btn.text = str(t_now)[0:8]
		self.ids.time_btn.md_bg_color=(0, 0.5, 0, 1)
		Clock.schedule_once(self.button_able, 0)


	def show_time_picker(self):
		'''Open time picker dialog.'''	
		time_dialog = MyTimePicker()
		act_t = datetime.now()
		current_time = datetime.now().time()
		time_dialog.set_time(current_time)
		time_dialog.bind(on_save=self.t_on_save)
		time_dialog.open()

	
	def load_data(self, *args):
		Clock.schedule_once(self.load_data_clk, 0)


	def load_data_clk(self, *args):
		token_str = 'Token ' + self.active_token
		hd_token = {'Authorization':token_str}
		print(hd_token)
		if self.active_token == 'Empty':
			self.mess_text2 = "Isn't valid login with staff status"
		else:	
			print('Token have, Data Request')
			try:
				store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/act_ware/', headers=hd_token).json()
				# print('store', store)			
				self.stor = self.ware_json(store)
				# print("self.stor json:        ",self.stor)
				return self.stor
			except:
				self.mess_text2 = "Problem with internet conection."
				print("Problem with internet conection")

	
	def ware_json(self, store_d):
		'''JSON for tuple '''
		store = []
		for item in store_d:
			it = json.loads(item)
			store.append(it)
		return store


	def ware_button(self, *args):
		''' carussel button => selected coffee raw material'''
		print("self.stor", self.stor)
		if self.stor != None:
			tuple_len = len(self.stor)
			self.ware_step += 1
			if self.ware_step > tuple_len:
				self.ware_step = 1
			id = self.stor[self.ware_step-1]['w_id']
			name = self.stor[self.ware_step-1]['w_name'].replace('Coffee','')
			name.replace(',','')
			dose = self.stor[self.ware_step-1]['w_dose']
			print('self.ware_step',self.ware_step, id, name, dose)
			texte = str(id) + " " + name + "" + str(dose) +" dose"
			print(texte)
			self.ids.ware_btn.text = texte
			self.ids.ware_btn.md_bg_color=(0, 0.5, 0, 1)
			self.ids.ware_btn.value = id
			self.button_able()
		else:
			print(self.active_token)
			if self.active_token == 'Empty':
				self.mess_text2 = "Isn't valid login with staff status"
			else:
				self.mess_text2 = "Something went wrong. No ware data"
			Clock.schedule_once(self.fresh_make_mess, 3)
			Clock.schedule_once(self.fresh_make_mess, 0)


	def press_dose(self, act_choice):
		'''One Choice button selection function'''
		for dose_but in self.ids.make_grid.children:
			print(dose_but.text)
			dose_but.selected = False
			dose_but.text_color = [0, 0, 0, 0.3]
			dose_but.md_bg_color = [0.5, 0.5, 0.5, 1]
			print(dose_but.text, dose_but.text_color)
		act_choice.text_color = (1, 1, 1, 1)
		act_choice.md_bg_color = (0, 0.5, 0, 1)
		print(act_choice.value)
		self.ids.make_grid.value = act_choice.value
		self.button_able()
	

	def button_able(self, *args):
		'''buttun disabled if not authenticated 
			disabled TimePicker if Date not selected
			disabled SAVE button if all option isn't selected.
		'''
		if  self.act_staff == False:
			able = True
			self.mess_text2 = "You have not staff status"
		elif self.active_token == 'Empty':
			able = True
			self.mess_text2 = "Isn't valid login with staff status"
		else:
			able = False
			self.mess_text2 = "Set the parameters:"
		# First coffee selection after the dose
		if self.ids.ware_btn.value == 0:
			able = True
		print(able)
		for button1 in self.ids.make_grid.children:
			button1.disabled = able
		# Date button after Dose selection button
		if self.ids.make_grid.value == 0:
			self.ids.date_btn.disabled = True
		else:
			self.ids.date_btn.disabled = False
		
		# Time button after date button
		if self.ids.date_btn.text == 'Coffee Date':
			self.ids.time_btn.disabled = True
		else:
			self.ids.time_btn.disabled = False
		# Check data to Save button enabled
		if (self.ids.ware_btn.value == 0 or
			self.ids.date_btn.text == 'Coffee Date' or
			self.ids.time_btn.text == 'Coffee Time' or
			self.ids.make_grid.value == 0):
			self.ids.ware_save.disabled = True 
		else:
			self.ids.ware_save.disabled = False
		Clock.schedule_once(self.fresh_make_mess, 3)
		Clock.schedule_once(self.fresh_make_mess, 0)
		print('END able of Make page')
		

	def ware_save(self, *args):
		ware = self.ids.ware_btn.value
		dose = self.ids.make_grid.value
		if self.dt_obj:
			make_date = self.dt_obj.isoformat()
			print('SAVE', 'self.dt_obj',  make_date, type(make_date))
		sends = {
			"c_make_user": self.act_pkey,
			"c_make_date": make_date,
			"c_make_ware": ware,
			"c_make_dose": dose
		}
		print(sends)
		try:
			token_str = 'Token ' + self.active_token
			hd_token = {'Authorization':token_str}
			if self.active_token != "Empty":
				print('LOG ware_save Token', self.active_token)
				# requests.post('https://coffeeanteportas.herokuapp.com/c_app/coffe_make/', headers=hd_token, data=sends)
				self.ids.ware_save.text_color = (1, 1, 1, 1)
				self.ids.ware_save.md_bg_color = (0, 0.5, 0, 1)
				self.mess_text2 = "New coffee brewing time saved."
				Clock.schedule_once(self.fresh_make_mess, 0)
				Clock.schedule_once(self.go_home, 2)
		except:
			self.mess_text2 = "It seems, there is no internet"
			Clock.schedule_once(self.fresh_make_mess, 3)
			Clock.schedule_once(self.fresh_make_mess, 0)
	

	def fresh_make_mess(self, *args, **kwargs):
		print(self.mess_text2)
		self.ids.coffe_message_label.text = self.mess_text2
		self.mess_text2 = ""


	def go_home(self, *args):
		sm = self.app.root.ids.nav_bottom
		sm.switch_tab('screen 1')
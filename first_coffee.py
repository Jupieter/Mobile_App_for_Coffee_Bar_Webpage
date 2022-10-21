from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from datetime import time, datetime
import requests
import sqlite3
from login import LogInCard


presentation = Builder.load_file('kv/first_coffee.kv')
main_ids = ObjectProperty


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()

class FirstCoffe(MDCard): # the.boss@staff.com    Enter1
	# print('LogInCard 0')
	
	def __init__(self, **kwargs):
		super(FirstCoffe, self).__init__(**kwargs)
		self.dt_obj = None
		self.dialog = None
		self.first_id = None
		# print('fk_test', main_ids)
		# sm = ScreenManager()
		# y = sm.screens
		# # print('fk sm :', y)
		x = self.children[0]
		# print('fk ids :', x)
		magam = self
		Clock.schedule_once(magam.load_data, 0)
		Clock.schedule_interval(magam.load_data, 10) # data request
		Clock.schedule_interval(magam.time_back, 1) # time counter sec
		 
	
	def switch_scr2(self):
		'''get a reference to the top right label only by walking through the widget tree'''
		scr1 = MDApp.get_running_app().id_scr_1
		print(scr1)
		# scr1.icon = 'account-check'

	
	# def load_token(self, *args):
	# 	conn = sqlite3.connect('coffe_app.db')
	# 	active_tok = conn.execute("SELECT act_token from act_tokens")
	# 	for row in active_tok:
	# 		active_token = row[0]
	# 	return active_token

	def load_data(self, *args):
		try:
			store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/todaytcoffee/').json()
			print('STORE',store)
			if store == []:
				# print('Empty coffee')
				self.dt_obj = None
				fc_date = 'No coffee today'
				fc_hour = '--'
				fc_min = '--'

			else:
				# print('Else coffee')
				list_data = []
				for item in store:
					list_data.append({'text': item['c_make_date'], "pkey": item['id']})
				first_coffe = list_data[0]['text']
				self.first_id = list_data[0]['pkey']
				print(first_coffe)
				# self.data = first_coffe
				# # print(self.dat			
				fc_date = first_coffe[0:10]
				# print(fc_date)
				fc_hour = first_coffe[11:13]
				fc_min = first_coffe[14:16]
				# print(fc_hour,':',fc_min)

				dt = first_coffe[0:10]+' ' + first_coffe[11:19]
				self.dt_obj =datetime.fromisoformat(dt)
				print('dt_obj', self.dt_obj)
		
		except:
			store = []
			fc_date = 'Problem with internet conection'
			fc_hour = '--'
			fc_min = '--'
		self.ids.fk_datum_label.text = (f'{fc_date}')
		self.ids.fk_hour_label.text = (f'{fc_hour}')
		self.ids.fk_min_label.text = (f'{fc_min}')
		
	
	def time_back(self, *args):
		# counter without data request
		if self.dt_obj:
			act_t = datetime.now()
			timedelta_obj = (self.dt_obj - act_t)
			self.back_sec = timedelta_obj.seconds
			to_hour = int(self.back_sec/3600)
			to_min = int(self.back_sec/60)-to_hour*60
			to_sec = int(self.back_sec)-to_hour*3600-to_min*60
			to_hour ='{:0>2}'.format(to_hour)
			to_min ='{:0>2}'.format(to_min)
			to_sec ='{:0>2}'.format(to_sec)
		else:
			to_hour = '--'
			to_min = '--'
			to_sec = '--'

		self.ids.fk_hour_to_label.text = (f'{to_hour}')
		self.ids.fk_min_to_label.text = (f'{to_min}')
		self.ids.fk_sec_to_label.text = (f'{to_sec}')

	def friends_dialog(self):
		print("megnyomtam")
		datas = None
		sends = {"coffee_selected": self.first_id}
		print(self.first_id)
		log_card = LogInCard()
		active_token = log_card.load_token()
		print('LOG Token', active_token)
		if active_token == "Empty":
			store = ["First Log in!"]
		if active_token != "Empty":
			token_str = 'Token ' + active_token
			hd_token = {'Authorization':token_str}
			print(sends)
			store = requests.post('https://coffeeanteportas.herokuapp.com/c_app/coffe_friends/', headers=hd_token, data=sends).json()
		item_s = []
		for data in store:
			z = Item(text=data, source="image/coffee-ante-porta-512.png")
			item_s.append(z)
		self.dialog = MDDialog(
            title="Friends for the following coffee:",
            type="simple",
            items=item_s
        )
		self.dialog.open()


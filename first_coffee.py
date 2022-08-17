from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.label import Label
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from datetime import time, datetime
import requests
import sqlite3


presentation = Builder.load_file('kv/first_coffee.kv')
main_ids = ObjectProperty

class CounterLabel(Label):
    pass

class FirstCoffe(MDCard): # the.boss@staff.com    Enter1
	# print('LogInCard 0')
	def __init__(self, **kwargs):
		super(FirstCoffe, self).__init__(**kwargs)
		# print('fk_test', main_ids)
		# sm = ScreenManager()
		# y = sm.screens
		magam = self
		# # print('fk sm :', y)
		x = self.children[0]
		# print('fk ids :', x)
		Clock.schedule_once(magam.load_data, 0)
		Clock.schedule_interval(magam.load_data, 1) 
	
	def switch_scr2(self):
        # get a reference to the top right label only by walking through the widget tree
		scr1 = MDApp.get_running_app().id_scr_1
		print(scr1)
		# scr1.icon = 'account-check'

	
	def load_token(self, *args):
		conn = sqlite3.connect('coffe_app.db')
		active_tok = conn.execute("SELECT act_token from act_tokens")
		for row in active_tok:
			active_token = row[0]
			# print ("token = ", active_token)
		# Clock.schedule_interval(# print('tik-tak'), 3)
		return active_token

	def load_data(self, *args):
		store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/todaytcoffee/').json()
		print('STORE',store)
		if store == []:
			# print('Empty coffee')
			fc_date = 'No coffee today'
			fc_hour = '--'
			fc_min = '--'
			to_hour = '--'
			to_min = '--'
			to_sec = '--'
		else:
			# print('Else coffee')
			list_data = []
			for item in store:
				list_data.append({'text': item['c_make_date']})
			first_coffe = list_data[0]['text']
			# print(first_coffe)
			# self.data = first_coffe
			# # print(self.dat			
			fc_date = first_coffe[0:10]
			# print(fc_date)
			fc_hour = first_coffe[11:13]
			fc_min = first_coffe[14:16]
			# print(fc_hour,':',fc_min)

			dt = first_coffe[0:10]+' ' + first_coffe[11:19]
			dt_obj =datetime.fromisoformat(dt)
			act_t = datetime.now()
			# print(dt_obj,'-', type(dt_obj), '-',type(act_t))
			timedelta_obj = (dt_obj - act_t)
			to_hour = int(timedelta_obj.seconds/3600)
			to_min = int(timedelta_obj.seconds/60)-to_hour*60
			to_sec = int(timedelta_obj.seconds)-to_hour*3600-to_min*60
			print(to_hour,to_min, to_sec)
		
		self.ids.fk_datum_label.text = (f'{fc_date}')
		self.ids.fk_hour_label.text = (f'{fc_hour}')
		self.ids.fk_min_label.text = (f'{fc_min}')
		self.ids.fk_hour_to_label.text = (f'{to_hour}')
		self.ids.fk_min_to_label.text = (f'{to_min}')
		self.ids.fk_sec_to_label.text = (f'{to_sec}')
		

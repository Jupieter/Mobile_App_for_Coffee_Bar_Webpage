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


Builder.load_file('kv/coffee_make.kv')
main_ids = ObjectProperty

class CounterLabel(Label):
    pass

class CoffeWare(MDCard): # the.boss@staff.com    Enter1
	print('Coffee 0')
	def __init__(self, **kwargs):
		super(CoffeWare, self).__init__(**kwargs)
		self.load_data()
		magam = self
		Clock.schedule_once(magam.load_data, 0)
		#Clock.schedule_interval(magam.load_data, 5) 
	
	def load_token(self, *args):
		conn = sqlite3.connect('coffe_app.db')
		active_tok = conn.execute("SELECT act_token from act_tokens")
		for row in active_tok:
			active_token = row[0]
			print ("token = ", active_token)
		return active_token
	

	def load_data(self, *args):
		print('recycle ware')
		active_token = self.load_token()
		print('LOG Token', active_token)
		token_str = 'Token ' + active_token
		hd_token = {'Authorization':token_str}
		# print('HEAD Token', hd_token)
		if active_token == 'Empty':
			print(self.ids)
			self.ids.coffe_message_label.text = "Isn't valid login"
		else:	
			print('Request')
			store = requests.get('https://coffeeanteportas.herokuapp.com/c_app/act_ware/', headers=hd_token).json()
			print('store', store)
			self.ids.coffe_message_label.text = "van kávé"
			st = []
			for item in store:
				# sti = item["w_name"])
				print('st', item)
			print(self.ids.coffe_ware_label.text)
			print(self.ids.coffe_message_label.text)
			
		

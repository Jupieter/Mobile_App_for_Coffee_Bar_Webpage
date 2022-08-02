from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivy.properties import ObjectProperty
import time

import requests
import sqlite3
# from main import MyRecycleView
# from main import active_token


Builder.load_file('kv/login.kv')



class LogInCard(MDCard): # the.boss@staff.com    Enter1
	print('LogInCard 0')
	def __init__(self, **kwargs):
		super(LogInCard, self).__init__(**kwargs)
		ld_user = self.load_user()
		self.ids.user.text = ld_user
		# # print(ld_user)
		# x = self.root.ids.screen4.ids.items()
		#x = self.ids.items()
		#for i in x:
		#	# print('x', x)

	# def on_start(self):
		# print('on_start()')
		# print(self.get_root_window()) # -- None
		# print(self.get_parent_window()) # -- None
	# pass

	def log_out(self):
		active_token = self.load_token()
		print('LOG Token', active_token)
		token_str = 'Token ' + active_token
		hd_token = {'Authorization':token_str}
		store = requests.post('https://jupieter.pythonanywhere.com/c_app/logout/', headers=hd_token)
		print(hd_token)
		print(store)
		self.btn_disable(False, False, True)
		self.act_token_db('Empty', 'Empty')
		self.ids.welcome_label.text =('LOG IN')
		scr4 = MDApp.get_running_app().id_scr_4
		self.ids.password.text = ""	
		scr4.icon = 'account-cancel'
		

	def log_in(self):
		print('START LOG')
		user = self.ids.user.text
		password = self.ids.password.text
		if user != "" or password != "" :
			x = {'email':user, 'password':password}
			sends = x
			print(sends)
			store = requests.post('https://jupieter.pythonanywhere.com/c_app/login/', data=sends).json()
			print(store)
			keys = []
			values = []
			for key in store.keys():
				print ('key', key)
				keys.append(key)
			print ('key: ', keys[0] )
			if keys[0] == 'expiry':
				self.ids.welcome_label.text =(f'Logged {user}.')
				act_expiry = store['expiry']
				act_token = store['token']
				print(act_expiry)
				print(act_token)
				self.act_token_db(act_token, act_expiry)
				password='Emp'
				self.act_user_db(user, password)
				self.btn_disable(True, True, False)
				self.ids.welcome_label.text =('LOG OUT')
				scr4 = MDApp.get_running_app().id_scr_4
				self.ids.password.text = ""	
				scr4.icon = 'account-check'
				print('END LOG') 

			elif keys[0] == 'non_field_errors':
				x = store['non_field_errors']
				print('val: ', x)
				self.ids.welcome_label.text =(f' {x}')


			else:
				self.ids.welcome_label.text =(f'Hi /{user}/ wrong email or password!')
				print('WRONG LOG')
	
	def btn_disable(self, btn_in, btn_clr, btn_out):
		self.ids.log_in_btn.disabled = btn_in
		self.ids.log_clr_btn.disabled = btn_clr
		self.ids.log_out_btn.disabled = btn_out

	def load_token(self, *args):
		conn = sqlite3.connect('coffe_app.db')
		active_tk = conn.execute("SELECT act_token from act_tokens")
		for row in active_tk:
			active_token = row[0]
		return active_token

	def load_user(self, *args):
		conn = sqlite3.connect('coffe_app.db')
		user = conn.execute("SELECT act_user from act_users")
		for row in user:
			active_user = row[0]
		return active_user

	def act_token_db(self, act_token, act_expiry):
		print(act_token)
		conn = sqlite3.connect('coffe_app.db')	
		cur = conn.cursor()
		sql = """UPDATE act_tokens 
					SET act_token = ?, act_expiry = ?
					WHERE id = ?"""
		data = (act_token, act_expiry, 1)
		cur.execute(sql, data)
		conn.commit()
		conn.close()

	def act_user_db(self, act_user, act_pass):
		print(act_user, act_pass)
		conn = sqlite3.connect('coffe_app.db')	
		cur = conn.cursor()
		sql = """UPDATE act_users 
					SET act_user = ?, act_pass = ? 
					WHERE id = ?"""
		data = (act_user, act_pass, 1)
		cur.execute(sql, data)
		conn.commit()
		conn.close()

	def read_user(self):
		conn = sqlite3.connect('coffe_app.db')	
		cur = conn.cursor()
		# conn.execute("SELECT act_token from act_tokens")
		sql = """SELECT act_user FROM act_users WHERE id = 1"""
		print(sql)
		data = (1)
		users = cur.execute(sql)
		# print('user: ', users)
		for row in users:
			user = row[0]
			print ("user = ", user)
		conn.close()
		return user


	def clear(self):
		print('Clear  !')
		self.ids.user.text = ""		
		self.ids.password.text = ""	
		self.ids.welcome_label.text = "LOG IN"		

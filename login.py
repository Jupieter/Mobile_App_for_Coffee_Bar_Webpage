from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextFieldRound
from kivy.properties import ObjectProperty
import time

import requests
import sqlite3



Builder.load_file('kv/login.kv')



class LogInCard(MDCard): # the.boss@staff.com    Enter1   {'email': 'boss@staff.com', 'password': 'Enter1'}
	print('LogInCard 0')
	def __init__(self, **kwargs):
		super(LogInCard, self).__init__(**kwargs)
		self.mess_text = ""
		ld_user = self.load_user()
		self.ids.user.text = ld_user


	def log_out(self):
		active_token = self.load_token()
		print('LOG Token', active_token)
		token_str = 'Token ' + active_token
		hd_token = {'Authorization':token_str}
		try:
			store = requests.post('https://coffeeanteportas.herokuapp.com/c_app/logout/', headers=hd_token)
			print(hd_token)
			print(store)
			self.btn_disable(False, False, True)
			self.act_token_db('Empty', 'Empty')
			self.ids.welcome_label.text =('LOG IN')
			scr4 = MDApp.get_running_app().id_scr_4
			self.ids.password.text = ""	
			scr4.icon = 'account-cancel'
			self.ids.login_message_label.text = ""
			self.mess_text = 'Logged out succesfully'
			Clock.schedule_once(self.fresh_mess, 3)
		except:
			store = {'nothing':'nothing'}
			self.mess_text = 'Problem with internet conection'
			Clock.schedule_once(self.fresh_mess, 3)
			print('No internet')
		Clock.schedule_once(self.fresh_mess, 0)
		

	def log_in(self):
		print('START LOG')
		user = self.ids.user.text
		password = self.ids.password.text
		if user != "" or password != "" :
			x = {"email": user, 'password':password}
			sends = x
			print(sends)
			try:
				store = requests.post('https://coffeeanteportas.herokuapp.com/c_app/login/', data=sends).json()
				
				print('login store: ', store)
				keys = []
				for key in store.keys():
					print ('key', key)
					keys.append(key)
				print ('key: ', keys[0] )
				if keys[0] == 'expiry':
					# self.ids.login_message_label.text =(f'Logged: {user}.')
					self.mess_text =(f'Logged: {user}.')
					act_expiry = store['expiry']
					act_token = store['token']
					act_pkey = store['user_pk']
					act_staff = store['is_staff']
					print(act_expiry)
					print(act_token)
					print(act_pkey)
					print(act_staff)
					self.act_token_db(act_token, act_expiry)
					password ='Emp'  # if don't store the password
					print('come USER DB ')
					self.act_user_db(user, password, act_pkey, act_staff)
					self.btn_disable(True, True, False)
					self.ids.welcome_label.text =('LOG OUT')
					scr4 = MDApp.get_running_app().id_scr_4
					self.ids.password.text = ""	
					scr4.icon = 'account-check'
					Clock.schedule_once(self.fresh_mess, 3)
					print('END LOG') 
				else:
					self.mess_text = 'Wrong email or password!'
					Clock.schedule_once(self.fresh_mess, 3)
					print('WRONG LOG')
				
			except:
				store = {'nothing':'nothing'}
				self.mess_text = 'Problem with internet conection'
				Clock.schedule_once(self.fresh_mess, 3)
				print('No internet')
		Clock.schedule_once(self.fresh_mess, 0)
				
	
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
					SET act_token = ?, 
					act_expiry = ?
					WHERE id = ?"""
		data = (act_token, act_expiry, 1)
		cur.execute(sql, data)
		conn.commit()
		conn.close()

	def act_user_db(self, act_user, act_pass, act_pkey, act_staff):
		print(act_user, act_pass, act_pkey, act_staff)
		conn = sqlite3.connect('coffe_app.db')	
		cur = conn.cursor()
		sql = """UPDATE act_users 
					SET act_user = ?, 
					act_pass = ?,
					act_pkey = ?,
					act_staff = ?
					WHERE id = ?"""
		data = (act_user, act_pass, act_pkey, act_staff, 1)
		cur.execute(sql, data)
		conn.commit()
		conn.close()

	def read_user(self):
		conn = sqlite3.connect('coffe_app.db')	
		cur = conn.cursor()
		sql = """SELECT act_user, act_pkey, act_staff FROM act_users WHERE id = 1"""
		print(sql)
		data = (1)
		users = cur.execute(sql)
		print('user: ', users)
		for row in users:
			user = row[0]
			pkey = row[1]
			staff_num = row[2]
			if staff_num == 1:
				staff = True
			else:
				staff = False
			print ("user = ", user)
			print ("pkey = ", pkey)
			print ("staff = ", staff)
		conn.close()
		return user, pkey, staff


	def clear(self):
		print('Clear  !')
		self.ids.user.text = ""		
		self.ids.password.text = ""	
		self.ids.welcome_label.text = "LOG IN"
		self.ids.login_message_label.text = ""		
	
	def fresh_mess(self, *args, **kwargs):
		self.ids.login_message_label.text = self.mess_text
		self.mess_text = ""
		


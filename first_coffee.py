from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem
from kivy.properties import  StringProperty
from datetime import datetime
import requests
from login import LogInCard


presentation = Builder.load_file('kv/first_coffee.kv')


class MyDialog(MDDialog):
	def __init__(self, **kwargs):
		super(MyDialog, self).__init__(**kwargs)


class Item(OneLineAvatarListItem):
	source = StringProperty()
	def __init__(self, **kwargs):
		super(OneLineAvatarListItem, self).__init__(**kwargs)
		app = MDApp.get_running_app()
		self.sm = app.root.ids.nav_bottom

	def on_press(self, **kwargs):
		if self.text == "First Log in!":
			self.sm.switch_tab('screen 4')
		else:
			self.sm.switch_tab('screen 2')
		card = self.parent.parent.parent.parent
		card.dismiss(force=True)


class FirstCoffe(MDCard): # the.boss@staff.com    Enter1
	
	def __init__(self, **kwargs):
		super(FirstCoffe, self).__init__(**kwargs)
		self.dt_obj = None
		self.dialog = None
		self.first_id = None
		Clock.schedule_once(self.load_data, 0)
		Clock.schedule_interval(self.load_data, 15) # data request
		Clock.schedule_interval(self.time_back, 1) # time counter sec
		 

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
				fc_date = first_coffe[0:10]
				fc_hour = first_coffe[11:13]
				fc_min = first_coffe[14:16]
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
		'''counter without data request'''
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
		print("pressed")
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
		self.dialog = MyDialog(
            title="Friends for the following coffee:",
            type="simple",
            items=item_s
        )
		self.dialog.open()



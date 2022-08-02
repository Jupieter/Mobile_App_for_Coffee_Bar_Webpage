import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'
cwd = os.getcwd()
# print(cwd)
os.environ['KIVY_HOME'] = cwd + '/conf'

from kivy.uix.label import Label
# import time
import sqlite3
# import requests

from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivymd.uix.card import MDCard
from kivy.uix.recycleview import RecycleView

# from login import LogInCard
from clock import IncrediblyCrudeClock
# from first_coffee import FirstCoffe

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

active_token = 'Semmi'



class ContentNavigationDrawer(MDBoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''
    
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class TestNavigationDrawer(MDApp):
    counter = NumericProperty(0)
    id_scr_1 = ObjectProperty()
    id_scr_4 = ObjectProperty()
    def build(self):
        print('Build 0')
        
        self.create_db()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"  # "Purple", "Red"
        return Builder.load_file('kv/main.kv')
    
    def create_db(self):
        print('CREATE START DB')
        # Create Database Or Connect To One
        conn = sqlite3.connect('coffe_app.db')
        cur = conn.cursor()
        sql = """CREATE TABLE if not exists act_tokens(
            id INT PRIMARY KEY NOT NULL,
            act_token TEXT,
            act_expiry TEXT)"""
        cur.execute(sql)
        sql = """INSERT OR IGNORE INTO 
                act_tokens (id, act_token) VALUES (?, ?)"""
        data1 = (1,'a1')    
        cur.execute(sql, data1)
        conn.commit()

        sql = """CREATE TABLE if not exists act_users(
            id INT PRIMARY KEY NOT NULL,
            act_user TEXT,
            act_pass TEXT)"""
        cur.execute(sql)
        sql = """INSERT OR IGNORE INTO 
                act_users (id, act_user, act_pass) 
                VALUES (?, ?, ?)"""
        data2 = (1,'a@a.com','abc123')    
        cur.execute(sql, data2)
        conn.commit()
        conn.close()
    
    def on_start(self):
        print('on_start')
        icons_item = {
            "folder": "My files",
            "account-multiple": "Shared with me",
            "star": "Starred",
            "history": "Recent",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        # print(icons_item)
        for icon_name in icons_item.keys():            
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )
        # log = LogInCard()
        # log.act_token_db('Empty', 'Empty')
        # self.root.ids.screen1.add_widget(FirstCoffe())
        self.root.ids.screen3.add_widget(IncrediblyCrudeClock())
        # self.root.ids.screen4.add_widget(LogInCard())
        self.id_scr_1 = self.root.ids.screen1
        self.id_scr_4 = self.root.ids.screen4
        main_rt = self.root
        print('main login', main_rt)

    

    


if __name__ == '__main__':
    print('START MAIN')
    TestNavigationDrawer().run()


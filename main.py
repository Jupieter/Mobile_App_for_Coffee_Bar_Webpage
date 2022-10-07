import os
os.environ['KIVY_NO_CONSOLELOG'] = '0'
cwd = os.getcwd()
# print(cwd)
os.environ['KIVY_HOME'] = cwd + '/conf'

print("0")
import sqlite3
print("sqlite3")
# corePrime 480 * 800, J3 - 720 x 1280, A13 2408 x 1080 a20e 720x1560
from kivy.uix.recycleview import RecycleView
print("1")
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
print("2")
from kivymd.app import MDApp
print("3")
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
print("4")
from kivymd.uix.boxlayout import MDBoxLayout
print("5")
from kivymd.uix.list import MDList
print("6")
from kivymd.uix.card import MDCard
print("7")
from kivymd.uix.list import OneLineIconListItem
print("8")
from kivymd.theming import ThemableBehavior
print("9")
from kivy.lang import Builder
print("10")

from login import LogInCard
print("LogInCard")
from coffe_make import CoffeWare
print("CoffeWare")
from first_coffee import FirstCoffe
print("FirstCoffe")
from order import CoffeOrder
print("CoffeOrder")
from kivy.uix.scrollview import ScrollView
from roulettescroll import RouletteScrollEffect
print("afer inports")

active_token = 'Semmi'


class ItemDrawer(OneLineIconListItem):
    print('ItemDrawer 0')
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class MDBottomNavigationItemSc1(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super(MDBottomNavigationItemSc1, self).__init__(**kwargs)


class MDBottomNavigationItemSc2(MDBottomNavigationItem):

    def __init__(self, **kwargs):
        super(MDBottomNavigationItemSc2, self).__init__(**kwargs)
        print('MD scr3')
        # self.app = MDApp.get_running_app()

    # def on_enter(self, *args):
    #     print("*  on_enter  CoffeOrder*")
    #     self.app.root.ids.order_grid.add_widget(CoffeOrder())
    #     self.app.root.ids.order_grid.add_widget(MilkOrder())
    # 
    # def on_leave(self, *args):
    #     print("*  on_leave  CoffeOrder*")
    #     main_app = CoffeeBarApp()
    #     grid_ch = self.app.root.ids.order_grid
    #     print(grid_ch)
    #     ch = []
    #     for child in grid_ch.children:
    #         print(child)
    #         ch.append(child)
    #     for dt in ch:
    #         grid_ch.remove_widget(dt)
    #     ch = []
 

class MDBottomNavigationItemSc3(MDBottomNavigationItem):
    pass
	
    # def __init__(self, **kwargs):
    #     super(MDBottomNavigationItemSc3, self).__init__(**kwargs)
    #     print('MD scr3')
    #     self.app = MDApp.get_running_app()
    # 
    # def on_enter(self, *args):
    #     print("*  on_enter  *")
    #     self.theme_cls.theme_style = "Light"
    #     self.theme_cls.primary_palette = "Brown"  # "Purple", "Red"
    #     self.app.root.ids.screen3.add_widget(CoffeWare())
    # 
    # def on_leave(self, *args):
    #     print("*  on_leave  *")
    #     self.app.root.ids.screen3.remove_widget(CoffeWare())
    #     grid = self.app.root.ids.screen3
    #     print(grid)
    #     ch = []
    #     for child in grid.children:
    #         print(child)
    #         ch.append(child)
    #     for dt in ch:
    #         grid.remove_widget(dt)
    #     ch = []
    #     grid_e = self.app.root.ids.screen3
    #     print("grid_e: ", grid_e.children)
# 

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


class CoffeeBarApp(MDApp):
    def __init__(self, **kwargs):
        print("--init--")
        super(CoffeeBarApp, self).__init__(**kwargs)
        
    counter = NumericProperty(0)
    id_scr_1 = ObjectProperty()
    scr_2_mess_lbl = ObjectProperty()
    id_scr_4 = ObjectProperty()
    


    def screen_make():
        print('Coffe Make switch')
        # coffe_make = CoffeWare()

    def build(self):
        print('Build 0')
        self.icon = 'conf/icon/coffee-ante-porta-512.png'
        
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
            act_pass TEXT,
            act_pkey INT NOT NULL default 0,
            act_staff BOOLEAN NOT NULL default 0 
            )"""
        cur.execute(sql)
        sql = """INSERT OR IGNORE INTO 
                act_users (id, act_user, act_pass) 
                VALUES (?, ?, ?)"""
        data2 = (1,'a@aa.com','abc1234')  
        print(data2)  
        cur.execute(sql, data2)
        conn.commit()
        conn.close()
    
    def on_start(self):
        print('on_start')
        icons_item = {
            "basket-plus-outline": "Acquisition",
            "account-multiple": "Warehouse",
            "storefront-outline": "Store",
            "notebook-edit-outline": "Booking",
            "email-send-outline": "Contact",
            "web": "Statistic",
        }
        # print(icons_item)
        for icon_name in icons_item.keys():            
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )
        log = LogInCard()
        log.act_token_db('Empty', 'Empty')
        self.root.ids.screen1.add_widget(FirstCoffe())
        self.root.ids.order_scroll.add_widget(CoffeOrder())
        # self.root.ids["order_scroll"].scroll_y = RouletteScrollEffect(anchor=20, interval=40)
        self.root.ids.screen3.add_widget(CoffeWare())
        self.root.ids.screen4.add_widget(LogInCard())
        self.id_scr_1 = self.root.ids.screen1
        self.scr_2_mess_lbl = self.root.ids.scr2_message_lbl
        self.id_scr_4 = self.root.ids.screen4
        main_rt = self.root
        print('main login:', main_rt)
        from kivy import platform
        from service.main import start_service
        if platform == "android":
            start_service()
            print("Android service called")
        
    def button_pressed(self):
        from plyer import notification
        print("toast - button_pressed")
        notification.notify(title='New Coffee', message="New coffe time:", toast=True)
    
    def button2_pressed(self):
        from plyer import notification
        print("notification - button_pressed")
        notification.notify(title='New Coffee', message="New coffe time:", ticker= "New Coffee", app_icon='image/coffe_icon1.png', toast=False)

    def button3_pressed(self):
        print("vibrator - button_pressed")
        from plyer import vibrator
        vibrator.vibrate(2)  # vibrate for 2 seconds
   


if __name__ == '__main__':
    print('START MAIN')
    CoffeeBarApp().run()

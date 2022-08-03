from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import ObjectProperty

import time

Builder.load_file('kv/clock.kv')


class IncrediblyCrudeClock(MDCard):
    print('LogInCard 0')
    def __init__(self, **kwargs):
        super(IncrediblyCrudeClock, self).__init__(**kwargs)
        crudeclock = self
        Clock.schedule_once(crudeclock.update, 0)
        Clock.schedule_interval(crudeclock.update, 1) 

    def update(self, *args):
        self.ids.clock_btn.text = time.asctime()
        print('TIME')  
        
        
#      
         

#class TimeApp(MDApp):
#    def build(self):
#        crudeclock = IncrediblyCrudeClock()
#        Clock.schedule_once(crudeclock.update, 0)
#        Clock.schedule_interval(crudeclock.update, 1)
#        return crudeclock
#
#if __name__ == "__main__":
#    TimeApp().run()
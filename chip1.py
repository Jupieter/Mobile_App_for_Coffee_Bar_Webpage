from logging import root
from kivy.animation import Animation
from kivy.lang import Builder

from kivymd.uix.screen import MDScreen
from kivymd.uix.chip import MDChip
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.app import MDApp
from kivy.properties import BooleanProperty

KV = '''
<MyScreen>

    MDBoxLayout:
        orientation: "vertical"
        adaptive_size: True
        spacing: "12dp"
        padding: "56dp"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            text: "One choice"
            bold: True
            font_style: "H5"
            adaptive_size: True

        MDGridLayout:
            id: chip_box
            cols: 2
            adaptive_size: True
            spacing: "25dp"
            
            MyChip:
                text: "2 Dose"
                value: 2
                on_press: root.press_dose(self)
                
            MyChip:
                text: "4 Dose"
                value: 4
                on_press: root.press_dose(self)

            MyChip:
                text: "6 Dose"
                value: 6
                on_press: root.press_dose(self)

            MyChip:
                text: "8 Dose"
                value: 8
                on_press: root.press_dose(self)
                

ScreenManager:

    MyScreen:
'''


class MyChip(MDFillRoundFlatButton):
    font_size = 25
    selected = BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = False
        self.text_color=(0, 0, 0, 0.6)

class MyScreen(MDScreen):

    def press_dose(self, act_choice):
        print(self.ids.chip_box.children)
        for dose_but in self.ids.chip_box.children:
            print(dose_but)
            dose_but.selected = False
            dose_but.text_color=(0, 0, 0, 0.3)
            dose_but.md_bg_color = (0.5, 0.5, 0.5, 1)
            act_choice.text_color=(0, 0, 0, 1)
            act_choice.md_bg_color=(0, 0.5, 0, 1)
            print(act_choice.value)
        

        



class Test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"
        return Builder.load_string(KV)
    print(root)


Test().run()
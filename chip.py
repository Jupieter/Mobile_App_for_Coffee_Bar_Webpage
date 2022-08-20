from kivy.animation import Animation
from kivy.lang import Builder

from kivymd.uix.screen import MDScreen
from kivymd.uix.chip import MDChip
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
            text: "Multiple choice"
            bold: True
            font_style: "H5"
            adaptive_size: True

        MDGridLayout:
            id: chip_box
            cols: 2
            adaptive_size: True
            spacing: "8dp"

            MyChip:
                text: "Elevator"
                
            MyChip:
                text: "Washer / Dryer"
                
            MyChip:
                text: "Fireplace"
                

            MyChip:
                text: "Bath"
                
                

ScreenManager:

    MyScreen:
'''


class MyChip(MDChip):
    # selected_chip_color  = (1, 0, 0, 0.5)
    text_color = (0, 0, 0, 0.5)
    _no_ripple_effect = False
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 0
    
    def on_press(self):
        sc = MyScreen()
        sc.removes_marks_all_chips()
        self.check = True
        
        self.set_chip_bg_color()
        self.set_chip_text_color()
        magam = self

    def set_chip_bg_color(self):
        '''
        Will be called every time the chip is activated/deactivated.
        Sets the background color of the chip.
        '''
        #print('self: ',self.text, self.check)
        #self.md_bg_color = ((0, 0, 0, 0.4) if self.check
        #    else (self.theme_cls.bg_darkest if self.theme_cls.theme_style == "Light"
        #        else (
        #            self.theme_cls.bg_light
        #            if not self.disabled
        #            else self.theme_cls.disabled_hint_text_color
        #        )
        #    )
        #)
        print(self.theme_cls.theme_style)
        if self.theme_cls.theme_style == "Light":
            print('li')
            if self.check == True:
                self.theme_cls.bg_darkest
                print('bg_darkest')
            else:
                self.theme_cls.bg_light
                print('bg_light')
        else:
            if self.check == True:
                self.theme_cls.bg_light
            else:
                self.theme_cls.bg_darkest

    def set_chip_text_color(self):
        if self.check == False:
            self.text_color=(0, 0, 0, 0.4)
            # Animation(text_color=(0, 0, 0, 0.4) , d=0.2 ).start(self.ids.label)
        else:
            self.text_color=(0, 0, 0, 1)
            selected_chip_color  = (1, 0, 0, 1)
            # Animation(text_color=(0, 0, 0, 1), d=0.2 ).start(self.ids.label)


class MyScreen(MDScreen):
    def removes_marks_all_chips(self):
        for instance_chip in self.ids.chip_box.children:
            instance_chip.check = False
            print(instance_chip.text, instance_chip.check)



class Test(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"
        return Builder.load_string(KV)


Test().run()